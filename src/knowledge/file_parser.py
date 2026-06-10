"""
文件解析器

支持从 .txt, .md, .csv, .docx, .pdf 文件中提取文本
"""

import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".docx", ".pdf"}


def parse_file(content_bytes: bytes, filename: str) -> Optional[str]:
    """
    从文件字节内容中提取文本

    Args:
        content_bytes: 文件字节内容
        filename: 文件名（用于判断类型）

    Returns:
        Optional[str]: 提取的文本，失败返回 None
    """
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    if ext in (".txt", ".md", ".csv"):
        return _parse_text(content_bytes)
    elif ext == ".docx":
        return _parse_docx(content_bytes)
    elif ext == ".pdf":
        return _parse_pdf(content_bytes)
    else:
        logger.warning(f"Unsupported file extension: {ext}")
        return None


def _parse_text(content_bytes: bytes) -> str:
    """解析纯文本文件"""
    try:
        return content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        try:
            return content_bytes.decode("gbk")
        except UnicodeDecodeError:
            return content_bytes.decode("utf-8", errors="replace")


def _parse_docx(content_bytes: bytes) -> Optional[str]:
    """解析 .docx 文件"""
    try:
        from docx import Document
        doc = Document(io.BytesIO(content_bytes))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        logger.error(f"Failed to parse docx: {e}")
        return None


def _parse_pdf(content_bytes: bytes) -> Optional[str]:
    """解析 .pdf 文件"""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(io.BytesIO(content_bytes))
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text.strip())
        return "\n\n".join(pages) if pages else None
    except Exception as e:
        logger.error(f"Failed to parse pdf: {e}")
        return None
