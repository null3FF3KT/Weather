from colorama import init, Fore, Back, Style
import textwrap

# Initialize colorama
init(autoreset=True)

def print_header(text):
    print(f"\n{Back.CYAN}{Fore.YELLOW}{Style.BRIGHT}{text:^60}{Style.RESET_ALL}")

def print_subheader(text):
    print(f"{Fore.YELLOW}{Style.BRIGHT}{text.center(60)}{Style.RESET_ALL}")

def print_info(label, value):
    label_width = 20
    value_width = 38
    print(f"{Fore.LIGHTGREEN_EX}{label:<{label_width}}{Style.RESET_ALL}"
          f"{value:<{value_width}}")

def print_warning(text):
    print(f"{Back.RED}{Fore.WHITE}{Style.BRIGHT}{text:^60}{Style.RESET_ALL}")

def print_highlight(text, color=Fore.LIGHTYELLOW_EX):
    print(f"{color}{Style.BRIGHT}{text:^60}{Style.RESET_ALL}")

def print_wrapped(text, width=60):
    print(textwrap.fill(text, width=width))