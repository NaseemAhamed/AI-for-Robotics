######################################################################
# This file copyright the Georgia Institute of Technology
#
# Permission is given to students to use or modify this file (only)
# to work on their assignments.
#
# You may NOT publish this file or make it available to others not in
# the course.
#
######################################################################

# These import statements give you access to library functions which you may
# (or may not?) want to use.
from math import *
from glider import *
#from copy import deepcopy


# This is the function you will have to write for part A.
# -The argument 'height' is a floating point number representing
# the number of meters your glider is above the average surface based upon
# atmospheric pressure. (You can think of this as hight above 'sea level'
# except that Mars does not have seas.) Note that this sensor may be off
# a static  amount that will not change over the course of your flight.
# This number will go down over time as your glider slowly descends.
#
# -The argument 'radar' is a floating point number representing the
# number of meters your glider is above the specific point directly below
# your glider based off of a downward facing radar distance sensor. Note that
# this sensor has random Gaussian noise which is different for each read.

# -The argument 'mapFunc' is a function that takes two parameters (x,y)
# and returns the elevation above "sea level" for that location on the map
# of the area your glider is flying above.  Note that although this function
# accepts floating point numbers, the resolution of your map is 1 meter, so
# that passing in integer locations is reasonable.
#
#
# -The argument OTHER is initially None, but if you return an OTHER from
# this function call, it will be passed back to you the next time it is
# called, so that you can use it to keep track of important information
# over time.
#

def estimate_next_pos(height, radar, mapFunc, OTHER=None):
   """Estimate the next (x,y) position of the glider."""
   if OTHER is None:
       P = []
       N = 30000           
    # generate random guessed particles     
       for i in range(N):
          g = glider()
          g.x = random.uniform(-250, 250)
          g.y = random.uniform(-250, 250)
          g.z = height
          g.heading = random.gauss(0,pi/4.0)
          P.append(g)

   
   else:    
      P = OTHER
      N = 1000
      
   # calculate the weights
   W = []
   for i in range(N):
      sigma = 5
      mu = height - radar
#      x = mapFunc(P[i].x, P[i].y) + random.uniform(-10, 10) + random.random()
      x = mapFunc(P[i].x, P[i].y)
      prob = exp(-((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
      W.append(prob)

   
   # resampling
   P3 = []
   index = int(random.random() * N)
   beta = 0.0
   mw = max(W)
   
   P_x = []
   P_y = []


   for i in range(1000):
      beta += random.random() * 2.0 * mw
      while beta > W[index]:
         beta -= W[index]
         index = (index + 1) % N

      g_new = glider()
      g_new.x = P[index].x
      g_new.y = P[index].y
      g_new.z = height
      g_new.heading = random.gauss(0,pi/4.0)
      P3.append(g_new)
      
      P3[i].heading += random.uniform(-0.05, 0.05)
      
      
      P3[i].x += random.gauss(0,5)
      
      
      P3[i].y += random.gauss(0,5)
      
      
      P3[i].glide()
      

      P_x.append(P3[i].x)
      P_y.append(P3[i].y)
#      optionalPointsToPlot.append((P3[i].x, P3[i].y, P3[i].heading))
         
   # averaging the x and y of the particles after resampling
   average_x = sum(P_x)/len(P_x)
   average_y = sum(P_y)/len(P_y)
   x_estimate = average_x
   y_estimate = average_y
   
   xy_estimate = (x_estimate, y_estimate)
 
   OTHER = P3
    
   return xy_estimate, OTHER



def next_angle(height, radar, mapFunc, OTHER=None):
       
   if OTHER is None:
       P = []
       N = 30000
   
# generate random guessed particles
       
       for i in range(N):
          g = glider(random.uniform(-250, 250), random.uniform(-250, 250), height, random.gauss(0.0, pi / 4), mapFunc)  
          g.mapFunc = mapFunc
          P.append(g)
   else:      
       P = OTHER
       N = 1000  
       
 #glide the particles  
#   for p in P:
#       p.glide()
       
# calculate the weights
   W = []  
   for p in P:     
      sigma = 50
      mu = radar
      x = p.z-mapFunc(p.x,p.y)
      
      prob = exp(-((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
      W.append(prob)
        
# resampling    
   n = len(P)
   P_new = []
   index = int(random.random() * n)
   beta = 0.0
   mw = max(W)
    
   for i in range(N):
      beta += random.random() * 2.0 * mw
      while beta > W[index]:
         beta -= W[index]
         index = (index + 1) % n
      g_new = glider(P[index].x, P[index].y, height, P[index].heading, mapFunc)
      P_new.append(g_new)
   P = P_new
 
# fuzz the x, y of the particles
   P_x = []
   P_y = []
   P_h = []  
   
   for p in P:
      p.x = p.x + random.gauss(0,1)
      p.y = p.y + random.gauss(0,1)
      p.heading = p.heading + random.gauss(0, 0.15)
      P_x.append(p.x)
      P_y.append(p.y)
      P_h.append(p.heading)
     

#average the x, y and heading for particles 
      
   average_x = sum(P_x)/len(P_x)
   average_y = sum(P_y)/len(P_y)  
   average_h = sum(P_h)/len(P_h)

   x_estimate = average_x
   y_estimate = average_y
   h_estimate = average_h
   
   
#use atan2 to calculate the steering angle to (0,0) and call the angle_trunc
   steering_angle = angle_trunc(atan2(-y_estimate, -x_estimate) - h_estimate)
   
   
#limit the steering angle for particles   
#   steering = max( -pi/8.0, steering_angle)
#   steering = min( steering_angle, pi/8.0)

#steer the particles for the next iteration
   for p in P:  
      p.glide(steering_angle)
#      p.heading += steering_angle
#      p.heading = angle_trunc(p.heading)
   
   OTHER = P  

   return steering_angle, OTHER
