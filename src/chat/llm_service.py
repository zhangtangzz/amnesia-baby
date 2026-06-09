"""
LLM 服务

负责调用 LLM 生成回复
"""

from typing import Optional
import openai
from ..config import get_settings


class LLMService:
    """
    LLM 服务
    
    调用 OpenAI 兼容的 LLM 生成回复
    """
    
    def __init__(self):
        """初始化服务"""
        self.settings = get_settings()
        self.client = openai.AsyncOpenAI(
            api_key=self.settings.openai_api_key,
            base_url=self.settings.openai_api_base,
        )
    
    async def generate(self, prompt: str, context: Optional[str] = None) -> str:
        """
        生成回复
        
        Args:
            prompt: Prompt 内容
            context: 上下文信息
            
        Returns:
            str: 生成的回复
            
        Raises:
            ValueError: Prompt 为空
            Exception: LLM 调用失败
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # 构建消息
        messages = []
        
        if context:
            messages.append({"role": "system", "content": context})
        
        messages.append({"role": "user", "content": prompt})
        
        # 调用 LLM
        response = await self._call_llm(messages)
        
        return response.choices[0].message.content
    
    async def _call_llm(self, messages):
        """
        调用 LLM
        
        Args:
            messages: 消息列表
            
        Returns:
            LLM 响应
        """
        return await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )