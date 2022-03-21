import websocket
from threading import Thread
import time
import sys
import keyboard
import ctypes
import pyautogui


def on_message(ws, message):
    print(message)
    if(message == "opt:1"):
        # keyboard.press('1')
        # keyboard.press_and_release("win+l")
        ctypes.windll.user32.LockWorkStation()
    else:
        keyboard.press('2')
        # ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
        # keyboard.press_and_release("2")
        # pyautogui.press('3')



def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    def run(*args):
        for i in range(3):
            # send the message, then wait
            # so thread doesn't exit and socket
            # isn't closed
            ws.send("Hello %d" % i)
            time.sleep(1)

        time.sleep(1)
        # ws.close()
        print("Thread terminating...")

    Thread(target=run).start()


# if __name__ == "__main__":
# 打开调试
websocket.enableTrace(True)
# if len(sys.argv) < 2:
#     host = "ws://echo.websocket.events/"
# else:
#     host = sys.argv[1]
host = "ws://192.168.43.120:80/ws"
# host = "ws://192.168.31.95:80/ws"
ws = websocket.WebSocketApp(host,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.on_open = on_open
ws.run_forever()



# ----------------------------------------------------------

# import ctypes
# from ctypes import wintypes
# import time

# user32 = ctypes.WinDLL('user32', use_last_error=True)

# INPUT_MOUSE    = 0
# INPUT_KEYBOARD = 1
# INPUT_HARDWARE = 2

# KEYEVENTF_EXTENDEDKEY = 0x0001
# KEYEVENTF_KEYUP       = 0x0002
# KEYEVENTF_UNICODE     = 0x0004
# KEYEVENTF_SCANCODE    = 0x0008

# MAPVK_VK_TO_VSC = 0

# # msdn.microsoft.com/en-us/library/dd375731
# VK_TAB  = 0x09
# VK_MENU = 0x12

# # C struct definitions

# wintypes.ULONG_PTR = wintypes.WPARAM

# class MOUSEINPUT(ctypes.Structure):
#     _fields_ = (("dx",          wintypes.LONG),
#                 ("dy",          wintypes.LONG),
#                 ("mouseData",   wintypes.DWORD),
#                 ("dwFlags",     wintypes.DWORD),
#                 ("time",        wintypes.DWORD),
#                 ("dwExtraInfo", wintypes.ULONG_PTR))

# class KEYBDINPUT(ctypes.Structure):
#     _fields_ = (("wVk",         wintypes.WORD),
#                 ("wScan",       wintypes.WORD),
#                 ("dwFlags",     wintypes.DWORD),
#                 ("time",        wintypes.DWORD),
#                 ("dwExtraInfo", wintypes.ULONG_PTR))

#     def __init__(self, *args, **kwds):
#         super(KEYBDINPUT, self).__init__(*args, **kwds)
#         # some programs use the scan code even if KEYEVENTF_SCANCODE
#         # isn't set in dwFflags, so attempt to map the correct code.
#         if not self.dwFlags & KEYEVENTF_UNICODE:
#             self.wScan = user32.MapVirtualKeyExW(self.wVk,
#                                                  MAPVK_VK_TO_VSC, 0)

# class HARDWAREINPUT(ctypes.Structure):
#     _fields_ = (("uMsg",    wintypes.DWORD),
#                 ("wParamL", wintypes.WORD),
#                 ("wParamH", wintypes.WORD))

# class INPUT(ctypes.Structure):
#     class _INPUT(ctypes.Union):
#         _fields_ = (("ki", KEYBDINPUT),
#                     ("mi", MOUSEINPUT),
#                     ("hi", HARDWAREINPUT))
#     _anonymous_ = ("_input",)
#     _fields_ = (("type",   wintypes.DWORD),
#                 ("_input", _INPUT))

# LPINPUT = ctypes.POINTER(INPUT)

# def _check_count(result, func, args):
#     if result == 0:
#         raise ctypes.WinError(ctypes.get_last_error())
#     return args

# user32.SendInput.errcheck = _check_count
# user32.SendInput.argtypes = (wintypes.UINT, # nInputs
#                              LPINPUT,       # pInputs
#                              ctypes.c_int)  # cbSize

# # Functions

# def PressKey(hexKeyCode):
#     x = INPUT(type=INPUT_KEYBOARD,
#               ki=KEYBDINPUT(wVk=hexKeyCode))
#     user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

# def ReleaseKey(hexKeyCode):
#     x = INPUT(type=INPUT_KEYBOARD,
#               ki=KEYBDINPUT(wVk=hexKeyCode,
#                             dwFlags=KEYEVENTF_KEYUP))
#     user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

# def AltTab():
#     """Press Alt+Tab and hold Alt key for 2 seconds
#     in order to see the overlay.
#     """
#     PressKey(VK_MENU)   # Alt
#     PressKey(VK_TAB)    # Tab
#     ReleaseKey(VK_TAB)  # Tab~
#     time.sleep(2)
#     ReleaseKey(VK_MENU) # Alt~

# if __name__ == "__main__":
#     AltTab()