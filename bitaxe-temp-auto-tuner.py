import requests
import time
import signal
import sys
import argparse

# ANSI Color Codes for console output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"


# Parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Bitaxe Temperature Monitor and Auto-Tuner'
    )
    parser.add_argument('bitaxe_ip', help='IP address of the Bitaxe (e.g., 192.168.2.26)')
    parser.add_argument('-v', '--voltage', type=int, default=1200,
                        help='Initial core voltage in mV (default: 1200)')
    parser.add_argument('-f', '--frequency', type=int, default=800,
                        help='Initial frequency in MHz (default: 800)')
    parser.add_argument('-t', '--target_temp', type=int, default=60,
                        help='Target CPU temperature in °C (default: 60)')
    parser.add_argument('-i', '--interval', type=int, default=5,
                        help='Monitoring sample interval in seconds (default: 5)')
    parser.add_argument('-p', '--power_limit', type=int, default=30,
                        help='Power supply wattage limit (default: 30W)')
    return parser.parse_args()


args = parse_arguments()
bitaxe_ip = f"http://{args.bitaxe_ip}"
current_voltage = args.voltage
current_frequency = args.frequency
target_temp = args.target_temp
sample_interval = args.interval
power_limit = args.power_limit

# Configuration parameters
voltage_step = 10  # mV adjustment step
frequency_step = 25  # MHz adjustment step
min_allowed_voltage = 1000  # mV
max_allowed_voltage = 1300  # mV
min_allowed_frequency = 700  # MHz
max_allowed_frequency = 900  # MHz

# Flag to control main loop
running = True


# Signal handler for graceful exit
def handle_sigint(signum, frame):
    global running
    print(RED + "\nExiting Bitaxe Monitor." + RESET)
    running = False


signal.signal(signal.SIGINT, handle_sigint)


def get_system_info():
    """Fetch system info from Bitaxe API."""
    try:
        response = requests.get(f"{bitaxe_ip}/api/system/info", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(YELLOW + f"Error fetching system info: {e}" + RESET)
        return None


def set_system_settings(core_voltage, frequency):
    """Set system parameters via Bitaxe API."""
    settings = {
        "coreVoltage": core_voltage,
        "frequency": frequency
    }
    try:
        response = requests.patch(f"{bitaxe_ip}/api/system", json=settings, timeout=10)
        response.raise_for_status()
        print(YELLOW + f"Applying settings: Voltage = {core_voltage}mV, Frequency = {frequency}MHz" + RESET)
        time.sleep(2)
    except requests.exceptions.RequestException as e:
        print(RED + f"Error setting system settings: {e}" + RESET)


def monitor_and_adjust():
    global current_voltage, current_frequency
    print(GREEN + f"Starting Bitaxe Monitor. Target temp: {target_temp}°C" + RESET)
    set_system_settings(current_voltage, current_frequency)

    while running:
        info = get_system_info()
        if info is None:
            time.sleep(sample_interval)
            continue

        temp = info.get("temp")
        hash_rate = info.get("hashRate", 0)
        voltage_reported = info.get("voltage", 0)
        power_consumption = info.get("power", 0)

        status = (f"Temp: {temp}°C | Hashrate: {int(hash_rate)} GH/s | "
                  f"Power: {power_consumption}W | "
                  f"Voltage: {voltage_reported}mV | "
                  f"Current Settings -> Voltage: {current_voltage}mV, Frequency: {current_frequency}MHz")
        print(GREEN + status + RESET)

        if temp is None or power_consumption > power_limit:
            print(RED + "Power limit exceeded! Lowering settings." + RESET)
            if current_frequency - frequency_step >= min_allowed_frequency:
                current_frequency -= frequency_step
            elif current_voltage - voltage_step >= min_allowed_voltage:
                current_voltage -= voltage_step
            set_system_settings(current_voltage, current_frequency)
        elif temp > target_temp:
            print(RED + f"Temp {temp}°C exceeds limit. Lowering settings." + RESET)
            if current_frequency - frequency_step >= min_allowed_frequency:
                current_frequency -= frequency_step
            elif current_voltage - voltage_step >= min_allowed_voltage:
                current_voltage -= voltage_step
            set_system_settings(current_voltage, current_frequency)
        elif temp < (target_temp - 2):
            print(YELLOW + f"Temp {temp}°C is low. Trying to optimize." + RESET)
            if current_frequency + frequency_step <= max_allowed_frequency:
                current_frequency += frequency_step
            elif current_voltage + voltage_step <= max_allowed_voltage:
                current_voltage += voltage_step
            set_system_settings(current_voltage, current_frequency)
        elif hash_rate < 1600:  # Hashrate should be close to benchmarked results
            print(YELLOW + "Hashrate underperforming! Adjusting voltage." + RESET)
            if current_voltage + voltage_step <= max_allowed_voltage:
                current_voltage += voltage_step
                set_system_settings(current_voltage, current_frequency)
        else:
            print(GREEN + "Stable. No adjustment needed." + RESET)

        time.sleep(sample_interval)


if __name__ == "__main__":
    try:
        monitor_and_adjust()
    except Exception as e:
        print(RED + f"An unexpected error occurred: {e}" + RESET)
    finally:
        print(GREEN + "Exiting monitor. Goodbye." + RESET)
