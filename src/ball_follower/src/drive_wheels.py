#!/usr/bin/env python
#Vineet Tiruvadi
#Lab 2 for Intro Robotics

import rospy
from geometry_msgs.msg import Twist, Point
import numpy as np

import sys, select, termios, tty

class Driver:
	sendVel = np.array([0,0,0])
	
	def __init__(self):
		self.ballSub = rospy.Subscriber("/ball_loc",Point,self.mover)
		self.VelPub = rospy.Publisher("/cmd_vel",Twist,queue_size=5)
	
	def mover(self,inPoint):
		
		#INPUT HERE IS A POINT
		inCoord = np.array(inPoint)
		#Check if the point we're looking for is normalized
		assert inCoord.any() <= 1
		
		inX = inPoint.x
		#Center to the screen
		inX = inX - 0.5
		
		#since we're JUST TURNING FOR NOW, we'll focus on the x coord
		targ = inX
		
		t_av = 0
		
		#set target_angular_vel; still just velocity
		t_av += np.sign(targ) * 0.1
		
		#is target Ang Vel > control ang vel?
		c_av = min(t_av,c_av + 0.1/4.0)
		
		twist=Twist()
		#We don't care about linear twist yet
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0;
		twist.angular.x = 0;twist.angular.y;twist.angular.z = c_av
		self.pub_vel(twist)
		
	def pub_vel(self,twist):
		self.VelPub.publish(twist)
		
		
if __name__== "__main__":
	try:
		rospy.init_node('WheelDriver')
		mainDrv = Driver()
		rate = rospy.Rate(30)
		
		while not rospy.is_shutdown():
			rate.sleep()
	except rospy.ROSInterruptException:
		pass
		
