from typing import List, TypedDict


class Items(TypedDict):
    """所有道具"""

    knife: int
    """刀"""
    handcuffs: int
    """手铐"""
    cigarettes: int
    """香烟"""
    glass: int
    """放大镜"""
    drink: int
    """饮料"""


class Choices(TypedDict):
    """所有选项"""

    damage: int
    """当前伤害"""
    skip: bool


class GameData(TypedDict):
    """总数据"""

    game_id: str
    player_name: str
    """玩家名称"""
    round_num: int
    """当前行动回合"""
    round_self: bool
    """是否是自己行动"""
    lives: int
    """当前剩余生命值"""
    enemy_lives: int
    """敌人剩余生命值"""
    weapon_all: int
    """武器总子弹数量"""
    weapon_if: List[bool]
    """武器子弹是否可用"""
    items: Items
    """所有道具"""
    one_choice: Choices
