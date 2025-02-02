import random

from .action import Action


def ai_action(game_state):
    """
    根据当前游戏状态，决定 AI 的行动。

    Returns:
        一个字符串，表示 AI 的行动，格式为 "行动类型 参数"，
        例如 "使用 刀" 或 "开枪 1"。
    """

    # 随机选择行动类型
    action_type = random.choice(["使用", "开枪"])

    if action_type == "使用":
        # 随机选择可用的道具
        available_items = [
            item
            for item in game_state["eneny_items"]
            if game_state["eneny_items"][item] > 0
        ]
        if available_items:
            item = random.choice(available_items)
            return Action("使用", item)
        else:
            # 没有可用道具，随机选择开枪目标
            target = random.choice([1, 2])
            return Action("开枪", target)
    else:
        # 随机选择开枪目标
        target = random.choice([1, 2])
        return Action("开枪", target)
