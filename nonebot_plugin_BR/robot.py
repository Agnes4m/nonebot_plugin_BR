import json
import os
import random

import google.generativeai as genai
from nonebot import logger

from .action import Action
from .config import config
from .model import GameData

key = config.key
prompt = config.prompt
HTTP_PROXY = config.http_proxy
HTTPS_PROXY = config.https_proxy
model_name = config.model_name

logger.debug(f"prompt: {prompt}")
logger.debug(f"HTTP_PROXY: {HTTP_PROXY}")
logger.debug(f"HTTPS_PROXY: {HTTPS_PROXY}")
logger.debug(f"model_name: {model_name}")
if HTTP_PROXY == "" and HTTPS_PROXY == "":
    logger.warning("没有设置代理！gemini api可能不可用，如报错不支持的地区请设置代理！")
else:
    # 设置代理
    os.environ["HTTP_PROXY"] = HTTP_PROXY
    os.environ["HTTPS_PROXY"] = HTTPS_PROXY
if key != "":
    genai.configure(api_key=key)
    if model_name != "":
        gemini = genai.GenerativeModel(model_name)
    else:
        gemini = genai.GenerativeModel("gemini-2.0-flash-exp")
    if prompt == "":
        prompt: str = """
      你现在扮演一个轮盘赌游戏的AI决策者，与玩家进行对战。
游戏开始时，枪内随机装入数量不定的子弹，包含随机数量的实弹和空包弹（极端情况可能全是实弹或空弹）。子弹的具体装填方式是随机的，你无法得知每一颗子弹的具体位置。
每回合你必须做出决策：
使用道具（一次只能使用一种。且有数量限制）：
刀：使你的下次攻击伤害翻倍。
香烟：恢复一点生命值。
手铐：使对手跳过下一回合。
饮料：从枪中退出一发子弹。
放大镜：查看下一发子弹是否为实弹。如果你使用了，则会告知你结果。
开枪：选择对敌人（1）或自己（2）开枪。如果对自己开枪是空包弹则不扣血并额外获得一回合。
请根据当前游戏局势做出最优决策。你的目标是提取胜，请严格按照给定格式返回！不要出现任何其它文本，
尤其是不要出现：
```json
或者
```
只允许返回：
{"action": "{open_gun或者use}","argument": "{道具名称}","gemini的分析": "{你的分析}"}
"""


async def ai_action(game_data: GameData, game_state, is_live_ammunition):
    """
            AI 的行动。
    Returns:
                    Action
    """
    if key == "":
        action = random_action(game_data)
    else:
        action = await gemini_do(game_data, game_state, is_live_ammunition)
    return action


def random_action(game_data):
    # 随机选择行动类型
    action_type = random.choice(["使用", "开枪"])

    if action_type == "使用":
        # 随机选择可用的道具
        available_items = [
            item
            for item in game_data["eneny_items"]
            if game_data["eneny_items"][item] > 0
        ]
        if available_items:
            item = random.choice(available_items)
            return Action("使用", item)
        # 没有可用道具,随机选择开枪目标
        target = random.choice([1, 2])
        return Action("开枪", str(target))
    # 随机选择开枪目标
    target = random.choice([1, 2])
    return Action("开枪", str(target))


async def gemini_do(game_data, game_state, is_live_ammunition):
    global prompt
    global gemini
    prompt_temp = prompt + game_state["msg"]
    if is_live_ammunition is not -1:
        if is_live_ammunition == 1:
            prompt_temp += "你刚刚使用了放大镜，下一发是实弹"
        elif is_live_ammunition == 0:
            prompt_temp += "你刚刚使用了放大镜，下一发是空包弹"
        elif is_live_ammunition == 2:
            prompt_temp += "手铐已使用跳过对手一回合"
    try:
        logger.debug(f"prompt_temp: {prompt_temp}")
        response = gemini.generate_content(prompt_temp)
        logger.debug("gemini 返回内容" + response.text)
    except Exception:
        logger.exception("调用 Gemini API 出错")  # 记录详细的异常信息
        return random_action(game_data)

    try:
        decision = json.loads(response.text)  # 使用 json.loads() 解析 JSON 字符串
        action_type = decision["action"]
        argument = decision["argument"]

        if action_type == "open_gun":
            return Action("开枪", argument)  # 直接创建 Action 对象
        elif action_type == "use":
            return Action("使用", argument)  # 直接创建 Action 对象
        else:
            logger.warning(f"未知的行动类型: {action_type}")
            return random_action(game_data)

    except (json.JSONDecodeError, KeyError) as e:  # 捕获 JSON 解码错误和键错误
        logger.error(f"解析 Gemini 返回的文本出错: {e}")
        return random_action(game_data)
    except Exception as e:  # 捕获其他异常
        logger.exception(f"处理 Gemini 返回的文本时出错: {e}")
        return random_action(game_data)
