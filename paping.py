import socket
import time
import sys
import colorama
from colorama import Fore, Style, Back
from threading import Thread
from itertools import cycle
import signal

colorama.init()

class Spinner:
    def __init__(self):
        self.spinner_chars = cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.running = False
        self.thread = None

    def spin(self):
        while self.running:
            sys.stdout.write(f"\r{next(self.spinner_chars)} Testing connection... ")
            sys.stdout.flush()
            time.sleep(0.1)

    def __enter__(self):
        self.running = True
        self.thread = Thread(target=self.spin)
        self.thread.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write('\r' + ' ' * 30 + '\r')
        sys.stdout.flush()

def print_banner():
    print(f"\n{Fore.CYAN}{Back.BLACK}{'*' * 60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{' TCP CONNECTION TESTER '.center(60, '★')}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'*' * 60}{Style.RESET_ALL}\n")

def print_stats(start_time, success, total, response_times):
    duration = time.time() - start_time
    print(f"\n{Fore.CYAN}{' TEST SUMMARY '.center(60, '─')}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}Total Time:  {Fore.WHITE}{duration:.2f}s")
    print(f"{Fore.MAGENTA}Attempts:    {Fore.WHITE}{total}")
    print(f"{Fore.MAGENTA}Successful:  {Fore.WHITE}{success} ({success/total*100:.1f}%)")
    print(f"{Fore.MAGENTA}Failed:      {Fore.WHITE}{total - success}")
    
    if response_times:
        print(f"\n{Fore.MAGENTA}Fastest:     {Fore.WHITE}{min(response_times):.2f}ms")
        print(f"{Fore.MAGENTA}Slowest:     {Fore.WHITE}{max(response_times):.2f}ms")
        print(f"{Fore.MAGENTA}Average:     {Fore.WHITE}{sum(response_times)/len(response_times):.2f}ms")
    
    print(f"{Fore.CYAN}{'─' * 60}{Style.RESET_ALL}")

def paping(host, port, attempts=5, timeout=2):
    success = 0
    response_times = []
    start_time = time.time()

    print(f"{Fore.BLUE}\n🔎 Target: {Fore.WHITE}{host}{Fore.BLUE} | Port: {Fore.WHITE}{port}")
    print(f"{Fore.BLUE}🚀 Attempts: {Fore.WHITE}{attempts}{Fore.BLUE} | Timeout: {Fore.WHITE}{timeout}s{Style.RESET_ALL}\n")

    for attempt in range(1, attempts + 1):
        try:
            with Spinner():
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                start = time.time()
                sock.connect((host, port))
                elapsed = (time.time() - start) * 1000
                response_times.append(elapsed)
                success += 1
                status = f"{Fore.GREEN}✔ Success{Style.RESET_ALL}"
                time_info = f"{Fore.WHITE}{elapsed:.2f}ms"
        except socket.timeout:
            status = f"{Fore.RED}✖ Timeout{Style.RESET_ALL}"
            time_info = f"{Fore.WHITE}N/A"
        except ConnectionRefusedError:
            status = f"{Fore.RED}✖ Refused{Style.RESET_ALL}"
            time_info = f"{Fore.WHITE}N/A"
        except Exception as e:
            status = f"{Fore.RED}⚠ Error: {str(e)}{Style.RESET_ALL}"
            time_info = f"{Fore.WHITE}N/A"
        finally:
            sys.stdout.write(f"\r{Fore.CYAN}Attempt {attempt}/{attempts}: {status} {time_info}{Style.RESET_ALL}\n")
            if 'sock' in locals():
                sock.close()

        time.sleep(0.5 if attempt < attempts else 0)

    print_stats(start_time, success, attempts, response_times)

def get_input(prompt, validation_func, error_msg):
    while True:
        try:
            value = input(prompt)
            return validation_func(value)
        except ValueError:
            print(f"{Fore.RED}⚠ {error_msg}{Style.RESET_ALL}")

def validate_port(port):
    port = int(port)
    if 1 <= port <= 65535:
        return port
    raise ValueError

def validate_attempts(attempts):
    attempts = int(attempts)
    if attempts > 0:
        return attempts
    raise ValueError

def validate_timeout(timeout):
    timeout = float(timeout)
    if timeout > 0:
        return timeout
    raise ValueError

def signal_handler(sig, frame):
    print(f"\n{Fore.RED}\n⚠ Test interrupted by user!{Style.RESET_ALL}")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print_banner()

    host = get_input(
        f"{Fore.YELLOW}🌐 Enter host/domain: {Style.RESET_ALL}",
        str,
        "Please enter a valid hostname or IP address"
    )

    port = get_input(
        f"{Fore.YELLOW}🔌 Enter port (1-65535): {Style.RESET_ALL}",
        validate_port,
        "Invalid port number (1-65535)"
    )

    attempts = get_input(
        f"{Fore.YELLOW}🔁 Enter number of attempts: {Style.RESET_ALL}",
        validate_attempts,
        "Please enter a positive integer"
    )

    timeout = get_input(
        f"{Fore.YELLOW}⏳ Enter timeout (seconds): {Style.RESET_ALL}",
        validate_timeout,
        "Please enter a positive number"
    )

    try:
        print(f"\n{Fore.BLUE}🔄 Resolving host...{Style.RESET_ALL}")
        ip = socket.gethostbyname(host)
        print(f"{Fore.GREEN}✅ Resolved {host} → {ip}{Style.RESET_ALL}")
    except socket.gaierror:
        print(f"{Fore.RED}❌ Failed to resolve host!{Style.RESET_ALL}")
        sys.exit(1)

    print(f"\n{Fore.YELLOW}🚦 Starting connectivity test...{Style.RESET_ALL}")
    paping(host, port, attempts, timeout)
    print(f"\n{Fore.GREEN}{' TEST COMPLETE '.center(60, '★')}{Style.RESET_ALL}\n")
    input(f"{Fore.YELLOW}🔚 Press Enter to exit...{Style.RESET_ALL}")
