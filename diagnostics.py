import subprocess
from typing import Dict


def get_wifi_signal_strength():
    output = subprocess.check_output(['iwconfig'], text=True, 
                                        stderr=subprocess.DEVNULL)
    strength_fraction = output.split('Link Quality=')[1].split()[0]
    numerator, denominator = map(float, strength_fraction.split('/', 1))
    return numerator / denominator


def get_memory_info(units_arg:str = '--mega') -> Dict[str, str]:
    output = subprocess.check_output(['free', '-w', '--mega'], text=True)
    # TODO can i use headers, numbers = output.split() ? 
    column_headers = output.split('Mem:')[0].split()[:7]
    numbers = list(map(int, 
                        output.split('Mem:')[1].split()[:len(column_headers)]))
    return dict(zip(column_headers, numbers))


if __name__ == '__main__':
    print(get_memory_info())
    print(get_wifi_signal_strength())