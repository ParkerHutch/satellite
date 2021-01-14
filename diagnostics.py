import subprocess
from typing import Dict


def get_memory_info(units_arg:str = '--mega') -> Dict[str, str]:
    output = subprocess.check_output(['free', '-w', '--mega'], text=True)
    
    column_headers = output.split('Mem:')[0].split()[:7]
    numbers = list(map(int, 
                        output.split('Mem:')[1].split()[:len(column_headers)]))
    return dict(zip(column_headers, numbers))


if __name__ == '__main__':
    print(get_memory_info())