# InkyPi Buttons

Hardware button handler for a Raspberry Pi + Pimoroni Inky Impression (7.3") running [InkyPi](https://github.com/fatihak/InkyPi).

## What it does

- Uses gpiozero to read the 4 buttons on the Inky Impression.
- Talks to the InkyPi web server via `http://localhost/display_plugin_instance`.
- Button mappings (by default):

  - **A** – `sudo systemctl restart inkypi.service`
  - **B** – Shows an AM or PM calendar plugin instance, depending on the local time.
  - **C/D** – Reserved for future use.

All playlist / plugin instance names are configurable at the top of `inkypi_buttons.py`.

## Files

- `inkypi_buttons.py` – main button handler script
- `systemd/inkypi-buttons.service` – example systemd unit to run the script on boot

## Install (example)

1. Copy `inkypi_buttons.py` to `/home/jack/` (or your preferred user home):

   ```bash
   cp inkypi_buttons.py /home/jack/
   chmod +x /home/jack/inkypi_buttons.py


sudo cp systemd/inkypi-buttons.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable inkypi-buttons.service
sudo systemctl start inkypi-buttons.service

journalctl -u inkypi-buttons.service -f

