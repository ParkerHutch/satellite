import os
import subprocess
from datetime import datetime
from typing import Dict, List

from picamera import PiCamera

""" 
    fswebcam arguments for image capture and processing
"""
capture_args = [
    '--resolution', '1280x720',
    '--delay', '1'
]
processing_args = [
    '--banner-colour', '#FF0000', 
    '--font', 'sans:20',
    '--no-shadow',
    '--no-subtitle', 
    '--no-info'
]

pi_camera = None
try:
    pi_camera = PiCamera()
except:
    pass

def find_devices(search_range: int = 10) -> Dict[str, int]:
    """Return a dictionary of device names as keys and the corresponding 
    number of inputs (cameras) as values. Only devices that have 1 or more 
    inputs are stored. If the PiCamera is connected, it will not be included in 
    this list.

    Args:
        search_range (int, optional): The number of /dev/video{number} devices
        to check. Defaults to 10.

    Returns:
        dict[str, int]: A dictionary where each key is a device name and each 
        key's corresponding value is the number of inputs associated with the 
        device.
    """

    inputs = {}
    for i in range(search_range):
        device_name = f'/dev/video{i}'
        device_cameras = get_device_inputs(device_name)
        if device_cameras > 0:
            inputs[device_name] = device_cameras 
    
    if pi_camera is not None:
        inputs['RPi Camera Module'] = 1

    return inputs

def get_device_inputs(device_name: str) -> int:
    """Get the number of inputs (cameras) associated with the given video
    device. To find the number of inputs, this function calls fswebcam with the
    --list-inputs flag on the /dev/video{mount_num} device and parses the output
    to find the last input's associated number. For a mount with one camera, the
    parsed output will be '0:Camera 1'. This function interprets the number
    found before the last colon to as the largest camera index. It is assumed
    that there is a valid camera on this mount for every integer value between
    this index and 0, and including 0.

    Args:
        device_name (str): the name of the device to find associated inputs for.

    Returns:
        int: The number of valid inputs connected to the device.
    """

    # Run a command to check the device's inputs and capture the output
    cmd_output = subprocess.check_output(
        [
            'script', '-q', '-c', 
            f'(fswebcam --list-inputs -d {device_name})', 
            '/dev/null'
        ], 
        text=True
    )
    error_messages = [
        'Unable to query input 0.', 
        'No such file or directory', 
        'Message from syslogd@raspberrypi'
    ]
    if any(message in cmd_output for message in error_messages):
        return 0
    else:
        start = 'Available inputs:'
        end = 'No input was specified'
        inputs_found = (cmd_output.split(start)[1]).split(end)[0]
        last_colon_index = inputs_found.rfind(':')
        largest_device_index = int(
            inputs_found[last_colon_index - 1: last_colon_index])
        return largest_device_index + 1

def get_fswebcam_capture_args(device: str, 
                                add_processing: bool, 
                                image_file_path:str) -> List[str]:
    """Generates an array of arguments to add to the 'fswebcam' command to take 
    a picture on the given device and store it in the file given by 
    image_file_path. The capture_args array is used to supply arguments 
    associated with image capture, and the processing_args array is used,
    if add_processing is True, to process the image after it is taken.  

    Args:
        device (str): The name of the device to use to take a picture. An 
        example value could be /dev/video0.
        add_processing (bool): Whether to add image processing effects to photos 
        after capture.
        image_file_path (str): The path and filename of the file to store the
        captured image in.

    Returns:
        List[str]: a list of arguments to use in conjuction with the fswebcam
        command.
    """
    args = ['fswebcam', '-q', '-d', device]
    args.extend(capture_args)
    if add_processing:
        args.extend(processing_args)
        timestamp_text = datetime.now().strftime('%m/%d/%Y %I:%M %p')
        args.extend([
            '--title', f'DEVICE: {device}',
            '--timestamp', timestamp_text
        ]) 
    else:
        args.extend(['--no-banner'])
    args.extend([image_file_path + '.jpg'])
    return args

