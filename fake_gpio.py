BCM = 'BCM'
OUT = 'OUT'
IN = 'IN'
HIGH = True
LOW = False

_pin_state = {}


def setwarnings(flag):
    print(f"[FakeGPIO] setwarnings({flag})")


def setmode(mode):
    print(f"[FakeGPIO] setmode({mode})")


def setup(pin, mode):
    _pin_state[pin] = False
    print(f"[FakeGPIO] setup(pin={pin}, mode={mode})")


def output(pin, value):
    _pin_state[pin] = value
    print(f"[FakeGPIO] output(pin={pin}, value={value})")


def input(pin):
    return _pin_state.get(pin, LOW)


def cleanup():
    print("[FakeGPIO] cleanup()")
    _pin_state.clear()