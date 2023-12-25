import sys

from .steps import check_start, check_follow, get_mismatch, repair_start, repair_follow
from .utils import mdadm_get_detail
from .settings import settings


def main():
    if settings.check and not mdadm_get_detail(settings.device).is_resyncing():
        if not check_start(settings.device):
            sys.exit(1)
        if not check_follow(settings.device):
            sys.exit(1)

    ok, mismatch_count = get_mismatch(settings.device)
    if not ok:
        sys.exit(1)

    if settings.repair and (mismatch_count > settings.repair_mismatch_threshold or mdadm_get_detail(settings.device).is_resyncing()):
        if not repair_start(settings.device):
            sys.exit(1)
        if not repair_follow(settings.device):
            sys.exit(1)
