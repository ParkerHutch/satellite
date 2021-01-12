import snapshot
import email_handler

#TODO time how long these functions take
import time
start = time.time()
snapshot.take_picture()
end = time.time()
print(f'timing took {start-end} seconds ')
snapshot.stop()

email_handler.send_email('images/')