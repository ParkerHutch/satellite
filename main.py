import time
import sys
import argparse
from typing import List
import snapshot
import email_handler

parser = argparse.ArgumentParser(description='Use a device to capture and send photos')
parser.add_argument('-v', '--verbose', 
                    help="show output when running the program", action='store_true')
parser.add_argument('-p', '--process-images', 
                    help="add image processing to captured images", action='store_true')
parser.add_argument('--no-email', help="don't email the images after capture", action='store_true')
parser.add_argument('-d', '--device',
                    help='which device to use for capturing photos (specify all to use all devices)', 
                    type=str, default='all')
parser.add_argument('-l', '--list-devices',
                    help='list all detected devices and quit', action='store_true')

def main():
    args = parser.parse_args()
    
    if args.list_devices:
        print('Connected devices'.center(30, '-'))
        print('Device Name\t\tCameras')
        for device, cameras in snapshot.find_devices().items():
            print(f'{device}\t\t{cameras}')
        
    else:
        capture_start = time.time()
        snapshot.capture(camera_device=args.device, 
                            add_processing=args.process_images, 
                            verbose=args.verbose)
        capture_end = time.time()
        if args.verbose:
            print(f'Taking pictures: \t{capture_end-capture_start} seconds')
        snapshot.stop()

        if not args.no_email:
            email_start = time.time()
            email_handler.send_email('images/')
            email_end = time.time()
            if args.verbose:
                print(f'Sending email: \t\t{email_end - email_start} seconds')

if __name__ == '__main__':
    main()