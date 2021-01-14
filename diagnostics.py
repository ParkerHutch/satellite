import subprocess
from typing import Dict


def get_memory_info(units_arg:str = '--mega') -> Dict[str, str]:
    output = subprocess.check_output(['free', '-w', '--mega'], text=True)
    columns = output.split('Mem:')[0].split()
    numbers = list(map(int, output.split('Mem:')[1].split()))
    return dict(zip(columns, numbers))


if __name__ == '__main__':
    print(get_memory_info())