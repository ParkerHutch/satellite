import subprocess

if __name__ == '__main__':
    output = subprocess.check_output(
        ['awk', '/^Mem/ {print $3}', '<(free -m)'])
    print(output)