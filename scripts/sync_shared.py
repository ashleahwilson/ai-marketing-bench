#!/usr/bin/env python3
"""Keep files shared between skills identical. Each skill must install on its own, so shared files are copied, not linked.

Usage:
    python3 scripts/sync_shared.py           # copy each source over its copies
    python3 scripts/sync_shared.py --check   # exit 1 if any copy differs (run before committing)
"""

import filecmp
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# source (edit this one) -> copies
SHARED = {
    "skills/brand-voice-gate/references/subtractive.md": ["skills/de-slop/references/subtractive.md"],
    "skills/brand-voice-gate/scripts/check_voice.py": ["skills/de-slop/scripts/check_voice.py"],
    "skills/brand-voice-gate/scripts/check_trace.py": ["skills/de-slop/scripts/check_trace.py"],
}


def main():
    check = "--check" in sys.argv
    stale = []
    for src, copies in SHARED.items():
        for dst in copies:
            s, d = os.path.join(ROOT, src), os.path.join(ROOT, dst)
            if os.path.isfile(d) and filecmp.cmp(s, d, shallow=False):
                continue
            if check:
                stale.append(dst)
            else:
                os.makedirs(os.path.dirname(d), exist_ok=True)
                shutil.copy(s, d)
                print(f"synced {dst}")
    if stale:
        print("out of sync (run python3 scripts/sync_shared.py):\n  " + "\n  ".join(stale))
        return 1
    if check:
        print("shared files in sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
