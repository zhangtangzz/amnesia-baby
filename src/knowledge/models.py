"""
知识库数据模型
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class RelationshipType(str, Enum):
    """关系类型枚举"""
    PARENT = "父母"
    SIBLING = "兄弟姐妹"
    FRIEND = "朋友"
    COLLEAGUE = "同事"
    PARTNER = "伴侣"
    MENTOR = "导师"
    COMPETITOR = "竞争对手"
    PARTNER_BUSINESS = "合作伙伴"


class SourceType(str, Enum):
    """来源类型枚举"""
    VIDEO = "video"
    AUDIO = "audio"
    ARTICLE = "article"
    WIKI = "wiki"
    SOCIAL_MEDIA = "social_media"
    CHAT = "chat"
    USER_UPLOAD = "user_upload"


class KnowledgeProfile(BaseModel):
    """基础信息"""
    name: str = Field(..., description="姓名")
    alias: List[str] = Field(default=[], description="别名")
    gender: Optional[str] = Field(default=None, description="性别")
    birthday: Optional[str] = Field(default=None, description="生日")
    occupation: Optional[str] = Field(default=None, description="职业")
    nationality: Optional[str] = Field(default=None, description="国籍")
    education: Optional[str] = Field(default=None, description="教育背景")
    location: Optional[str] = Field(default=None, description="所在地")
    description: Optional[str] = Field(default=None, description="描述")


class Relationship(BaseModel):
    """人物关系"""
    person_id: Optional[str] = Field(default=None, description="人物ID")
    name: str = Field(..., description="姓名")
    relationship: str = Field(..., description="关系类型")
    closeness: float = Field(..., ge=0.0, le=1.0, description="亲密度")
    description: Optional[str] = Field(default=None, description="描述")


class Event(BaseModel):
    """重要事件"""
    event_id: Optional[str] = Field(default=None, description="事件ID")
    title: str = Field(..., description="标题")
    time: Optional[str] = Field(default=None, description="时间")
    location: Optional[str] = Field(default=None, description="地点")
    description: Optional[str] = Field(default=None, description="描述")
    impact: float = Field(..., ge=0.0, le=1.0, description="影响度")


class Belief(BaseModel):
    """观点体系"""
    topic: str = Field(..., description="主题")
    stance: str = Field(..., description="立场")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")


class Fact(BaseModel):
    """事实库"""
    fact: str = Field(..., description="事实")
    category: str = Field(..., description="类别")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")


class Timeline(BaseModel):
    """人生时间轴"""
    year: str = Field(..., description="年份")
    events: List[str] = Field(..., description="事件列表")


class Evidence(BaseModel):
    """证据库"""
    source_type: str = Field(..., description="来源类型")
    source_name: str = Field(..., description="来源名称")
    content: str = Field(..., description="内容")
    confidence: float = Field(..., ge=0.0, le=1.0, description="置信度")


class KnowledgeBase(BaseModel):
    """知识库"""
    profile: KnowledgeProfile = Field(..., description="基础信息")
    relationships: List[Relationship] = Field(default=[], description="人物关系")
    events: List[Event] = Field(default=[], description="重要事件")
    beliefs: List[Belief] = Field(default=[], description="观点体系")
    facts: List[Fact] = Field(default=[], description="事实库")
    timeline: List[Timeline] = Field(default=[], description="人生时间轴")
    evidence: List[Evidence] = Field(default=[], description="证据库")
