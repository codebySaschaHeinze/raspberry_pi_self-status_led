from gpiozero import RGBLED
from time import sleep

led = RGBLED(red=22, green=27, blue=17)

COLORS = {
    "OFF":     (0, 0, 0),
    "GREEN":   (0, 1, 0),  
    "BLUE":    (0, 0, 1),  
    "YELLOW":  (1, 1, 0),  
    "CYAN":    (0, 1, 1),  
    "MAGENTA": (1, 0, 1),  
    "RED":     (1, 0, 0),  
}

