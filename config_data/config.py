from dataclasses import dataclass
from typing import Union
from environs import Env 


@dataclass
class TgBot:
    token: str

@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: Union[str, None] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
        
        )
    )
    
