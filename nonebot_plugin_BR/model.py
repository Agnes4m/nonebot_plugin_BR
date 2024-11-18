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
    skip: int
    """默认0,1则跳过玩家1回合,2跳过玩家2一回合"""


class GameData(TypedDict):
    """总数据"""

    is_start: bool
    player_id: str
    player_id2: str
    player_name: str
    player_name2: str
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
    eneny_items: Items
    """敌人所有道具"""
    one_choice: Choices


class StateDecide(TypedDict):
    """状态决策"""

    msg: str
    """输出信息"""
    is_finish: bool
    """是否结束游戏"""
    bullet: bool
    """是否换子弹"""
    weapon: int
    """新增道具数量"""


class PlayerSession(TypedDict):
    """玩家会话"""

    player_id: str
    player_name: str
    session_uid: str
