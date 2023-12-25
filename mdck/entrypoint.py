import sys

from .steps import check_start, check_follow


def main():
    device = sys.argv[-1]

    if not check_start(device):
        sys.exit(1)

    check_follow(device)
