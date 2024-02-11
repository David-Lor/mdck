# mdadm check & repair tool

mdck is a Python app that checks and repairs mdadm arrays.

## Docker run

```bash
MDADM_DEVICE=md0
# apk add mdadm-utils
docker run --privileged -v /dev/$MDADM_DEVICE:/dev/$MDADM_DEVICE -v /sys/block/$MDADM_DEVICE/md:/sys/block/$MDADM_DEVICE/md
```
