from os import system
import subprocess
from typing import Dict
import psutil
import humanize
import platform
import time


def get_cpu_usage_percent() -> float:
    """Get the system's CPU utilization percentage."""
    return psutil.cpu_percent()


def get_wifi_signal_strength() -> float:
    """Get the wifi signal strength as a percentage. This function extracts the
    output from the 'iwconfig' command to get the strength value.

    Returns:
        float: the wifi signal strength percentage
    """
    output = subprocess.check_output(['iwconfig'], text=True, 
                                        stderr=subprocess.DEVNULL)
    strength_fraction = output.split('Link Quality=')[1].split()[0]
    numerator, denominator = map(float, strength_fraction.split('/', 1))
    return (numerator / denominator) * 100


def get_memory_used_percent() -> float:
    """Get the percentage of memory on the system that has been used out of the
    total available memory.

    Returns:
        float: the system's memory used percentage
    """
    mem = psutil.virtual_memory()
    used_percent = (float(mem.used) / mem.available) * 100
    return used_percent


def get_memory_available() -> int:
    """Return the system's available memory in bytes."""
    return psutil.virtual_memory().available


def get_system() -> str:
    """Return the platform's system (Linux, Windows, etc.) if it can be found, 
    otherwise 'Unknown'

    Returns:
        str: the platform's system or 'Unknown'
    """
    return platform.system() if platform.system() else 'Unknown'


def get_processor() -> str:
    """Return the platform's processor if it can be found, otherwise 'Unknown'

    Returns:
        str: the platform's processor or 'Unknown'
    """
    return platform.processor() if platform.processor() else 'Unknown'


def get_boot_time() -> str:
    """Get the system's last boot time as a human readable string.

    Returns:
        str: the system's last boot time, formatted as mm/dd/yyy HR:MM AM/PM
    """
    boot_time_epoch = psutil.boot_time()
    return time.strftime('%m/%d/%Y %I:%M %p', time.localtime(boot_time_epoch))


def get_temperature() -> float:
    """Get the computer hardware's temperature in degrees Farenheit. If multiple
    temperature sensors are present, this returns the first sensor's 
    temperature.

    Returns:
        float: the computer hardware's temperature in degrees Farenheit
    """

    temps = psutil.sensors_temperatures(fahrenheit=True)
    first_temp = next(iter(temps.values()))[0].current
    return first_temp


def get_formatted_diagnostics() -> Dict[str, any]:
    """Get computer diagnostics as a dictionary with attributes as keys and 
    their formatted values as values.

    Returns:
        Dict[str, any]: a dictionary of diagnostic attributes, where values have
        been formatted so as to be displayable to a user
    """

    return {
        'CPU Usage': f'{get_cpu_usage_percent():.1f}%',
        'Wifi Strength': f'{get_wifi_signal_strength():.1f}%',
        'Temperature': f'{get_temperature():.1f}\u00b0F',
        'Memory Used': f'{get_memory_used_percent():.1f}%',
        'Memory Available': f'{humanize.naturalsize(get_memory_available())}',
        'System': get_system(),
        'Processor': get_processor(),
        'Boot Time': get_boot_time()
    }