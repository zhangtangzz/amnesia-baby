"""
自定义异常
"""


class PersonalityError(Exception):
    """人格系统基础异常"""
    pass


class ValidationError(PersonalityError):
    """数据验证异常"""
    pass


class PersonalityProfileError(PersonalityError):
    """人格画像异常"""
    pass


class EvidenceError(PersonalityError):
    """人格证据异常"""
    pass