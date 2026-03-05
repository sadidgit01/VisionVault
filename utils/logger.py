import sys
from colorama import init, Fore, Style

# Initialize colorama for Windows support
init(autoreset=True)

class VaultLogger:
    @staticmethod
    def info(msg):
        print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {msg}")

    @staticmethod
    def success(msg):
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {msg}")

    @staticmethod
    def warn(msg):
        print(f"{Fore.YELLOW}[WARN]{Style.RESET_ALL} {msg}")

    @staticmethod
    def error(msg):
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {msg}", file=sys.stderr)

    @staticmethod
    def progress(current, total, label="Processing"):
        percent = int((current / total) * 100)
        bar = '█' * (percent // 5) + '-' * (20 - (percent // 5))
        sys.stdout.write(f'\r{Fore.MAGENTA}[{label}]{Style.RESET_ALL} |{bar}| {percent}%')
        sys.stdout.flush()