from nonebot.plugin import PluginMetadata, inherit_supported_adapters

from __main__ import br_help, br_start  # noqa: F401

from .config import ConfigModel

__version__ = "0.0.1"
__plugin_meta__ = PluginMetadata(
    name="恶魔轮盘赌",
    description="与机器人交互实现恶魔轮盘赌规则",
    usage="br help呼出帮助",
    type="application",
    config=ConfigModel,
    homepage="https://github.com/Agnes4m/nonebot_plugin_BR",
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "version": __version__,
        "author": "Agnes4m <Z735803792@163.com>",
    },
)
