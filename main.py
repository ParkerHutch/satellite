import snapshot
import email_handler

#TODO make the images directory, if it doesn't exist errors occur
snapshot.take_picture()
snapshot.stop()

email_handler.send_email('images/')