"""
文本素材解析器

负责解析文本素材，提取人格证据
"""

from typing import List
from ..personality.evidence import PersonalityEvidence, PersonalityTrait


class TextMaterialParser:
    """
    文本素材解析器
    
    解析文本内容，提取人格证据
    """
    
    def __init__(self):
        """初始化解析器"""
        # 关键词映射到人格维度（简化版本）
        self.trait_keywords = {
            PersonalityTrait.RISK_PREFERENCE: [
                "风险", "冒险", "挑战", "大胆", "勇敢", "创新", "突破",
            ],
            PersonalityTrait.ACHIEVEMENT_DRIVE: [
                "成功", "目标", "追求", "卓越", "成就", "优秀", "领先",
            ],
            PersonalityTrait.CURIOSITY: [
                "探索", "好奇", "学习", "研究", "发现", "未知", "新奇",
            ],
            PersonalityTrait.EMPATHY: [
                "理解", "共情", "关心", "帮助", "支持", "体贴", "善良",
            ],
            PersonalityTrait.DOMINANCE: [
                "领导", "主导", "控制", "指挥", "权威", "强大", "自信",
            ],
            PersonalityTrait.INDEPENDENCE: [
                "独立", "自主", "自由", "自我", "个人", "独自", "单独",
            ],
            PersonalityTrait.RESPONSIBILITY: [
                "责任", "负责", "担当", "可靠", "信任", "承诺", "认真",
            ],
            PersonalityTrait.CREATIVITY: [
                "创造", "创新", "想象", "独特", "新颖", "艺术", "设计",
            ],
            PersonalityTrait.SOCIAL_NEED: [
                "社交", "朋友", "团队", "合作", "交流", "人脉", "关系",
            ],
            PersonalityTrait.SECURITY_NEED: [
                "安全", "稳定", "保障", "保护", "谨慎", "保守", "可靠",
            ],
        }
    
    async def parse(self, text: str, source: str) -> List[PersonalityEvidence]:
        """
        解析文本，提取人格证据
        
        Args:
            text: 文本内容
            source: 证据来源
            
        Returns:
            List[PersonalityEvidence]: 人格证据列表
        """
        if not text or not text.strip():
            return []
        
        evidence_list = []
        
        # 遍历关键词映射
        for trait, keywords in self.trait_keywords.items():
            # 检查文本是否包含关键词
            matched_keywords = [kw for kw in keywords if kw in text]
            
            if matched_keywords:
                # 计算分数（简化版本：基于匹配关键词数量）
                score = min(len(matched_keywords) / 3.0, 1.0)
                
                # 计算置信度（简化版本）
                confidence = 0.7 + (len(matched_keywords) * 0.05)
                confidence = min(confidence, 1.0)
                
                # 创建证据
                evidence = PersonalityEvidence(
                    trait=trait,
                    score=score,
                    evidence=text,
                    source=source,
                    confidence=confidence,
                    metadata={"matched_keywords": matched_keywords},
                )
                evidence_list.append(evidence)
        
        return evidence_list