# Raspberry Pi Debugging Runbook

Use this when the Pi stops responding over SSH or the backend/frontend dies while running in tmux.

## Current Known-Good State

These were verified after the last reboot:

- Wi-Fi interface: `wlan0`
- Static Wi-Fi IP: `10.0.0.123`
- Wi-Fi signal: about `-50 dBm`
- Wi-Fi power save: `off`
- SSH service: active
- Disk usage: healthy
- Memory usage after boot: healthy
- Temperature after boot: about `37 C`
- `vcgencmd get_throttled`: `throttled=0x0`

Persistent journaling has been enabled with:

```bash
sudo mkdir -p /var/log/journal
sudo systemctl restart systemd-journald
```

Confirm it is working:

```bash
journalctl --list-boots
```

## Before Starting The App

Create a debug log directory:

```bash
mkdir -p ~/zimalab-debug
```

In one tmux pane, capture system, SSH, network, and kernel logs:

```bash
journalctl -f -u NetworkManager -u ssh -k 2>&1 | tee -a ~/zimalab-debug/system-live.log
```

In another tmux pane, watch system health:

```bash
watch -n 2 'date; uptime; free -h; vcgencmd measure_temp; vcgencmd get_throttled; df -h /'
```

Start the backend with persistent logs:

```bash
cd ~/dev/zima-labs/zima-lab/rpi
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 2>&1 | tee -a ~/zimalab-debug/backend.log
```

Start the frontend with persistent logs:

```bash
cd ~/dev/zima-labs/zima-lab/frontend
npm run dev -- --host 0.0.0.0 2>&1 | tee -a ~/zimalab-debug/frontend.log
```

## If SSH Stops Working

From another machine on the same network:

```bash
ping 10.0.0.123
```

If ping fails with `Destination host unreachable`, the Pi is either off the network or locked up. If the red power LED is solid, power is present, but the Pi may still be frozen.

Power-cycle the Pi if needed, then SSH in immediately and run:

```bash
journalctl --list-boots
journalctl -b -1 -n 300 --no-pager
journalctl -b -1 -k --no-pager | grep -iE 'wlan|brcm|firmware|deauth|disconnect|reset|oom|killed|voltage|thrott|thermal|mmc|i/o error|ext4|usb'
tail -200 ~/zimalab-debug/system-live.log
tail -200 ~/zimalab-debug/backend.log
tail -200 ~/zimalab-debug/frontend.log
vcgencmd get_throttled
```

## Quick Health Checks

Run these any time after reboot:

```bash
uptime
df -h
free -h
vcgencmd get_throttled
vcgencmd measure_temp
systemctl status ssh --no-pager
iw dev wlan0 link
iw dev wlan0 get power_save
ip addr show wlan0
ip route
```

## How To Interpret Results

`vcgencmd get_throttled` should be:

```text
throttled=0x0
```

Anything else means the Pi has seen undervoltage, throttling, or thermal limits since boot.

Kernel log clues:

- `oom`, `Out of memory`, `Killed process`: memory exhaustion
- `voltage`, `under-voltage`, `throttled`: power supply or cable issue
- `thermal`: overheating
- `mmc`, `I/O error`, `EXT4-fs error`: SD card or filesystem issue
- `wlan`, `brcm`, `deauth`, `disconnect`: Wi-Fi or driver issue
- `usb`, `reset`: USB device issue, possibly webcam/camera-related

The previous reboot showed:

```text
EXT4-fs (mmcblk0p2): orphan cleanup on readonly fs
```

That usually means the system did not shut down cleanly. It does not identify the root cause by itself, but it supports investigating hard freeze, power interruption, or forced unplug rather than a normal app exit.

