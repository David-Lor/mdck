from .models import MdadmStates, MdadmActions
from .utils import mdadm_get_detail, mdadm_set_sync_action, mdadm_get_mismatch_count, mdadm_follow_percentage


def check_start(device: str) -> bool:
    status = mdadm_get_detail(device)
    if not status.is_active():
        print("Not active!")
        return False
    if status.is_checking():
        print("Already checking!")
        return True

    if not mdadm_set_sync_action(device, MdadmActions.Check):
        return False

    return True


def check_follow(device: str) -> bool:
    return mdadm_follow_percentage(device, MdadmStates.Checking)


def check_mismatch(device: str) -> tuple[bool, int]:
    ok, mismatch_count = mdadm_get_mismatch_count(device)
    if not ok:
        return False, -1

    print("Mismatch count:", mismatch_count)
    return True, mismatch_count


def repair_start(device: str) -> bool:
    pass


def repair_follow(device: str) -> bool:
    pass
