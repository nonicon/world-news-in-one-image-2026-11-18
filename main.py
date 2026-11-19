"""World News in One Image - 18 November 2026.

The entry image (entry.png, drawn at build time with Pillow) sums up the
world news of Wednesday 18 November 2026: the Xi-Trump-Putin summit in
Shenzhen, the US-Iran strikes in the Gulf, Ukraine's hit on the Kerch
Bridge, the Democrats taking the US Senate, Cyclone Akvan, the Ebola
surge in DR Congo, and the US losing measles-free status, plus five
more stories in the "Also today" strip.

The program runs with no network and only the standard library: it
copies the image beside this file to /output/entry.png.
"""
import os
import shutil
import sys


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    sys.exit(main())
