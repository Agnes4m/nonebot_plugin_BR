import json
import random
from pathlib import Path
from typing import cast

from nonebot import on_command
from nonebot.adapters import Event
from nonebot.matcher import Matcher

# from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot_plugin_uninfo import Session, UniSession

from .config import config
from .model import GameData

br_start = on_command(
    "br",
    aliases={"BR", "恶魔轮盘赌", "恶魔轮盘"},
    priority=2,
    block=True,
)


@br_start.handle()
async def _(
    ev: Event,
    matcher: Matcher,
    state: T_State,
    session: Session = UniSession(),
    # args: Message = CommandArg(),
):
    # 判断是否有在玩的游戏
    game_id = ev.get_session_id()
    data_path = Path(config.br_path) / "player" / f"{game_id}.json"
    if data_path.is_file():
        with data_path.open("r", encoding="utf-8") as f:
            game_data = json.load(f)
        await matcher.send("检测到在进行的游戏，游戏继续！")  # noqa: RUF001
    else:
        # 创建新的游戏
        weapon_size = random.randint(2, 8)
        game_data = {
            "game_id": game_id,
            "player_name": (session.user.nick or session.user.name),
            "round_num": 1,
            "round_self": True,
            "lives": 3,
            "enemy_lives": 6,
            "weapon_all": weapon_size,
            "weapon_if": [random.choice([True, False]) for _ in range(weapon_size)],
            "items": {
                "knife": 0,
                "handcuffs": 0,
                "cigarettes": 0,
                "glass": 0,
                "drink": 0,
            },
        }

        await matcher.send("恶魔轮盘赌开始！发送“准备”开始游戏！")  # noqa: RUF001

    game_data = cast(GameData, game_data)
    state["game_data"] = game_data


@br_start.got("准备", prompt="准备开始游戏！")  # noqa: RUF001
async def _():
    pass
