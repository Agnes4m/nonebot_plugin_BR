from .model import GameData


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
