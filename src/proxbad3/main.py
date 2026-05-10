#!/usr/bin/env python

import argparse
import os.path
import sys

from proxbad3.menu import menu_loop
from proxbad3.config import Config, Frequency
from proxmark3 import Proxmark3Adapter, Proxmark3


def setup_parser() -> argparse.ArgumentParser:
    """Set up the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="proxbad3",
        description="An automated tool for testing the security of RFID access control systems using the Proxmark3 device.",
        epilog="Example usage: python main.py --device /dev/ttyACM0",
    )
    parser.add_argument(
        "-d", "--device", dest="device", help="Path to the Proxmark3 device"
    )
    parser.add_argument(
        "-hf",
        "--high-frequency",
        dest="hf",
        help="Enable high-frequency (13.56 MHz) testing mode",
        action="store_false",
    )
    parser.add_argument(
        "-lf",
        "--low-frequency",
        dest="lf",
        help="Enable low-frequency (125 kHz) testing mode",
        action="store_true",
    )
    return parser


def make_config() -> Config:
    """Create a configuration object based on command-line arguments or menu selection."""
    if not len(sys.argv) > 1:
        return menu_loop()
    else:
        parser = setup_parser()
        args = parser.parse_args()
        return Config(args.device, Frequency(0 if args.hf else 1))


def main() -> None:
    """Main function to run the Proxmark3 security testing tool."""
    config = make_config()
    if config.freq == Frequency.LF:
        print("Low-frequency testing mode not supported yet.")
        sys.exit(1)

    device_path = config.device.split(" ")[0] if config.device else None
    adapter = None
    if device_path and os.path.exists(device_path):
        adapter = Proxmark3Adapter(device_path)

    if not adapter:
        print("The specified device does not exist.")
        sys.exit(1)

    pm3 = Proxmark3(adapter)


if __name__ == "__main__":
    """Entry point of the script."""
    main()
