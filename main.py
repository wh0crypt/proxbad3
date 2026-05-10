#!/usr/bin/env python

import proxmark3 as pm3
import argparse
import os.path


def setup_parser() -> argparse.ArgumentParser:
    """Set up the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="proxbad3",
        description="An automated tool for testing the security of RFID access control systems using the Proxmark3 device.",
        epilog="Example usage: python main.py --device /dev/ttyACM0",
    )
    parser.add_argument(
        "-d", "--device", help="Path to the Proxmark3 device", required=True
    )
    return parser


def main():
    """Main function to run the Proxmark3 security testing tool."""
    parser = setup_parser()
    args = parser.parse_args()
    adapter = None
    if args.device and os.path.exists(args.device):
        adapter = pm3.Proxmark3Adapter(args.device)

    if not adapter:
        print("The specified device does not exist.")
        return

    print(f"Using device: {args.device}")


if __name__ == "__main__":
    """Entry point of the script."""
    main()
