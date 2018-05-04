import cv2
import imutils
import numpy as np
KERNEL_SIZE = 3
SIGMA = 7
LAMBDA = 8
GAMMA = .02
PSI = 0


def read_image(filepath):
	return cv2.imread(filepath,0)

	
	
def binarize(image, delta=20):
	
	equalized = cv2.equalizeHist(image)

	gaborKernels = [cv2.getGaborKernel((KERNEL_SIZE,KERNEL_SIZE), SIGMA, theta, LAMBDA,GAMMA,PSI,cv2.CV_32F) for theta in range(0,360, delta)]
	filtered = [cv2.filter2D(image, cv2.CV_32F, kernel) for kernel in gaborKernels]
	
	#although the gabor kernels are checked against several finger orientations, for now I know the angle is 0
	return filtered[0]

#Skeletonization/thinning algorithm taken from https://stackoverflow.com/questions/33095476/is-there-any-build-in-function-can-do-skeletonization-in-opencv
def skeletonize(image):
	size = np.size(image)
	skel = np.zeros(image.shape,np.uint8)
	
	ret, img = cv2.threshold(image, 127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
	element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
	done = False
	while (not done):
		eroded = cv2.erode(image,element)
		temp = cv2.dilate(eroded,element)
		temp = cv2.subtract(image,temp)
		skel = cv2.bitwise_or(skel,temp)
		image = eroded.copy()

		zeros = size - cv2.countNonZero(image)
		if zeros==size:
			done = True
	#invert image
	return cv2.bitwise_not(skel)

	
#https://github.com/kjanko/python-fingerprint-recognition/blob/master/app.py#L66
def get_keypoints(image):
	harris_corners = cv2.cornerHarris(image,3,3,.04)
	harris_corners = cv2.normalize(harris_corners,0,255, norm_type=cv2.NORM_MINMAX,dtype=cv2.CV_32FC1)
	keypoints = []
	for i, row in enumerate(harris_corners):
		for j, value in enumerate(row):
			if value > 125:
				keypoints.append(cv2.KeyPoint(j, i, 1))
				
	#features = list(filter(lambda x: x > 125, harris_corners.flatten()))

	orb = cv2.ORB_create()
	return (keypoints, orb.compute(image,keypoints)[1])
	#https://docs.opencv.org/3.4.1/d1/d89/tutorial_py_orb.html 
	
	
def parse_image(image):
	binarized = binarize(image)
	skeletonized = skeletonize(image)
	
	return get_keypoints(skeletonized)
	
	
if __name__ == "__main__":
	image = read_image("input/test0.jpg")
	#binarized = binarize(image)
	#skeletonized = skeletonize(image)
	#cv2.imwrite('output/skeleton.jpg',skeletonized)
	#keypoints, descriptors = get_keypoints(skeletonized)
	keypoints, descriptors = parse_image(image)
	kp_image = cv2.drawKeypoints(image, keypoints, outImage=None)
	cv2.imwrite('output/keypoints.jpg', kp_image)