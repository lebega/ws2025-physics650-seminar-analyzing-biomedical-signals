import os
import tempfile
from pathlib import Path

def fix_tmp_for_pytisean():
    """
    This function fixes the Temp path on linux
    Ensure a valid temp directory on Linux + macOS.
    Preference order:
      1) $TMPDIR if valid
      2) tempfile.gettempdir()
      3) /tmp (fallback)
    """
    candidates = []

    env = os.environ.get("TMPDIR")
    if env:
        candidates.append(env)

    candidates.append(tempfile.gettempdir())
    candidates.append("/tmp")

    for d in candidates:
        try:
            p = Path(d)
            p.mkdir(parents=True, exist_ok=True)
            test = p / "pytisean_write_test.tmp"
            test.write_text("ok", encoding="utf-8")
            test.unlink()
            os.environ["TMPDIR"] = str(p)
            tempfile.tempdir = str(p)
            return str(p)
        except Exception:
            continue

    raise RuntimeError("No writable temp directory found for pytisean.")
