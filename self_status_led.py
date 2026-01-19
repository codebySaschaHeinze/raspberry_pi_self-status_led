#!/usr/bin/env python3
from gpiozero import RGBLED
import subprocess
import time
import signal
import sys


led = RGBLED(red=22, green=27, blue=17)

COLORS = {
    "OFF":     (0, 0, 0),
    "GREEN":   (0, 0.1, 0),
    "BLUE":    (0, 0, 1),
    "YELLOW":  (1, 1, 0),
    "CYAN":    (0, 1, 1),
    "MAGENTA": (1, 0, 1),
    "RED":     (1, 0, 0),
}

def set_color(name):
    led.color = COLORS.get(name, COLORS["MAGENTA"])

def is_active(unit: str) -> bool:
    r = subprocess.run(["systemctl", "is-active", unit], capture_output=True, text=True)
    return r.stdout.strip() == "active"


PATTERNS = {
    "BOOTING":  [
        ("RED", 0.2), ("OFF", 0.1),
        ("YELLOW", 0.2), ("OFF", 0.1),
        ("GREEN", 0.2), ("OFF", 0.1),
        ("CYAN", 0.2), ("OFF", 0.1),
        ("BLUE", 0.2), ("OFF", 0.1),
        ("MAGENTA", 0.2), ("OFF", 0.1),
    ],  
    "CHECKING": [("BLUE", 0.15), ("OFF", 0.15)],   
    "OK":       [("GREEN", 1.0)],                     
    "ERROR":    [("RED", 0.15), ("OFF", 0.15)],         
    "WARN":     [("YELLOW", 0.25), ("OFF", 0.75)],      
    "BUSY":     [("CYAN", 0.4), ("OFF", 0.2)],       
}

current_state = "BOOTING"

def set_state(state: str):
    global current_state
    current_state = state if state in PATTERNS else "ERROR"


def decide_state():
    unit = "cron.service"  
    if is_active(unit):
        return "OK"
    return "ERROR"


def run():
    set_state("BOOTING")
    end = time.time() + 5

    i = 0
    while time.time() < end:
        pattern = PATTERNS[current_state]
        color, dur = pattern[i % len(pattern)]
        set_color(color)
        time.sleep(dur)
        i += 1

    while True:
        state = decide_state()
        set_state(state)

        pattern = PATTERNS[current_state]
        t_end = time.time() + 2
        j = 0
        while time.time() < t_end:
            color, dur = pattern[j % len(pattern)]
            set_color(color)
            time.sleep(dur)
            j += 1

def handle_exit(signum, frame):
    led.off()
    led.close()
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

run()
