import sys

from .steps import check_start, check_follow, check_mismatch, repair_start, repair_follow
from .utils import mdadm_get_detail


def main():
    device = sys.argv[-1]

    if not check_start(device):
        sys.exit(1)
    if not check_follow(device):
        sys.exit(1)

    ok, mismatch_count = check_mismatch(device)
    if not ok:
        sys.exit(1)

    if mismatch_count > 0 or mdadm_get_detail(device).is_resyncing():
        if not repair_start(device):
            sys.exit(1)
        if not repair_follow(device):
            sys.exit(1)
