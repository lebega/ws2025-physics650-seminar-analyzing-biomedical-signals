#!/usr/bin/env python3
import os
import shutil
import sys
import tempfile
from fix_temp_path import fix_tmp_for_pytisean
import pytisean.pytisean as pt
from pytisean import tiseano
def main():
    tmp = fix_tmp_for_pytisean()
    print("Using temp dir:", tmp)
    pt.DIRSTR=tmp

    os.environ["TMPDIR"] = "/tmp"
    tempfile.tempdir = "/tmp"

    exe = shutil.which("henon")
    if not exe:
        print("FAIL: TISEAN binary 'henon' not found on PATH.")
        sys.exit(1)
    print(f"OK: found henon at: {exe}")

    

    data, msg = tiseano("henon", "-l2000")
    print("OK: pytisean executed henon")
    print("shape:", getattr(data, "shape", None))
    print("first row:", data[0])
    print("msg head:", (msg or "")[:200])

if __name__ == "__main__":
    main()
