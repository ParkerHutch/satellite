import time
import sys
import argparse
from typing import List
import snapshot
import email_handler

parser = argparse.ArgumentParser(description='Use a device to capture and send photos')
parser.add_argument('-v', '--verbose', 
                    help='show output when running the program', action='store_true')
parser.add_argument('-p', '--process-images', 
                    help='add image processing to captured images', action='store_true')
parser.add_argument('-n', '--no-email', help="don't email the images after capture", action='store_true')
parser.add_argument('-d', '--device',
                    help="which device to use for capturing photos (specify 'all' to use all devices)", 
                    type=str, default='all')
parser.add_argument('-l', '--list-devices',
                    help='list all detected devices and quit', action='store_true')
parser.add_argument('-o', '--output', type=str, default=None, metavar='FILE',
                        help='output logs to the given file')

def main():
    args = parser.parse_args()
    
    if args.list_devices:
        print('Connected Devices'.center(31, '-'))
        print('Device Name\t\tCameras')
        for device, cameras in snapshot.find_devices().items():
            print(f'{device}\t\t{cameras}')
        
    else:
        capture_start = time.time()
        snapshot.capture(camera_device=args.device, 
                            add_processing=args.process_images, 
                            verbose=args.verbose,
                            log_file_path=args.keep_output
        )
        capture_end = time.time()
        if args.verbose:
            print(f'Taking pictures: \t{int(capture_end-capture_start)} seconds')
        

        if not args.no_email:
            email_start = time.time()
            email_handler.send_email('images/', verbose=args.verbose)
            email_end = time.time()
            if args.verbose:
                print(f'Sending email: \t\t{int(email_end - email_start)} seconds')
        
        snapshot.stop()

if __name__ == '__main__':
    main()