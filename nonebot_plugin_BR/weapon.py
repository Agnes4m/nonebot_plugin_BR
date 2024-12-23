import random
from typing import List, Optional, cast

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
    async def use_drink(cls, game_data: GameData):
        game_data["weapon_if"].pop(0)
        game_data["weapon_all"] -= 1
        return game_data

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

        # 生成新道具
        swap_number = random.randint(0, 4)

        available_weapons = ["knife", "handcuffs", "cigarettes", "glass", "drink"]
        weapon_indices = {
            weapon: index for index, weapon in enumerate(available_weapons)
        }

        # 生成玩家道具
        new_weapon1: List[int] = []
        for _ in range(swap_number):
            # 随机选择一个道具
            weapon_key = random.choice(available_weapons)
            new_weapon1.append(weapon_indices[weapon_key])

            # 检查并初始化道具数量
            if weapon_key not in game_data["items"]:
                game_data["items"][weapon_key] = 0
            game_data["items"][weapon_key] += 1

        # 生成敌方道具
        new_weapon2: List[int] = []
        for _ in range(swap_number):
            weapon_key = random.choice(available_weapons)
            new_weapon2.append(weapon_indices[weapon_key])

            # 检查并初始化敌方道具数量
            if weapon_key not in game_data["eneny_items"]:
                game_data["eneny_items"][weapon_key] = 0
            game_data["eneny_items"][weapon_key] += 1
        return game_data, out_data, new_weapon1, new_weapon2
