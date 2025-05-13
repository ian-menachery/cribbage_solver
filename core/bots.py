from core.player import Player
from core.value_player import ValuePlayer
from core.rl_player import RLPlayer

def get_bot(bot_name: str):
    name = bot_name.lower()
    if name == "random":
        return Player("RandomBot")
    elif name == "value":
        return ValuePlayer("ValueBot")
    elif name == "rl":
        return RLPlayer("RLBot", model_path="models/discard_dqn_agent.zip")
    else:
        raise ValueError(f"Unknown bot type: {bot_name}") 