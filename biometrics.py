""""
References used: 
https://pdfs.semanticscholar.org/8af6/b870fd1dc3fb703450df39847eef1503d448.pdf
https://github.com/rtshadow/biometrics
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.89.8984&rep=rep1&type=pdf
"""
import cv2
from image_processing import parse_image
import sys
SOLUTION = "input/test0.jpg"
THRESHOLD = 33
#Taken from https://github.com/kjanko/python-fingerprint-recognition/blob/master/app.py#L66
def compare_fingerprints(img1, img2):
	print("Parsing first image")
	keypoints1, des1 = parse_image(img1)
	print("Parsing second ")
	keypoints2, des2 = parse_image(img2)
	
	#Brute force matcher
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
	matches = sorted(bf.match(des1, des2), key= lambda match:match.distance)
	
	score = sum(map(lambda match: match.distance,matches))/len(matches)
	return score < THRESHOLD
	
def check_match(input):
	sol = cv2.imread(SOLUTION, cv2.IMREAD_GRAYSCALE)
	
	if compare_fingerprints(input, sol):
		print("Fingerprints match!")
	else:
		print("Authentication failure")
		
if __name__=="__main__":
	filename = sys.argv[1]
	input = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
	check_match(input)
	