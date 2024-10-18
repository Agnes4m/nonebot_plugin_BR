import random
from typing import Optional, cast

from nonebot.log import logger

from .model import GameData, StateDecide


class Weapon:

    @classmethod
    async def use_knife(cls, game_data: GameData) -> GameData:
        game_data["one_choice"]["damage"] = 2
        return game_data

    @classmethod
    async def use_handcuffs(cls, game_data: GameData) -> GameData:
        game_data["one_choice"]["skip"] = True
        return game_data

    @classmethod
    async def use_cigarettes(cls, game_data: GameData) -> GameData:
        if game_data["round_self"]:
            game_data["lives"] += 1
        else:
            game_data["enemy_lives"] += 1
        return game_data

    @classmethod
    async def use_glass(cls, game_data: GameData):
        return game_data, game_data["weapon_if"][0]

    @classmethod
    async def new_item(
        cls,
        game_data: GameData,
        out_data: Optional[StateDecide] = None,
    ):
        """生成新道具"""
        if out_data is None:
            out_data = cast(
                StateDecide,
                {
                    "msg": "",
                    "is_finish": False,
                    "bullet": False,
                    "weapon": 0,
                },
            )
        self_weapon = sum(
            int(value)
            for value in game_data["items"].values()
            if isinstance(value, (int, float))
        )
        enemy_weapon = sum(
            int(value)
            for value in game_data["eneny_items"].values()
            if isinstance(value, (int, float))
        )

        # 计算可交换的道具数量
        weapon_number_max = max(8 - self_weapon, 8 - enemy_weapon)
        swap_number = random.randint(1, max(4, weapon_number_max))

        # out_data["weapon"] = swap_number
        # out_data["msg"] += f"\n🔫剩余子弹: {game_data['weapon_all']}"

        # 生成新道具
        swap_number = random.randint(0, 4)

        out_data["weapon"] = swap_number
        out_data["msg"] += f"\n🔫剩余子弹: {game_data['weapon_all']}"

        # 生成新的道具
        available_weapons = ["knife", "handcuffs", "cigarettes", "glass", "drink"]

        for _ in range(swap_number):
            # 随机选择一个道具
            weapon_key = random.choice(available_weapons)

            # 检查并初始化道具数量
            if weapon_key not in game_data["items"]:
                game_data["items"][weapon_key] = 0
            game_data["items"][weapon_key] += 1

        new_weapon2 = [random.randint(1, 5) for _ in range(swap_number)]
        for index in new_weapon2:
            weapon_key = f"weapon{index + 1}"
            # 检查并初始化敌方道具数量
            if weapon_key not in game_data["eneny_items"]:
                game_data["eneny_items"][weapon_key] = 0
            game_data["eneny_items"][weapon_key] += 1
        logger.info(f"[br]道具生成,{new_weapon1}{new_weapon2}")
        return game_data, out_data, new_weapon1, new_weapon2
