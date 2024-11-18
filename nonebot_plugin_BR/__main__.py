from pathlib import Path
from typing import cast

from nonebot import on_command
from nonebot.adapters import Event, Message
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot_plugin_session import EventSession, SessionIdType
from nonebot_plugin_uninfo import Session, UniSession
from nonebot_plugin_waiter import prompt

from .config import config
from .game import Game, LocalData
from .model import GameData, PlayerSession
from .utils import Format
from .weapon import Weapon

game_players = cast(list[PlayerSession], [])

br_help = on_command(
    "br help",
    aliases={"BR HELP", "Br Help", "br帮助"},
    priority=2,
    block=True,
)


@br_help.handle()
async def _(matcher: Matcher):
    await matcher.finish(
        """游戏指令
- br开始/br加入/br准备 —— 开始游戏
- br设置血量 —— 设置血量
- 开枪 —— 开枪
- 使用道具 xxx —— 使用道具
- 结束游戏 —— 结束游戏""",
    )


br_start = on_command(
    "br开始",
    aliases={"br加入", "br进入", "br准备"},
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
                f"""玩家 {session_id.user.nick or session_id.user.name} 加入游戏,游戏开始.
第一枪前发送“br设置血量”可修改双方的血量
请先手发送“开枪”来执行游戏操作""",
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
            f"玩家 {session_id.user.name} 发起了恶魔轮盘游戏!\n请等待另外一个用户加入游戏",
        )
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
    game_data = cast(GameData, game_data)


async def game_rule(event: Event, session: EventSession):  # noqa: RUF029
    # logger.info(game_players)
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
    player_id = event.get_user_id()
    session_uid = session.get_id(SessionIdType.GROUP)
    game_data = await LocalData.read_data(session_uid)

    if not game_data["player_id2"]:
        await matcher.finish("你还没有对手呢,快艾特你的好朋友发送“br加入”进入游戏吧")

    # 首次攻击判定
    if not game_data["is_start"]:
        logger.info("[br]开始游戏,先手为player1")
        game_data, _, new_weapon1, new_weapon2 = await Weapon.new_item(game_data)

        out_msg = f"""
道具新增:
{game_data["player_name"]}: {await Format.creat_item(new_weapon1)}
{game_data["player_name2"]}: {await Format.creat_item(new_weapon2)}
"""
        if player_id == game_data["player_id2"]:
            out_msg += f"\n{game_data['player_name2']}发动偷袭,开始游戏"
        else:
            out_msg += f"{game_data['player_name']}发动偷袭,开始游戏"
        await matcher.send(out_msg)
        if player_id == game_data["player_id2"]:
            game_data["player_id"], game_data["player_id2"] = (
                game_data["player_id2"],
                game_data["player_id"],
            )
            game_data["player_name"], game_data["player_name2"] = (
                game_data["player_name2"],
                game_data["player_name"],
            )

        await LocalData.save_data(session_uid, game_data)

    if not game_data["is_start"]:
        game_data["is_start"] = True
    # 判断是否是自己回合
    logger.info(game_data["round_self"])
    logger.info(player_id == game_data["player_id2"])
    if game_data["round_self"] and player_id == game_data["player_id2"]:
        await matcher.finish(f"现在是{game_data['player_name']}的回合\n请等待对手行动")
    if not game_data["round_self"] and player_id == game_data["player_id"]:
        await matcher.finish(f"现在是{game_data['player_name2']}的回合\n请等待对手行动")

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

    # 判断枪有没有子弹
    if_reload, out_msg = await Game.check_weapon(game_data, session_uid)
    if if_reload:
        await matcher.send(out_msg)
    if obj == "2":
        game_data, out_msg = await Game.start(game_data, True)  # noqa: FBT003
    else:
        game_data, out_msg = await Game.start(game_data, False)  # noqa: FBT003
    await matcher.send(out_msg)
    await LocalData.save_data(session_uid, game_data)

    # 状态判定
    state_data = await Game.state(game_data, session_uid)
    out_msg = state_data["msg"]

    if state_data["is_finish"]:
        # 游戏结束
        await LocalData.delete_data(session_uid)
        await matcher.finish(out_msg)

    await LocalData.save_data(session_uid, game_data)
    await matcher.finish(out_msg)


swich_life = on_command("br设置血量", rule=game_rule)


@swich_life.handle()
async def _(
    ev: Event,
    matcher: Matcher,
    session: EventSession,
    args: Message = CommandArg(),
):
    logger.info("[br]正在设置血量指令")
    player_id = ev.get_user_id()
    session_uid = session.get_id(SessionIdType.GROUP)
    game_data = await LocalData.read_data(session_uid)
    if player_id != game_data["player_id"] and player_id != game_data["player_id2"]:
        await matcher.finish("你不是游戏中的玩家")
    if game_data["is_start"]:
        await matcher.finish("游戏已开始,请勿修改血量")
    lives = args.extract_plain_text()
    if not lives.isdigit():
        await matcher.finish("血量必须为数字")
    lives = int(lives)
    if lives < 0 or lives > 8:
        await matcher.finish("血量范围为1-8")
    await LocalData.switch_life(game_data, session_uid, lives)
    logger.info(f"[br]血量已设置为{lives}")
    await matcher.finish(f"血量已设置为{lives}")


