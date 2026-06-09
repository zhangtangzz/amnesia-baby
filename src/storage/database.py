"""
持久化存储

基于 JSON 文件的简单持久化，支持角色和知识库数据
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

# 数据目录
DATA_DIR = Path(__file__).parent.parent.parent / "data"


def _ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(exist_ok=True)


def _get_file_path(name: str) -> Path:
    """获取数据文件路径"""
    _ensure_data_dir()
    return DATA_DIR / f"{name}.json"


def save_json(name: str, data: Any) -> None:
    """
    保存 JSON 数据到文件

    Args:
        name: 数据名称（不含扩展名）
        data: 要保存的数据
    """
    path = _get_file_path(name)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.debug(f"Saved {name} to {path}")
    except Exception as e:
        logger.error(f"Failed to save {name}: {e}")


def load_json(name: str, default: Any = None) -> Any:
    """
    从文件加载 JSON 数据

    Args:
        name: 数据名称（不含扩展名）
        default: 默认值

    Returns:
        加载的数据，不存在返回 default
    """
    path = _get_file_path(name)
    if not path.exists():
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load {name}: {e}")
        return default
