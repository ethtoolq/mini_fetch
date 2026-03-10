import platform
import os
import time
import sys

system = platform.system()

# проверка поддержки цвета
USE_COLOR = sys.stdout.isatty()

GREEN = "\033[92m" if USE_COLOR else ""
CYAN = "\033[96m" if USE_COLOR else ""
RESET = "\033[0m" if USE_COLOR else ""


def get_os():
    return platform.system() + " " + platform.release()


def get_host():
    return platform.node()


def get_kernel():
    return platform.version()


def get_cpu():
    cpu = platform.processor()
    if not cpu:
        cpu = "unknown"
    return cpu


# linux ram
def get_ram_linux():
    meminfo = {}
    with open("/proc/meminfo") as f:
        for line in f:
            key, value = line.split(":")
            meminfo[key] = int(value.strip().split()[0])

    total = meminfo["MemTotal"] // 1024
    free = meminfo["MemAvailable"] // 1024
    used = total - free

    return used, total


# windows ram
def get_ram_windows():
    import ctypes

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("length", ctypes.c_ulong),
            ("memoryLoad", ctypes.c_ulong),
            ("totalPhys", ctypes.c_ulonglong),
            ("availPhys", ctypes.c_ulonglong),
            ("totalPageFile", ctypes.c_ulonglong),
            ("availPageFile", ctypes.c_ulonglong),
            ("totalVirtual", ctypes.c_ulonglong),
            ("availVirtual", ctypes.c_ulonglong),
            ("availExtendedVirtual", ctypes.c_ulonglong),
        ]

    stat = MEMORYSTATUSEX()
    stat.length = ctypes.sizeof(MEMORYSTATUSEX)

    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))

    total = stat.totalPhys // (1024 * 1024)
    free = stat.availPhys // (1024 * 1024)

    used = total - free

    return used, total


# uptime linux
def get_uptime_linux():
    with open("/proc/uptime") as f:
        seconds = float(f.readline().split()[0])

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    return hours, minutes


# uptime windows
def get_uptime_windows():
    uptime = time.time() - os.path.getctime("C:\\Windows\\System32")

    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)

    return hours, minutes


if system == "Linux":
    ram_used, ram_total = get_ram_linux()
    uptime_h, uptime_m = get_uptime_linux()

    logo = [
        "      ______",
        "     / ____/",
        "    / /",
        "   / /___",
        "   \\____/"
    ]

elif system == "Windows":
    ram_used, ram_total = get_ram_windows()
    uptime_h, uptime_m = get_uptime_windows()

    logo = [
        "   _______",
        "  |  _  _ |",
        "  | | || |",
        "  | | || |",
        "  |_| ||_|"
    ]

else:
    logo = ["mini fetch"]


info = [
    f"{CYAN}os{RESET}     : {get_os()}",
    f"{CYAN}host{RESET}   : {get_host()}",
    f"{CYAN}kernel{RESET} : {get_kernel()}",
    f"{CYAN}cpu{RESET}    : {get_cpu()}",
    f"{CYAN}ram{RESET}    : {ram_used}MB / {ram_total}MB",
    f"{CYAN}uptime{RESET} : {uptime_h}h {uptime_m}m"
]


for i in range(max(len(logo), len(info))):
    left = logo[i] if i < len(logo) else ""
    right = info[i] if i < len(info) else ""
    print(GREEN + left + RESET + "   " + right)
