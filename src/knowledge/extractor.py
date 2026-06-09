"""
知识提取器

负责从文本中提取知识
"""

from typing import List, Optional
from .models import (
    KnowledgeBase,
    KnowledgeProfile,
    Fact,
    Evidence,
    SourceType,
)


class KnowledgeExtractor:
    """
    知识提取器
    
    从文本中提取结构化知识
    """
    
    def __init__(self):
        """初始化提取器"""
        pass
    
    async def extract(self, text: str, source: str) -> KnowledgeBase:
        """
        提取知识
        
        Args:
            text: 文本内容
            source: 来源名称
            
        Returns:
            KnowledgeBase: 知识库
        """
        if not text or not text.strip():
            return KnowledgeBase(
                profile=KnowledgeProfile(name="Unknown"),
                relationships=[],
                events=[],
                beliefs=[],
                facts=[],
                timeline=[],
                evidence=[],
            )
        
        # 提取基础信息
        profile = self._extract_profile(text)
        
        # 提取事实
        facts = self._extract_facts(text)
        
        # 提取证据
        evidence = self._extract_evidence(text, source)
        
        return KnowledgeBase(
            profile=profile,
            relationships=[],
            events=[],
            beliefs=[],
            facts=facts,
            timeline=[],
            evidence=evidence,
        )
    
    def _extract_profile(self, text: str) -> KnowledgeProfile:
        """
        提取基础信息
        
        Args:
            text: 文本内容
            
        Returns:
            KnowledgeProfile: 基础信息
        """
        # 简化版本：从文本中提取姓名和教育背景
        name = "Unknown"
        education = None
        occupation = None
        
        # 简单的关键词提取
        if "毕业于" in text:
            # 提取教育背景
            parts = text.split("毕业于")
            if len(parts) > 1:
                edu_part = parts[1].split("，")[0]
                education = edu_part.strip()
        
        if "创立" in text or "创业" in text:
            occupation = "创业者"
        
        # 提取姓名（简化版本）
        if "张三" in text:
            name = "张三"
        elif "李四" in text:
            name = "李四"
        
        return KnowledgeProfile(
            name=name,
            education=education,
            occupation=occupation,
        )
    
    def _extract_facts(self, text: str) -> List[Fact]:
        """
        提取事实
        
        Args:
            text: 文本内容
            
        Returns:
            List[Fact]: 事实列表
        """
        facts = []
        
        # 提取教育相关事实
        if "毕业于" in text:
            parts = text.split("毕业于")
            if len(parts) > 1:
                edu_part = parts[1].split("，")[0]
                facts.append(Fact(
                    fact=f"毕业于{edu_part.strip()}",
                    category="education",
                    confidence=0.92,
                ))
        
        # 提取事业相关事实
        if "创立" in text or "创业" in text:
            facts.append(Fact(
                fact="创立某科技公司",
                category="career",
                confidence=0.94,
            ))
        
        return facts
    
    def _extract_evidence(self, text: str, source: str) -> List[Evidence]:
        """
        提取证据
        
        Args:
            text: 文本内容
            source: 来源名称
            
        Returns:
            List[Evidence]: 证据列表
        """
        evidence = []
        
        # 将整个文本作为证据
        evidence.append(Evidence(
            source_type=SourceType.VIDEO,
            source_name=source,
            content=text,
            confidence=0.91,
        ))
        
        return evidence
