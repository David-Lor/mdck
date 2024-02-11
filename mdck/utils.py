import time
import subprocess

import jc

from .models import MdadmOutput, MdadmStates
from .callback import Update, State, trigger_callback
from .settings import settings


def mdadm_exec(device: str, *args) -> MdadmOutput:
    cmd = ["mdadm", *args, f"/dev/{device}"]
    output = subprocess.check_output(cmd)

    output_dict = jc.parse("mdadm", output.decode())
    return MdadmOutput.model_validate(output_dict)


def mdadm_get_detail(device: str) -> MdadmOutput:
    return mdadm_exec(device, "--detail")


def mdadm_set_sync_action(device: str, action: str) -> bool:
    if not write(f"/sys/block/{device}/md/sync_action", action):
        print("KO set sync_action to", action)
        return False

    return True


def mdadm_get_mismatch_count(device: str) -> tuple[bool, int]:
    ok, value = read(f"/sys/block/{device}/md/mismatch_cnt")
    if not ok:
        print("KO read mismatch_cnt")
        return False, 0
    if not value.isnumeric():
        print("KO read mismatch_cnt (value not numeric)")
        return False, 0

    return True, int(value)


def mdadm_follow_percentage(device: str, state: str) -> bool:
    last_percentage = -1
    while True:
        status = mdadm_get_detail(device)
        if state == MdadmStates.Checking:
            current_percentage = status.check_status_percentage
        elif state == MdadmStates.Resyncing:
            current_percentage = status.resync_status_percentage
        else:
            print("mdadm_follow_percentage: invalid state")
            return False

        if current_percentage is None:
            return True

        if current_percentage != last_percentage:
            last_percentage = current_percentage
            print(state.capitalize(), current_percentage, "%")
            trigger_callback(Update(
                state=State.Checking if state == MdadmStates.Checking else State.Resyncing,
                device=device,
                percentage=last_percentage,
            ))

        time.sleep(settings.watch_sleep)


def write(path: str, content: str):
    try:
        with open(path, "w") as f:
            f.write(content)
            return True

    except Exception as ex:
        print("Error:", ex)
        return False


def read(path: str) -> tuple[bool, str]:
    try:
        with open(path, "r") as f:
            return True, f.read().strip()

    except Exception as ex:
        print("Error:", ex)
        return False, ""
