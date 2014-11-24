# coding=utf-8

import win32api, win32con
import time
from blockext import *

class Leds:

    @command("%m.keys on", defaults=["caps lock"])
    def led_on(self, keys):
        nVirtKey = {
            "caps lock": win32con.VK_CAPITAL,
            "num lock": win32con.VK_NUMLOCK,
        }[keys]
        if(not win32api.GetKeyState(nVirtKey)):
            win32api.keybd_event(nVirtKey, 0, 0, 0)
            win32api.keybd_event(nVirtKey, 0, win32con.KEYEVENTF_KEYUP, 0)

    @command("%m.keys off", defaults=["caps lock"])
    def led_off(self, keys):
        nVirtKey = {
            "caps lock": win32con.VK_CAPITAL,
            "num lock": win32con.VK_NUMLOCK,
        }[keys]
        if(win32api.GetKeyState(nVirtKey)):
            win32api.keybd_event(nVirtKey, 0, 0, 0)
            win32api.keybd_event(nVirtKey, 0, win32con.KEYEVENTF_KEYUP, 0)

    @command("blink %m.keys %n times, delay %n us", defaults=["caps lock", 5, 100], is_blocking=True)
    def led_blink(self, keys, blinks=5, delay=100):
        nVirtKey = {
            "caps lock": win32con.VK_CAPITAL,
            "num lock": win32con.VK_NUMLOCK,
        }[keys]
        for n in range(0, 2*blinks):
            win32api.keybd_event(nVirtKey, 0, 0, 0)
            win32api.keybd_event(nVirtKey, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.001*delay)

descriptor = Descriptor(
    name = "Keyboard LEDs",
    port = 5001,
    blocks = get_decorated_blocks_from_class(Leds),
    menus = dict(
        keys = ["caps lock", "num lock"]
    ),
)

extension = Extension(Leds, descriptor)

if __name__ == "__main__":
    extension.run_forever(debug=True)
