#!/usr/bin/env python

#Rospy and Sub/Pub Libraries
import rospy
import geometry_msgs
from geometry_msgs.msg import Point
import sensor_msgs
from sensor_msgs.msg import CompressedImage

#Synthetic Data Libraries
import scipy.stats as stats
import numpy as np


#Matplotlib Libraries
import matplotlib.pyplot as plt

#Computer Vision Libraries
import cv2
from cv_bridge import CvBridge, CvBridgeError


class LocateBall:
	x = 0
	y = 0
	z = 0
	circles = [[],False]
	sim = False
	
	def __init__(self,simulator=False):
		#Setup pubs and subs
		self.pub = rospy.Publisher('/ball_loc',Point,queue_size=1)
		if not simulator:
			img = rospy.Subscriber("/raspicam_node/image/compressed", CompressedImage,self.ImgCallback)
		else:
			img = rospy.Subscriber("/usb_cam/image/compressed",CompressedImage,locate_ball)
		self.sim = simulator

		#First step is to init bridge class through CV
		self.bridge = CvBridge()

	def ImgCallback(self,CVData):
		curr_img = self.bridge.compressed_imgmsg_to_cv2(CVData, "bgr8")
		
		#processing here
		assert LocCircles(curr_img)
		
		
	def LocCircles(self,img):
		#processed image
		pimg = cv2.medianBlur(img,5)
		circs = cv2.HoughCircles(pimg,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=60,minRadius=20,maxRadius=0)
		
		if circs is not None:
			clist = np.uint16(np.around(circles))
			
			for ii in circles[0,:]:
				cv2.circle(pimg,(ii[0],ii[1]),ii[2],(0,255,0),2)
				cv2.circle(pimg,(ii[0],ii[1]),2,(0,0,255),3)
				
			coords = clist[0][0]
			h,w = pimg.shape[:2]
			self.x = coords[0]/float(w)
			self.y = coords[1]/float(h)
			self.z = coords[2]/(float(w)*float(h))
				
			return True
		else:
			print('No Circles Found')
			
			return False
			
	def pub_coord(self):
		self.pub.publish(Point(self.x,self.y,self.z))
		
if __name__ == '__main__':
	try:
		mainFind = LocateBall()
		
		rospy.init_node('BallLocate')
		rate = rospy.Rate(30)
		
		while not rospy.is_shutdown():
			if mainFind.circles[1] != False:
				mainFind.pub_coord()
			else:
				print('No Circles In FOV')
			rate.sleep()
		cv2.destroyAllWindows()
	except rospy.ROSInterruptException:
		pass

#Below is not used anymore! But keeping so can move into external library
#Can also integrate with webcam code/simulator to make a synthetic flow
def gen_synth_IMG():
	#define our image
	#ball_img = np.zeros((800,600),dtype=np.uint8)

	ball_img = np.random.normal(10,5,size=(800,600))
	#Add in a noisy sphere
	rcent = np.random.uniform(0,1,size=(2))
	rcent[0] = int(rcent[0] * 800)
	rcent[1] = int(rcent[1] * 600)

	rcent = rcent.astype(int)
	rrad = np.abs(int(np.random.normal(10,30)))
	rr,cc,val = circle_perimeter_aa(rcent[0],rcent[1],rrad)
	rr[rr>800] = 800
	ball_img[rr,cc] = val * 255

	plt.figure()
	plt.imshow(ball_img)
	plt.show()

	return ball_img
