import os
import sys

def clear_input_buffer():
    if os.name == 'nt':  # Windows
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:  # Linux / macOS
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)