def take_fswebcam_picture(device: str, add_processing: bool, log_file_path: str, 
                            image_file_path: str):
    """Uses the 'fswebcam' command to take a picture using the given device, 
    storing the image in the given image file path and appending the terminal
    output to the log file given by the log file path.

    Args:
        device (str): The device to use to take a picture.
        add_processing (bool): Whether to add image processing effects to photos 
        after capture.
        log_file_path (str): The path to the file to append logs to. 
        image_file_path (str): The path and filename of the file to store the
        captured image in.
    """

    log_file = open(log_file_path, 'a')
    log_file.write(f'Attempting to take a picture on the {device} device...')
    log_file.flush()
    subprocess.run(get_fswebcam_capture_args(device, add_processing, 
                                                image_file_path), 
                                                stdout=log_file, 
                                                stderr=log_file)

    log_file.write('DONE\n')
    log_file.flush()
    log_file.close()

def prepare_directory(images_directory_path: str): 
    """Sets up the directory with given path so that it can hold incoming
    images. If the folder exists, any file with a image extension (see
    img_extensions array) or 'image' prefix is removed. If the folder doesn't
    exist, it is created. If the given path specifies a file, a warning is
    raised.

    Args:
        images_directory_path (str): The path to the folder that should be 
        prepared to hold images
    """

    # Files with these extensions will be removed
    img_extensions = ['.jpg', '.png']
    if os.path.isdir(images_directory_path):
        files = [ 
            f for f in os.listdir(images_directory_path) 
                if f.startswith('image') or f.endswith(tuple(img_extensions)) 
        ]
        for f in files:
            os.remove(os.path.join(images_directory_path, f))
    elif not os.path.exists(images_directory_path):
        os.makedirs(images_directory_path)
    else:
        print('Error: images directory is actually a file.') # TODO raise exception
    
def capture(camera_device: str = 'all', add_processing: bool = False,
            verbose: bool = False, log_file_path:str = './camera_logs.txt',
            images_directory: str = './images/'):
    """Take a picture using the given device, or on all connected devices, and
    stores the output in the given directory. This function also generates a 
    temporary output file, which will either be stored in the file given by
    log_file_path or deleted on function end if log_file_path is None.

    Args:
        camera_device (str, optional): The device to use to take a photo. If 
        'all' is specified, all detected devices will be used to capture photos. 
        Defaults to 'all'.
        add_processing (bool, optional): Whether to add image processing effects
        to photos after capture. Defaults to False.
        verbose (bool, optional): Whether to show verbose output on stdout. 
        Defaults to False.
        log_file_path (str, optional): The path to the file to store logs in. 
        Defaults to './camera_logs.txt'.
        images_directory (str, optional): The path to the folder to store
        captured images in. Defaults to './images/'.
    """

    prepare_directory(images_directory)

    keep_output = log_file_path is not None
    log_file_path = log_file_path if log_file_path else './camera_logs.txt'
    
    # Clear the camera_log.txt file if it exists
    open(log_file_path, 'w').close()

    picture_num = 0
    if camera_device == 'picamera' or camera_device == 'all':
        if pi_camera is not None:
            pi_camera.capture(images_directory + f'image{picture_num}.jpg')
            picture_num += 1
        elif camera_device == 'picamera':
            print('PiCamera not connected') # TODO raise an exception here
    if camera_device == 'all':
        # Take a picture on all connected cameras, excluding the PiCamera
        for device_name, cameras in find_devices().items():
            if device_name != 'RPi Camera Module':
                for _ in range(cameras):
                    take_fswebcam_picture(
                        device_name, add_processing, log_file_path,
                        images_directory + f'image{str(picture_num)}')
                    picture_num += 1
    elif camera_device.startswith('/dev/video'):
        take_fswebcam_picture(
            camera_device, add_processing, log_file_path, 
            images_directory + 'image')
    else:
        print(f'device {camera_device} is not supported')
    
    if verbose:
        print('Camera Logs:')
        with open(log_file_path, 'r') as log_file:
            print(log_file.read())
    if not keep_output:
        os.remove(log_file_path)

def stop():
    """Close the PiCamera if it was initialized."""
    if pi_camera is not None:
        pi_camera.close()
