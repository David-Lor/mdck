# mdadm check & repair tool

mdck is a Python app that checks and repairs mdadm arrays.

## Running

### Requirements

- Updated Python 3 (tested with Python 3.10)
- [required packages](requirements.txt)

### Running

```bash
MDADM_DEVICE=md0 python .
```

#### Callback execution

mdck can run a callback script for each status update (including the percentage completion).
The relevant update data is passed as the first call argument, in JSON format.

Example:

```bash
#!/bin/bash

# Location: "callback.sh" in current directory.
# This will log each received update in a "mdck.log" file.

echo "[$(date)] $1" >> mdck.log
```

```bash
MDADM_DEVICE=md0 MDADM_UPDATES_CALLBACK_PATH=callback.sh python .
```

## Changelog

- 0.0.1
  - Initial release: check & repair, callback script execution
