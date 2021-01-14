import subprocess

if __name__ == '__main__':
    output = subprocess.check_output(['free', '-w', '--mega'], text=True)
    columns = output.split('Mem:')[0].split()
    numbers = output.split('Mem:')[1].split()
    memory_info = dict(zip(columns, numbers))
    print(memory_info)