use_itme = on_command("使用", rule=game_rule)


@use_itme.handle()
async def _(
    matcher: Matcher,
    session: EventSession,
    args: Message = CommandArg(),
):
    logger.info("[br]正在使用道具指令")
    txt = args.extract_plain_text().strip()
    game_data = await LocalData.read_data(session.get_id(SessionIdType.GROUP))
    if game_data["round_self"]:
        if "刀" in txt:
            if game_data["items"]["knife"] <= 0:
                await matcher.finish("你没有刀")
            game_data = await Weapon.use_knife(game_data)
            game_data["items"]["knife"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            await matcher.finish("刀已使用,你下一次攻击伤害为2(无论是否有子弹)")
        if "手铐" in txt:
            if game_data["items"]["handcuffs"] <= 0:
                await matcher.finish("你没有手铐")
            game_data = await Weapon.use_handcuffs(game_data)
            game_data["items"]["handcuffs"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            await matcher.finish("手铐已使用, 跳过对方一回合")
        if "香烟" in txt:
            if game_data["items"]["cigarettes"] <= 0:
                await matcher.finish("你没有香烟")
            game_data = await Weapon.use_cigarettes(game_data)
            game_data["items"]["cigarettes"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            await matcher.finish("香烟已使用, 血量加1")
        if "放大镜" in txt:
            if game_data["items"]["glass"] <= 0:
                await matcher.finish("你没有放大镜")
            game_data, msg = await Weapon.use_glass(game_data)
            game_data["items"]["glass"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            if msg:
                await matcher.finish("放大镜已使用,是实弹")
            if not msg:
                await matcher.finish("放大镜已使用,是空弹")
        if "饮料" in txt:
            if game_data["items"]["drink"] <= 0:
                await matcher.finish("你没有饮料")
            game_data = await Weapon.use_drink(game_data)
            game_data["items"]["drink"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            await matcher.finish("饮料已使用,退弹一发")
        else:
            await matcher.finish("无效道具")
    else:
        if "刀" in txt:
            if game_data["eneny_items"]["knife"] <= 0:
                await matcher.finish("你没有刀")
            game_data = await Weapon.use_knife(game_data)
            game_data["eneny_items"]["knife"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)

            await matcher.finish("刀已使用,你下一次攻击伤害为2(无论是否有子弹)")
        if "手铐" in txt:
            if game_data["eneny_items"]["handcuffs"] <= 0:
                await matcher.finish("你没有手铐")
            game_data = await Weapon.use_handcuffs(game_data)
            game_data["eneny_items"]["handcuffs"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            await matcher.finish("手铐已使用, 跳过对方一回合")
        if "香烟" in txt:
            if game_data["eneny_items"]["cigarettes"] <= 0:
                await matcher.finish("你没有香烟")
            game_data = await Weapon.use_cigarettes(game_data)
            game_data["eneny_items"]["cigarettes"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            await matcher.finish("香烟已使用, 血量加1")
        if "放大镜" in txt:
            if game_data["eneny_items"]["glass"] <= 0:
                await matcher.finish("你没有放大镜")
            game_data, msg = await Weapon.use_glass(game_data)
            game_data["eneny_items"]["glass"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            if msg:
                await matcher.finish("放大镜已使用,是实弹")
            if not msg:
                await matcher.finish("放大镜已使用,是空弹")
        if "饮料" in txt:
            if game_data["eneny_items"]["drink"] <= 0:
                await matcher.finish("你没有饮料")
            game_data = await Weapon.use_drink(game_data)
            game_data["eneny_items"]["drink"] -= 1
            await LocalData.save_data(session.get_id(SessionIdType.GROUP), game_data)
            await matcher.finish("饮料已使用,退弹一发")
        await matcher.finish("无效道具")


search_game = on_command("br当前状态", rule=game_rule)


@search_game.handle()
async def _(
    ev: Event,
    matcher: Matcher,
    session: EventSession,
):
    logger.info("[br]正在查询游戏状态指令")
    player_id = ev.get_user_id()
    session_uid = session.get_id(SessionIdType.GROUP)
    game_data = await LocalData.read_data(session_uid)
    if player_id != game_data["player_id"] and player_id != game_data["player_id2"]:
        await matcher.finish("你不是游戏中的玩家")
    out_msg = await Game.state(game_data, session_uid)
    await matcher.finish(out_msg["msg"])


game_end = on_command("结束游戏", rule=game_rule)
game_super = on_command("结束游戏", permission=SUPERUSER)


@game_super.handle()
@game_end.handle()
async def _(
    matcher: Matcher,
    session: EventSession,
):
    logger.info("[br]正在结束游戏指令")
    # player_id = ev.get_user_id()
    session_uid = session.get_id(SessionIdType.GROUP)
    # game_data = await LocalData.read_data(session_uid)

    # 结束游戏并清理玩家
    game_players[:] = [one for one in game_players if one["session_uid"] != session_uid]
    await LocalData.delete_data(session_uid)
    await matcher.finish("恶魔轮盘已游戏结束")
