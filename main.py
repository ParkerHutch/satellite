import snapshot
import email_handler

print('taking picture')
snapshot.take_picture('picamera', 'images/') #TODO make this directory, if it doesn't exist errors occur
snapshot.stop()
print('done')

email_handler.send_email('images/')