"""HinglishVinglish command line (successor to hinglish-legacy-brainstorm/app.py).

Runs offline with no credentials:

    python cli.py                                  # interactive
    python cli.py romanize "मैं कल दिल्ली जा रहा हूँ"
    python cli.py key bohot bahut bhot

Translation (English <-> Hindi) arrives in Phase 2.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "engine"))

from hv.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
