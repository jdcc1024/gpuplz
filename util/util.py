CEND = '\033[0m'
CRED = '\033[91m'
CYEL = '\033[33m'
from colorama import init as cr_init

cr_init()

def print_yellow(msg):
    print(f"{CYEL}{msg}{CEND}")

def print_red(msg):
    print(f"{CRED}{msg}{CEND}")

def print_col(msg, ansi):
    print(f"{ansi}{msg}{CEND}")