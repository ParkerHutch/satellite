import snapshot
import email_handler

print('taking picture')
snapshot.take_picture('picamera', 'images/')
snapshot.stop()
print('done')

email_handler.send_email('images/image.jpg')