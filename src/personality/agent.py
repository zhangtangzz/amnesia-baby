"""
Personality Agent

负责根据人格证据构建人格画像
"""

from typing import List, Dict, Any
from .evidence import PersonalityEvidence, PersonalityTrait
from .profile import PersonalityProfile
from .big_five import BigFiveProfile
from .enneagram import EnneagramProfile


class PersonalityAgent:
    """
    人格 Agent
    
    根据人格证据分析并生成人格画像
    """
    
    def __init__(self):
        """初始化 agent"""
        pass
    
    async def analyze(self, evidence_list: List[PersonalityEvidence]) -> Dict[str, Any]:
        """
        分析人格证据，生成人格画像
        
        Args:
            evidence_list: 人格证据列表
            
        Returns:
            Dict: 包含 personality, big_five, enneagram_top3 的结果
        """
        # 计算人格画像
        personality = self._calculate_personality(evidence_list)
        
        # 计算大五人格
        big_five = self._calculate_big_five(personality)
        
        # 计算九型人格
        enneagram = self._calculate_enneagram(personality)
        enneagram_top3 = dict(enneagram.get_top3())
        
        return {
            "personality": personality.model_dump(),
            "big_five": big_five.model_dump(),
            "enneagram_top3": enneagram_top3,
        }
    
    def _calculate_personality(self, evidence_list: List[PersonalityEvidence]) -> PersonalityProfile:
        """
        计算人格画像
        
        Args:
            evidence_list: 人格证据列表
            
        Returns:
            PersonalityProfile: 人格画像
        """
        # 初始化默认值
        traits = {trait.value: 0.5 for trait in PersonalityTrait}
        
        # 根据证据更新分数
        for evidence in evidence_list:
            trait = evidence.trait.value
            # 加权平均：分数 * 置信度
            if trait in traits:
                traits[trait] = evidence.score * evidence.confidence
        
        return PersonalityProfile(**traits)
    
    def _calculate_big_five(self, personality: PersonalityProfile) -> BigFiveProfile:
        """
        计算大五人格
        
        基于人格画像映射到大五人格维度
        
        Args:
            personality: 人格画像
            
        Returns:
            BigFiveProfile: 大五人格
        """
        # 映射关系（简化版本）
        openness = (personality.curiosity + personality.creativity) / 2
        conscientiousness = (personality.responsibility + personality.achievement_drive) / 2
        extraversion = (personality.social_need + personality.dominance) / 2
        agreeableness = (personality.empathy + (1 - personality.dominance)) / 2
        neuroticism = (personality.security_need + (1 - personality.independence)) / 2
        
        return BigFiveProfile(
            openness=openness,
            conscientiousness=conscientiousness,
            extraversion=extraversion,
            agreeableness=agreeableness,
            neuroticism=neuroticism,
        )
    
    def _calculate_enneagram(self, personality: PersonalityProfile) -> EnneagramProfile:
        """
        计算九型人格
        
        基于人格画像映射到九型人格
        
        Args:
            personality: 人格画像
            
        Returns:
            EnneagramProfile: 九型人格
        """
        # 映射关系（简化版本）
        type1 = (personality.responsibility + personality.achievement_drive) / 2
        type2 = (personality.empathy + personality.social_need) / 2
        type3 = (personality.achievement_drive + personality.dominance) / 2
        type4 = (personality.creativity + personality.independence) / 2
        type5 = (personality.curiosity + personality.independence) / 2
        type6 = (personality.security_need + personality.responsibility) / 2
        type7 = (personality.curiosity + personality.social_need) / 2
        type8 = (personality.dominance + personality.risk_preference) / 2
        type9 = ((1 - personality.dominance) + (1 - personality.security_need)) / 2
        
        return EnneagramProfile(
            type1=type1,
            type2=type2,
            type3=type3,
            type4=type4,
            type5=type5,
            type6=type6,
            type7=type7,
            type8=type8,
            type9=type9,
        )