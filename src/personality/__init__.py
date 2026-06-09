"""
人格系统模块
"""

from .profile import PersonalityProfile
from .big_five import BigFiveProfile
from .enneagram import EnneagramProfile

__all__ = [
    "PersonalityProfile",
    "BigFiveProfile",
    "EnneagramProfile",
]