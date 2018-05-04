
from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image
import numpy as np
import cv2
from biometrics import check_match
#Taken directly from https://picamera.readthedocs.io/en/release-1.13/recipes1.html

def take_photo():
	camera.start_preview()
	sleep(5)
	camera.capture()
	stream = BytesIO()
	camera = PiCamera()
	camera.start_preview()
	sleep(2)
	camera.capture(stream, format='jpeg')
	# "Rewind" the stream to the beginning so we can read its content
	stream.seek(0)
	image = Image.open(stream)
	
	#https://stackoverflow.com/questions/46624449/load-bytesio-image-with-opencv
	file_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
	return cv2.imdecode(file_bytes, cv.IMREAD_COLOR)
	
if __name__ == "__main__":
	input = take_photo()
	check_match(input)
	
