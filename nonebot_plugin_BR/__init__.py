from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_uninfo")
# require("nonebot_plugin_alconna")
require("nonebot_plugin_waiter")
require("nonebot_plugin_session")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.0.3"
__plugin_meta__ = PluginMetadata(
    name="恶魔轮盘赌",
    description="与机器人交互实现恶魔轮盘赌规则",
    usage="br help呼出帮助",
    type="application",
    config=ConfigModel,
    homepage="https://github.com/Agnes4m/nonebot_plugin_BR",
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_uninfo",
        "nonebot_plugin_session",
    ),
    extra={
        "version": __version__,
        "author": "Agnes4m <Z735803792@163.com>",
    },
)
