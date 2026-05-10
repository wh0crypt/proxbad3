import serial.tools.list_ports
import sys

from simple_term_menu import TerminalMenu
from typing import cast

from .config import Config, Frequency


def menu_loop() -> Config:
    """Set up the interactive command-line menu."""
    main_menu_title = "  Main Menu.\n  Press Q or Esc to quit.\n"
    main_menu_items = ["Device", "Frequency", "Continue", "Quit"]
    main_menu_cursor = "* "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False
    main_menu = TerminalMenu(
        title=main_menu_title,
        menu_entries=main_menu_items,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    device_menu_title = "  Device Menu.\n  Press Q or Esc to back to main menu.\n"
    device_menu_items = [
        f"[_] {d}" for d in reversed(serial.tools.list_ports.comports())
    ]
    device_menu_items.append("Back to Main Menu")
    device_menu_back = False
    device_menu = TerminalMenu(
        title=device_menu_title,
        menu_entries=device_menu_items,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    freq_menu_title = "  Frequency Menu.\n  Press Q or Esc to back to main menu.\n"
    freq_menu_items = [
        "[_] High Frequency (HF)",
        "[_] Low Frequency (LF)",
        "Back to Main Menu",
    ]
    freq_menu_back = False
    freq_menu = TerminalMenu(
        title=freq_menu_title,
        menu_entries=freq_menu_items,
        menu_cursor=main_menu_cursor,
        menu_cursor_style=main_menu_cursor_style,
        menu_highlight_style=main_menu_style,
        cycle_cursor=True,
        clear_screen=True,
    )

    device_selected = None
    freq_selected = Frequency.NONE
    main_sel = 0

    while not main_menu_exit:
        dev_label = device_selected.split(" - ")[0] if device_selected else "NONE"

        main_menu_items = [
            f"Device    [{dev_label}]",
            f"Frequency [{freq_selected.name}]",
            "Continue",
            "Quit",
        ]

        main_menu = TerminalMenu(
            title=main_menu_title,
            menu_entries=main_menu_items,
            menu_cursor=main_menu_cursor,
            menu_cursor_style=main_menu_cursor_style,
            menu_highlight_style=main_menu_style,
            cycle_cursor=True,
            clear_screen=True,
            cursor_index=main_sel if isinstance(main_sel, int) else 0,
        )

        main_sel = main_menu.show()

        if main_sel is None or main_sel == 2:
            main_menu_exit = True
            continue

        if main_sel == 3:
            sys.exit(1)

        match (main_sel):
            case 0:  # Device
                device_menu_back = False
                device_sel = 0
                ports = [str(d) for d in reversed(serial.tools.list_ports.comports())]
                while not device_menu_back:
                    options = []
                    for p in ports:
                        is_sel = device_selected == p
                        options.append(f"{'[*] ' if is_sel else '[_] '}{p}")
                    options.append("Back to Main Menu")

                    device_menu = TerminalMenu(
                        title=device_menu_title,
                        menu_entries=options,
                        menu_cursor=main_menu_cursor,
                        menu_cursor_style=main_menu_cursor_style,
                        menu_highlight_style=main_menu_style,
                        cycle_cursor=True,
                        clear_screen=True,
                        cursor_index=device_sel if isinstance(device_sel, int) else 0,
                    )

                    device_sel = device_menu.show()

                    if device_sel is None or device_sel == (len(options) - 1):
                        device_menu_back = True
                    else:
                        device_sel = cast(int, device_sel)
                        selected_port = ports[device_sel]
                        if device_selected == selected_port:
                            device_selected = None
                        else:
                            device_selected = selected_port
                        device_menu_back = True

            case 1:  # Frequency
                freq_menu_back = False
                while not freq_menu_back:
                    options = [
                        f"{'[*] ' if freq_selected == Frequency.HF else '[_] '}High Frequency (HF)",
                        f"{'[*] ' if freq_selected == Frequency.LF else '[_] '}Low Frequency (LF)",
                        "Back to Main Menu",
                    ]

                    freq_menu = TerminalMenu(
                        title=freq_menu_title,
                        menu_entries=options,
                        menu_cursor=main_menu_cursor,
                        menu_cursor_style=main_menu_cursor_style,
                        menu_highlight_style=main_menu_style,
                        cycle_cursor=True,
                        clear_screen=True,
                        cursor_index=(
                            freq_selected.value
                            if freq_selected != Frequency.NONE
                            else 0
                        ),
                    )

                    freq_sel = freq_menu.show()

                    if freq_sel is None or freq_sel == (len(freq_menu_items) - 1):
                        freq_menu_back = True
                    else:
                        new_freq = Frequency(freq_sel)
                        if freq_selected == new_freq:
                            freq_selected = Frequency.NONE
                        else:
                            freq_selected = new_freq
                        freq_menu_back = True
    return Config(device_selected, freq_selected)
