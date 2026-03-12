"""Shared infrastructure for OpenClaw skills"""
from .skill_base import SkillBase
from .config_manager import ConfigManager, config
from .response_formatter import ResponseFormatter

__all__ = ['SkillBase', 'ConfigManager', 'config', 'ResponseFormatter']
