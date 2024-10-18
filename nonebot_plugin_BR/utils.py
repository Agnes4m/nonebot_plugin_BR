import random
from typing import Dict

from .model import GameData, Items


class Format:
    """格式化工具"""

    @classmethod
    async def format_items_message(cls, game_data: GameData) -> str:
        """格式化道具信息为字符串"""
        player_message = f"""{game_data["player_name"]}: 
刀{game_data["items"].get("knife", 0)}, 手铐{game_data["items"].get("handcuffs", 0)}, 香烟{game_data["items"].get("cigarettes", 0)}, 放大镜{game_data["items"].get("glass", 0)}, 饮料{game_data["items"].get("drink", 0)}"""

        player2_message = f"""{game_data["player_name2"]}: 
刀{game_data["eneny_items"].get("knife", 0)}, 手铐{game_data["eneny_items"].get("handcuffs", 0)}, 香烟{game_data["eneny_items"].get("cigarettes", 0)}, 放大镜{game_data["eneny_items"].get("glass", 0)}, 饮料{game_data["eneny_items"].get("drink", 0)}"""

        return f"当前道具\n{player_message}\n{player2_message}\n"

    @classmethod
    async def generate_weapon(cls, weapon_dict: Items):
        """随机生成道具并更新道具数量"""
        available_weapons = ["knife", "handcuffs", "cigarettes", "glass", "drink"]

        # 随机生成道具数量
        num_weapons = random.randint(1, 5)

        for _ in range(num_weapons):
            # 随机选择一个道具
            weapon_key = random.choice(available_weapons)

            # 检查并初始化道具数量
            if weapon_key not in weapon_dict:
                weapon_dict[weapon_key] = 0

            weapon_dict[weapon_key] += 1
        return weapon_dict

    @classmethod
    async def creat_item(cls, new_weapon: list[int]):
        # 道具生成输出
        item_names: Dict[int, str] = {
            0: "刀",
            1: "手铐",
            2: "香烟",
            3: "放大镜",
            4: "饮料",
        }

        # 生成描述
        descriptions = []
        for index in new_weapon:
            if index in item_names:
                descriptions.append(f"{item_names[index]}1")  # 假设数量为 1

        return ",".join(descriptions)
