import enum
import subprocess
from typing import Optional

import pydantic

from .settings import settings


class State(str, enum.Enum):
    # TODO Merge with MdadmStates
    Checking = "checking"
    CheckEnd = "check_end"
    Resyncing = "resyncing"
    ResyncEnd = "resync_end"


class Update(pydantic.BaseModel):
    state: State
    device: str
    error: bool = False
    mismatch_count: Optional[int] = None
    percentage: Optional[int] = None


def trigger_callback(update: Update):
    update_data = update.model_dump_json()
    print("Callback:", update_data)
    if settings.updates_callback_path:
        # noinspection PyBroadException
        try:
            subprocess.call([settings.updates_callback_path, update_data])
        except Exception as ex:
            print("Error calling callback:", ex)
