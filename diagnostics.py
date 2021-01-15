import subprocess
from typing import Dict
import psutil
import humanize

# TODO make diagnostics object containing everything below
def get_cpu_usage_percent():
    return psutil.cpu_percent()

def get_wifi_signal_strength():
    output = subprocess.check_output(['iwconfig'], text=True, 
                                        stderr=subprocess.DEVNULL)
    strength_fraction = output.split('Link Quality=')[1].split()[0]
    numerator, denominator = map(float, strength_fraction.split('/', 1))
    return numerator / denominator


def get_memory_info():
    mem = psutil.virtual_memory()

    used_percent = float(mem.used) / mem.available
    return {
        'Used Percentage': used_percent, 
        'Memory Available': humanize.naturalsize(mem.available)
    }

    
if __name__ == '__main__':
    print('Memory:', get_memory_info())
    print('Wifi:', get_wifi_signal_strength())
    print('CPU Usage:', get_cpu_usage_percent())