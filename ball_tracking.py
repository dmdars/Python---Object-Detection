# USAGE
# python ball_tracking.py

# this is the program to track an orange ball and an obstacle with mostly black colored object.
# to close the program press 'q'

# import the necessary packages
from imutils.video import VideoStream
import cv2
import imutils
import time


def nothing(x):
	pass

# define the lower and upper boundaries of the "orange"
hlo = 0
slo = 189
vlo = 75
huo = 17
suo = 255
vuo = 255

# define the lower and upper boundaries of the "black"
hlb = 0
slb = 0
vlb = 0
hub = 180
sub = 255
vub = 30

# grab the reference to the webcam
vs = VideoStream(src=0).start()

# allow the camera or video file to warm up
time.sleep(2.0)

#create trackbar for hsv filter for orange
cv2.namedWindow('trackbar for orange')
cv2.createTrackbar('hlo','trackbar for orange',hlo,255,nothing)
cv2.createTrackbar('slo','trackbar for orange',slo,255,nothing)
cv2.createTrackbar('vlo','trackbar for orange',vlo,255,nothing)
cv2.createTrackbar('huo','trackbar for orange',huo,255,nothing)
cv2.createTrackbar('suo','trackbar for orange',suo,255,nothing)
cv2.createTrackbar('vuo','trackbar for orange',vuo,255,nothing)

# keep looping
while True:
	# grab the current frame
	frame = vs.read()

	# handle the frame from VideoCapture or VideoStream

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break

	#set the trackbar for orange
	orangeLower = (hlo, slo, vlo)
	orangeUpper = (huo, suo, vuo)

	#set the trackbar for black
	blackLower = (hlb, slb, vlb)
	blackUpper = (hub, sub, vub)


	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=640, height=480)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)


	# construct a mask for the color "orange" and "black", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask1 = cv2.inRange(hsv, orangeLower, orangeUpper)
	mask1 = cv2.erode(mask1, None, iterations=2)
	mask1 = cv2.dilate(mask1, None, iterations=2)

	mask2 = cv2.inRange(hsv, blackLower, blackUpper)
	mask2 = cv2.erode(mask2, None, iterations=2)
	mask2 = cv2.dilate(mask2, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts1 = imutils.grab_contours(cnts1)
	center1 = None
	
	# find contours in the mask and initialize the current
	# (x, y) center of the dummy
	cnts2 = cv2.findContours(mask2.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts2 = imutils.grab_contours(cnts2)
	center2 = None

	# msg[0]="Start"
	# only proceed if at least one contour was found
	if len(cnts1) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c1 = max(cnts1, key=cv2.contourArea)
		((x1, y1), radius) = cv2.minEnclosingCircle(c1)
		M1 = cv2.moments(c1)
		center = (int(M1["m10"] / M1["m00"]), int(M1["m01"] / M1["m00"]))
		coorX1 = int(M1["m10"] / M1["m00"])
		coorY1 = int(M1["m01"] / M1["m00"])

		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x1), int(y1)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)


	# only proceed if at least one contour was found
	if len(cnts2) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c2 = max(cnts2, key=cv2.contourArea)
		(x2, y2, w, h) = cv2.boundingRect(c2)
		M2 = cv2.moments(c2)
		coorX2 = int(M2["m10"] / M2["m00"])
		coorY2 = int(M2["m01"] / M2["m00"])

		# only proceed if the radius meets a minimum size
		if w > 20:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.rectangle(frame, (x2, y2), (x2 + w, y2 + h), (0, 255, 0), 2)
			
	# show the result frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	#update data hsv for orange
	hlo = cv2.getTrackbarPos('hlo','trackbar for orange')
	slo = cv2.getTrackbarPos('slo','trackbar for orange')
	vlo = cv2.getTrackbarPos('vlo','trackbar for orange')
	huo = cv2.getTrackbarPos('huo','trackbar for orange')
	suo = cv2.getTrackbarPos('suo','trackbar for orange')
	vuo = cv2.getTrackbarPos('vuo','trackbar for orange')

	
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break


# close all windows
cv2.destroyAllWindows()