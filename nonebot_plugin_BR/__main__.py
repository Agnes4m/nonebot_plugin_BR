from pathlib import Path
from typing import cast

from nonebot import on_command
from nonebot.adapters import Event, Message
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot_plugin_session import EventSession, SessionIdType
from nonebot_plugin_uninfo import Session, UniSession
from nonebot_plugin_waiter import prompt

from .config import config
from .game import Game, LocalData
from .model import GameData, PlayerSession

game_players = cast(list[PlayerSession], [])

br_help = on_command(
    "br help",
    aliases={"BR HELP", "Br Help", "br帮助"},
    priority=2,
    block=True,
)


@br_help.handle()
async def _(matcher: Matcher):
    await matcher.finish("to do")


br_start = on_command(
    "br开始",
    aliases={"br加入", "br进入"},
    priority=2,
    block=True,
)


@br_start.handle()
async def _(
    ev: Event,
    matcher: Matcher,
    session: EventSession,
    session_id: Session = UniSession(),
    # args: Message = CommandArg(),
):
    # 判断是否有在玩的游戏
    session_uid = session.get_id(SessionIdType.GROUP)
    player_id = ev.get_user_id()

    data_path = Path(config.br_path) / "player" / f"{session_uid}.json"

    if data_path.is_file():
        # 检查玩家数量
        game_data = await LocalData.read_data(session_uid)
        if game_data["player_id2"]:
            # 当前会话满人
            if player_id in [game_data["player_id"], game_data["player_id2"]]:
                await matcher.send("检测到在进行的游戏,游戏继续!")
                game_players.append(
                    cast(
                        PlayerSession,
                        {
                            "player_id": player_id,
                            "player_name": session_id.user.nick or session_id.user.name,
                            "session_uid": session_uid,
                        },
                    ),
                )
            else:
                await matcher.finish("本群游戏玩家已满了呢.")
        else:
            # 只有一个人
            await matcher.send(
                f"玩家 {session_id.user.nick or session_id.user.name} 加入游戏, 游戏开始.\n请发送“开枪”来执行游戏操作",
            )
            game_data["player_id2"] = player_id
            game_data["player_name2"] = session_id.user.nick or session_id.user.name
            await LocalData.save_data(session_uid, game_data)
            game_players.append(
                cast(
                    PlayerSession,
                    {
                        "player_id": player_id,
                        "player_name": session_id.user.nick or session_id.user.name,
                        "session_uid": session_uid,
                    },
                ),
            )

    else:
        # 创建新的游戏
        (Path(config.br_path) / "player").mkdir(parents=True, exist_ok=True)
        game_data = await LocalData.new_data(player_id, session_id)
        await LocalData.save_data(session_uid, game_data)
        await matcher.send(
            f"玩家 {session_id.user.name} 发起了恶魔轮盘赌游戏!\n请等待另外一个用户加入游戏",
        )

    game_data = cast(GameData, game_data)


async def game_rule(event: Event, session: EventSession):  # noqa: RUF029
    for one in game_players:
        if (
            event.get_user_id() == one["player_id"]
            and session.get_id(SessionIdType.GROUP) == one["session_uid"]
        ):
            return True
    return False


game_shut = on_command("开枪", rule=game_rule)


@game_shut.handle()
async def _(
    event: Event,
    matcher: Matcher,
    session: EventSession,
    args: Message = CommandArg(),
):
    logger.info("[br]正在执行开枪指令")
    player_id = event.get_session_id()
    session_uid = session.get_id(SessionIdType.GROUP)
    game_data = await LocalData.read_data(session_uid)

    if not game_data["player_id2"]:
        await matcher.finish("你还没有对手呢,快艾特你的好朋友发送“br加入”进入游戏吧")

    # 首次攻击判定
    if not game_data["is_start"]:
        await matcher.send(f"{game_data['player_name']}发动偷袭,开始游戏")
        if player_id == game_data["player_id2"]:
            game_data["player_id"], game_data["player_id2"] = (
                game_data["player_id2"],
                game_data["player_id"],
            )
        game_data["is_start"] = True
        await LocalData.save_data(session_uid, game_data)
    # 判断是否是自己回合
    if game_data["round_self"] and player_id == game_data["player_id2"]:
        await matcher.finish(f"现在是{game_data['player_name']}的回合")
    if not game_data["round_self"] and player_id == game_data["player_id"]:
        await matcher.finish(f"现在是{game_data['player_name2']}的回合")

    if args.extract_plain_text() not in ["1", "2"]:
        resp = await prompt("请输入攻击目标,1为对方,2为自己", timeout=120)

        if resp is None:
            await matcher.send("等待超时")
            return
        if resp.extract_plain_text() not in ["1", "2"]:
            await matcher.send("无效输入")
            return
        obj = resp.extract_plain_text()
    else:
        obj = args.extract_plain_text()
    obj = obj.strip()
    logger.info(f"[br]正在执行开枪指令,对象为:{obj}")

    if obj == "2":
        game_data, out_msg = await Game.start(game_data, True)  # noqa: FBT003
    else:
        game_data, out_msg = await Game.start(game_data, False)  # noqa: FBT003
    await matcher.send(out_msg)
    await LocalData.save_data(session_uid, game_data)

    # 状态判定
    state_data = await Game.state(game_data)
    out_msg = state_data["msg"]
    out_msg += f"""
    自己:
    刀{game_data["items"]["knife"]}, 手铐{game_data["items"]["handcuffs"]}, 香烟{game_data["items"]["cigarettes"]}, 放大镜{game_data["items"]["glass"]}, 饮料{game_data["items"]["drink"]}
    敌人:
    刀{game_data["eneny_items"]["knife"]}, 手铐{game_data["eneny_items"]["handcuffs"]}, 香烟{game_data["eneny_items"]["cigarettes"]}, 放大镜{game_data["eneny_items"]["glass"]}, 饮料{game_data["eneny_items"]["drink"]}
    """

    if state_data["is_finish"]:
        # 游戏结束
        await LocalData.delete_data(session_uid)
        await matcher.finish(out_msg)

    await LocalData.save_data(player_id, game_data)
    await matcher.finish(out_msg)
