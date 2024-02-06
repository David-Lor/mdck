import sys

from .steps import check_start, check_follow, get_mismatch, repair_start, repair_follow
from .settings import settings


def main():
    if settings.check:
        if not check_start(settings.device):
            sys.exit(1)
        if not check_follow(settings.device):
            sys.exit(1)

    ok, mismatch_count = get_mismatch(settings.device)
    if not ok:
        sys.exit(1)

    if settings.repair and mismatch_count > settings.repair_mismatch_threshold:
        if not repair_start(settings.device):
            sys.exit(1)
        if not repair_follow(settings.device):
            sys.exit(1)

    if settings.check_after_repair:
        main()
