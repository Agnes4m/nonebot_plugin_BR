from pathlib import Path

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    """基本配置"""

    prompt: str = """"""
    """给gemini的提示词"""
    key: str = ""
    """gemini api key，留空即视为不使用Gemini，申请地址：https://aistudio.google.com/apikey?hl=zh-cn"""
    model_name: str = ""
    """留空就使用默认gemini-2.0-flash-exp，具体可用模型名称请访问：https://ai.google.dev/gemini-api/docs/models/gemini?hl=zh-cn#gemini-2.0-flash"""
    http_proxy: str = ""
    """http代理"""
    https_proxy: str = ""
    """https代理"""
    br_path: str = str(Path("data/br"))
    """数据位置"""


config = get_plugin_config(ConfigModel)
