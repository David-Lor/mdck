from .models import MdadmStates, MdadmActions
from .utils import mdadm_get_detail, mdadm_set_sync_action, mdadm_follow_percentage


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


def check_follow(device: str):
    mdadm_follow_percentage(device, MdadmStates.Checking)
