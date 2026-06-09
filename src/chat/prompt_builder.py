"""
Prompt 构建器

负责构建角色聊天的 Prompt
"""

from typing import Dict, Any


class PromptBuilder:
    """
    Prompt 构建器
    
    根据角色信息、知识库和用户消息构建 Prompt
    """
    
    def __init__(self):
        """初始化构建器"""
        pass
    
    def build(
        self,
        character: Dict[str, Any],
        knowledge: Dict[str, Any],
        message: str,
    ) -> str:
        """
        构建 Prompt
        
        Args:
            character: 角色信息
            knowledge: 知识库
            message: 用户消息
            
        Returns:
            str: 构建的 Prompt
        """
        # 获取角色信息
        name = character.get("name", "Unknown")
        personality = character.get("personality")
        
        # 构建人格描述
        personality_desc = self._build_personality_description(personality)
        
        # 构建知识描述
        knowledge_desc = self._build_knowledge_description(knowledge)
        
        # 构建完整 Prompt
        prompt = f"""你正在扮演角色: {name}

## 角色人格

{personality_desc}

## 角色知识

{knowledge_desc}

## 用户消息

{message}

## 回复要求

请以角色的身份回复用户的消息。回复应该：
1. 符合角色的人格特征
2. 基于角色的知识
3. 自然、流畅、有说服力

请开始回复："""
        
        return prompt
    
    def _build_personality_description(self, personality) -> str:
        """
        构建人格描述
        
        Args:
            personality: 人格画像
            
        Returns:
            str: 人格描述
        """
        if personality is None:
            return "暂无人格信息"
        
        traits = []
        if hasattr(personality, 'achievement_drive'):
            traits.append(f"- 成就驱动: {personality.achievement_drive:.2f}")
        if hasattr(personality, 'curiosity'):
            traits.append(f"- 好奇心: {personality.curiosity:.2f}")
        if hasattr(personality, 'risk_preference'):
            traits.append(f"- 风险偏好: {personality.risk_preference:.2f}")
        if hasattr(personality, 'empathy'):
            traits.append(f"- 共情能力: {personality.empathy:.2f}")
        if hasattr(personality, 'dominance'):
            traits.append(f"- 支配性: {personality.dominance:.2f}")
        
        return "\n".join(traits) if traits else "暂无人格信息"
    
    def _build_knowledge_description(self, knowledge: Dict[str, Any]) -> str:
        """
        构建知识描述
        
        Args:
            knowledge: 知识库
            
        Returns:
            str: 知识描述
        """
        knowledge_list = knowledge.get("knowledge", [])
        
        if not knowledge_list:
            return "暂无知识信息"
        
        descriptions = []
        for item in knowledge_list:
            topic = item.get("topic", "")
            content = item.get("content", "")
            if topic and content:
                descriptions.append(f"- {topic}: {content}")
        
        return "\n".join(descriptions) if descriptions else "暂无知识信息"