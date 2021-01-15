from os import system
import subprocess
from typing import Dict
import psutil
import humanize
import platform

def get_cpu_usage_percent():
    return psutil.cpu_percent()


def get_wifi_signal_strength():
    output = subprocess.check_output(['iwconfig'], text=True, 
                                        stderr=subprocess.DEVNULL)
    strength_fraction = output.split('Link Quality=')[1].split()[0]
    numerator, denominator = map(float, strength_fraction.split('/', 1))
    return (numerator / denominator) * 100


def get_memory_info():
    mem = psutil.virtual_memory()

    used_percent = (float(mem.used) / mem.available) * 100
    return {
        'Used Percentage': used_percent, 
        'Memory Available': humanize.naturalsize(mem.available)
    }


def get_system():
    return platform.system() if platform.system() else 'Unknown'


def get_processor():
    return platform.processor() if platform.processor() else 'Unknown'

def get_temperature():
    temps = psutil.sensors_temperatures(fahrenheit=True)
    first_temp = next(iter(temps.values()))[0].current
    return first_temp

def get_diagnostics(): # TODO rename formatted diagnostics
    return {
        'CPU Usage': f'{get_cpu_usage_percent():.1f}%',
        'Wifi Strength': f'{get_wifi_signal_strength():.1f}%',
        'Temperature:': f'{get_temperature():.1f}\u00b0F',
        'Memory Used': f'{get_memory_info()["Used Percentage"]:.1f}%',
        'Memory Available': f'{get_memory_info()["Memory Available"]}',
        'System': get_system(),
        'Processor': get_processor()
    }