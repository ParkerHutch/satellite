import snapshot
import email_handler

print('taking picture')
snapshot.take_picture('webcam', 'images/image.jpg')
snapshot.stop()

email_handler.send_email('images/image.jpg')