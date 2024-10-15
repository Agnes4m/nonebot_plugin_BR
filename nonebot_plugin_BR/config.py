from pathlib import Path

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    """基本配置"""

    br_path: str = str(Path("data/br"))
    """数据位置"""


config = get_plugin_config(ConfigModel)
