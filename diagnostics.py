import subprocess

if __name__ == '__main__':
    output = subprocess.check_output(['free', '-w'], text=True)
    numbers = output.split('Mem:')[1].split()
    print(f'Memory used: {numbers[0]} Available: {numbers[1]}')
    #print(output)