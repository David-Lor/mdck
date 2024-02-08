from .models import MdadmStates, MdadmActions
from .callback import Update, State, trigger_callback
from .utils import mdadm_get_detail, mdadm_set_sync_action, mdadm_get_mismatch_count, mdadm_follow_percentage


def check_start(device: str) -> bool:
    status = mdadm_get_detail(device)
    if status.is_checking():
        print("Currently checking")
        return True
    if status.is_resyncing():
        print("Currently resyncing")
        return True

    return mdadm_set_sync_action(device, MdadmActions.Check)


def check_follow(device: str) -> bool:
    ok = mdadm_follow_percentage(device, MdadmStates.Checking)
    if not ok:
        trigger_callback(Update(
            state=State.Checking,
            device=device,
            error=True,
        ))

    return ok


def get_mismatch(device: str) -> tuple[bool, int]:
    ok, mismatch_count = mdadm_get_mismatch_count(device)
    if not ok:
        return False, -1

    print("Mismatch count:", mismatch_count)
    return True, mismatch_count


def repair_start(device: str) -> bool:
    status = mdadm_get_detail(device)
    if status.is_resyncing():
        print("Currently resyncing!")
        return True

    ok = mdadm_set_sync_action(device, MdadmActions.Repair)
    trigger_callback(Update(
        state=State.Resyncing,
        device=device,
        error=not ok,
    ))
    return ok


def repair_follow(device: str) -> bool:
    ok = mdadm_follow_percentage(device, MdadmStates.Resyncing)
    if not ok:
        trigger_callback(Update(
            state=State.Resyncing,
            device=device,
            error=True,
        ))

    return ok
