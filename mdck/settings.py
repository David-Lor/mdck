import pathlib
from typing import Optional

import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    device: str
    check: bool = True
    repair: bool = True
    check_after_repair: bool = True
    repair_mismatch_threshold: int = 0
    watch_sleep: float = 2
    updates_callback_path: Optional[pathlib.Path] = None

    class Config:
        env_prefix = "MDADM_"


settings = Settings()
