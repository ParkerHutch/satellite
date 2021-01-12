import time
import sys
from typing import List
#import snapshot
import email_handler

single_dash_args = ['v', 'q']
long_arg_equivalents = {
    'verbose': 'v',
    'quiet': 'q'
}
def parse_args(args: List[str]):
    parsed_args = []
    raw_args = args[1:] # remove filename
    for flag in raw_args:
        if flag.startswith('--'):
            long_arg = flag[2:]
            short_arg_equivalent = long_arg_equivalents.get(long_arg, None)
            print(f'Got long arg {long_arg}, short equivalent is {short_arg_equivalent}')
            if short_arg_equivalent and (not short_arg_equivalent in parsed_args):
                parsed_args.extend(short_arg_equivalent)
        elif flag.startswith('-'): # Parse single dash args
            flag_chars = flag[1:]
            for character in flag_chars:
                print(f'got short arg {character}')
                if character in single_dash_args:
                    if not character in parsed_args:
                        parsed_args.extend(character)
                else: 
                    print('invalid argument:', character) # TODO raise exception
        else:
            pass # TODO raise an exception for invalid argument
    return parsed_args

def main():
    print('args:', sys.argv)
    print('parsed args: ', parse_args(sys.argv))
    capture_start = time.time()
    #snapshot.take_picture()
    capture_end = time.time()
    print(f'taking pictures took {capture_end-capture_start} seconds')
    #snapshot.stop()

    email_start = time.time()
    #email_handler.send_email('images/')
    email_end = time.time()
    print(f'Sending email took {email_end - email_start} seconds')

if __name__ == '__main__':
    print('running main method')
    main()