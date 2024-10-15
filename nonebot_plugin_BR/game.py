import random
from .model import GameData

import asyncio
class Game:
    
    @classmethod
    async def start(cls, game_data: GameData, shut_self: bool):
        """开枪判定"""
        reround = False
        if game_data["round_self"]:
            msg = f"{game_data['player_name']}开枪了!"
        else:
            msg = "敌人开枪了!"
        damage = game_data["one_choice"]["damage"] if game_data["weapon_if"][0] else 0
        if shut_self:
            msg += "目标是自己。"
            if damage == 0:
                msg += "\n没有伤害。"
                reround = True
            msg += f"造成{damage}点伤害"

        else:
            msg += "目标是对方。"
            msg += f"造成{damage}点伤害"
        
        # 伤害计算
        if (game_data["round_self"] and shut_self) or (not game_data["round_self"] and not shut_self):
            game_data["lives"] -= damage
        else:
            game_data["enemy_lives"] -= damage    
            
        # 删除开枪的子弹        
        game_data["weapon_if"].pop(0)
        game_data["weapon_all"] -= 1
        return game_data, msg, reround

    @classmethod
    async def state(cls, game_data: GameData):
        """当前状态结算"""
        msg = "当前状态结算"
        
        # 判断是否死亡
        if game_data["lives"] <= 0:
            msg += f"\n{game_data['player_name']}血量为0,游戏结束"
            return msg, True
        elif game_data["enemy_lives"] <= 0:
            msg += f"\n{game_data['player_name']}你过关,"
            return msg, True
        
        # 判断当前枪支子弹
        if game_data["weapon_all"] <= 0:
            new_nub = random.randint(2, 8)
            game_data["weapon_all"] = new_nub
            game_data["weapon_if"] = [random.choice([True, False]) for _ in range(new_nub)]
            msg += f"\n子弹打完,已重置子弹\n当前子弹数: {new_nub}\n实弹数: {sum(game_data['weapon_if'])}"
        else:
            msg += f"当前子弹数: {game_data['weapon_all']}\n实弹数: {sum(game_data['weapon_if'])}"
        
        # 判断道具生成
        self_weapon = sum(int(value) for value in game_data["items"].values() if isinstance(value, (int, float)))
        enemy_weapon = sum(int(value) for value in game_data["eneny_items"].values() if isinstance(value, (int, float)))
        weapon_number_max = max(8 - self_weapon, 8 - enemy_weapon)
        swap_number = random.randint(1, max(4, weapon_number_max))
        return swap_number