import sys

from .steps import check_start, check_follow, get_mismatch, repair_start, repair_follow
from .callback import Update, State, trigger_callback
from .settings import settings


def main():
    if settings.check:
        if not check_start(settings.device):
            sys.exit(1)
        if not check_follow(settings.device):
            sys.exit(1)

    ok, mismatch_count = get_mismatch(settings.device)
    if not ok:
        trigger_callback(Update(
            device=settings.device,
            state=State.CheckEnd,
            error=True,
        ))
        sys.exit(1)

    trigger_callback(Update(
        device=settings.device,
        state=State.CheckEnd,
        mismatch_count=mismatch_count,
    ))

    if mismatch_count <= settings.repair_mismatch_threshold:
        sys.exit(0)

    if settings.repair:
        if not repair_start(settings.device):
            sys.exit(1)
        if not repair_follow(settings.device):
            sys.exit(1)

        if settings.check_after_repair:
            main()
