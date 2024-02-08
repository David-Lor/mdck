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
    device: str
    state: State
    error: bool = False
    mismatch_count: Optional[int] = None
    percentage: Optional[int] = None


def trigger_callback(update: Update):
    update_data = update.model_dump_json(exclude_none=True, exclude_unset=True)
    if settings.updates_callback_path:
        # noinspection PyBroadException
        try:
            subprocess.call([settings.updates_callback_path, update_data])
        except Exception as ex:
            print("Error calling callback:", ex)
