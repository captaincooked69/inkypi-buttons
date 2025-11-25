#!/usr/bin/env python3
"""
InkyPi hardware button handler for Pimoroni Inky Impression (7.3").

- Button A: restart the main InkyPi service
- Button B: show AM or PM calendar (depending on local time)
- Button C/D: reserved for future use

Tested on Raspberry Pi Zero 2 W + Inky Impression 7.3" with InkyPi.
Requires:
  - gpiozero
  - curl (for talking to the InkyPi web server)
"""

from gpiozero import Button
from signal import pause
from datetime import datetime
import subprocess
import json

# -------------------------------------------------------------------
# CONFIG – tweak these for your own playlists / plugins
# -------------------------------------------------------------------

# InkyPi web server endpoint (same Pi)
ENDPOINT_URL = "http://localhost/display_plugin_instance"

# AM calendar plugin instance
AM_PLAYLIST_NAME = "AM"            # playlist name in InkyPi
AM_PLUGIN_ID = "calendar"          # plugin_id as shown in the UI/network tab
AM_PLUGIN_INSTANCE = "am Meetings" # plugin instance name

# PM calendar plugin instance
PM_PLAYLIST_NAME = "pm"            # playlist name in InkyPi
PM_PLUGIN_ID = "calendar"          # plugin_id as shown in the UI/network tab
PM_PLUGIN_INSTANCE = "PM Calander" # plugin instance name (case/spelling must match!)

# Buttons A–D on Inky Impression 7.3" (top to bottom) – BCM numbers
PIN_A = 5
PIN_B = 6
PIN_C = 16
PIN_D = 24


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def trigger_plugin(playlist_name: str, plugin_id: str, plugin_instance: str) -> None:
    """
    Call InkyPi's /display_plugin_instance endpoint using JSON:
      {"playlist_name": "...", "plugin_id": "...", "plugin_instance": "..."}

    Fire-and-forget: we don't wait for curl to finish or care about the response.
    """
    payload = {
        "playlist_name": playlist_name,
        "plugin_id": plugin_id,
        "plugin_instance": plugin_instance,
    }
    data = json.dumps(payload)

    try:
        subprocess.Popen(
            [
                "curl",
                "-s",
                "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", data,
                ENDPOINT_URL,
            ]
        )
        print(
            f"Triggered plugin (fire-and-forget): "
            f"playlist='{playlist_name}', plugin_id='{plugin_id}', "
            f"instance='{plugin_instance}'"
        )
    except Exception as e:
        print(f"Failed to trigger plugin instance: {e}")


def show_calendar_am_vs_pm() -> None:
    """
    If local time (Pi's timezone) is before 12:00 → use AM instance.
    If 12:00 or later → use PM instance.
    """
    now = datetime.now().astimezone()
    print(f"[B] pressed at {now.isoformat()}")

    if now.hour < 12:
        print("Using AM calendar instance")
        trigger_plugin(
            AM_PLAYLIST_NAME,
            AM_PLUGIN_ID,
            AM_PLUGIN_INSTANCE,
        )
    else:
        print("Using PM calendar instance")
        trigger_plugin(
            PM_PLAYLIST_NAME,
            PM_PLUGIN_ID,
            PM_PLUGIN_INSTANCE,
        )


def restart_inkypi_service() -> None:
    """
    Restart the main InkyPi systemd unit (inkypi.service).
    Adjust the service name here if your unit is named differently.
    """
    try:
        subprocess.Popen(
            ["sudo", "systemctl", "restart", "inkypi.service"]
        )
        print("[A] Restarted InkyPi service (fire-and-forget)")
    except Exception as e:
        print(f"Failed to restart InkyPi service: {e}")


# -------------------------------------------------------------------
# Button callbacks
# -------------------------------------------------------------------

def on_a():
    print("Button A pressed")
    restart_inkypi_service()


def on_b():
    print("Button B pressed")
    show_calendar_am_vs_pm()


def on_c():
    print("Button C pressed (no action yet)")


def on_d():
    print("Button D pressed (no action yet)")


def main() -> None:
    # Set up the 4 buttons
    btn_a = Button(PIN_A, pull_up=True, bounce_time=0.3)
    btn_b = Button(PIN_B, pull_up=True, bounce_time=0.3)
    btn_c = Button(PIN_C, pull_up=True, bounce_time=0.3)
    btn_d = Button(PIN_D, pull_up=True, bounce_time=0.3)

    btn_a.when_pressed = on_a
    btn_b.when_pressed = on_b
    btn_c.when_pressed = on_c
    btn_d.when_pressed = on_d

    print("InkyPi button handler running (gpiozero). "
          "A=restart, B=AM/PM calendar, C/D spare.")
    pause()


if __name__ == "__main__":
    main()
