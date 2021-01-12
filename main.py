import time
import snapshot
import email_handler

capture_start = time.time()
snapshot.take_picture()
capture_end = time.time()
print(f'taking pictures took {capture_end-capture_start} seconds')
snapshot.stop()

email_start = time.time()
email_handler.send_email('images/')
email_end = time.time()
print(f'Sending email took {email_end - email_start} seconds')