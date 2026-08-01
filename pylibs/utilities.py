import os
import sys
import time
import platform


def clear(old=False, test=False):
    if old == False:
        if test == True:
            print("TEST, CLEARING")
            time.sleep(0.5)
        try:
            print("\033[2J\033[H", end="")
        except:
            os.system("cls" if os.name == "nt" else "clear")
    else:
        os.system("cls" if os.name == "nt" else "clear")


def progress_bar(current, total, bar_length=40):
    percent = current / total
    filled_length = int(bar_length * percent)
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    return f"\r[{bar}] {percent*100:5.1f}%"


def restart():
    system = platform.system()

    if system == "Windows":
        import subprocess
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(0)
    elif system in ("Linux", "Darwin"):
        se = sys.executable
        os.execv(se, [se] + sys.argv)
    else:
        raise OSError(f"Unsupported OS: {system}")



if __name__ == "__main__":
    total = 100
    for i in range(total + 1):
        print(progress_bar(i, total), end="", flush=True)
        time.sleep(0.05)
