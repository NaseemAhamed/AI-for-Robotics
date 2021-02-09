
from builtins import object
import random
import numpy as np


class Pilot(object):

    def __init__(self, min_dist, in_bounds):
        self.min_dist = min_dist
        self.in_bounds = in_bounds
        
        self.dict_x = {}
        self.dict_p = {}
#        self.l = []
      
    def observe_asteroids(self, asteroid_locations):
        """ self - pointer to the current object.
           asteroid_locations - a list of asteroid observations. Each 
           observation is a tuple (i,x,y) where i is the unique ID for
           an asteroid, and x,y are the x,y locations (with noise) of the
           current observation of that asteroid at this timestep.
           Only asteroids that are currently 'in-bounds' will appear
           in this list, so be sure to use the asteroid ID, and not
           the position/index within the list to identify specific
           asteroids. (The list may change in size as asteroids move
           out-of-bounds or new asteroids appear in-bounds.)

           Return Values:
                    None
        """
        global observe
        observe = asteroid_locations
        
            
        
#        l =  [(i, Asteroid.a_x, Asteroid.b_x, Asteroid.a_y, Asteroid.b_y)
#                  for i in enumerate(AsteroidField.asteroids)]
        
        pass

    def next_move(self, craft_state):
        """ self - a pointer to the current object.
            craft_state - implemented as CraftState in craft.py.

            return values: 
              angle change: the craft may turn left(1), right(-1), 
                            or go straight (0). 
                            Turns adjust the craft's heading by 
                             angle_increment.
              speed change: the craft may accelerate (1), decelerate (-1), or 
                            continue at its current velocity (0). Speed 
                            changes adjust the craft's velocity by 
                            speed_increment, maxing out at max_speed.
         """

        return random.randint(-1,1), random.randint(-1,1)

    def estimate_asteroid_locs(self):
        """ Should return an itterable (list or tuple for example) that 
            contains data in the format (i,x,y), consisting of estimates 
            for all in-bound asteroids. """
        
        x_est = ()
        b_x = -0.0024204559705969754
        b_y = 0.00022549442737217033 
        a_y = -4.8216649941407335e-05 
        a_x = -1.5557814847495184e-05
        
        for k in observe:
            if k[0] not in self.dict_x:
                self.dict_x[k[0]] = np.matrix([[k[1]], [b_x], [a_x], [k[2]], [b_y], [a_y]])
            if k[0] not in self.dict_p:
                self.dict_p[k[0]] = np.matrix([[1., 0., 0., 0., 0., 0.], [0., 1., 0., 0., 0., 0.], [0., 0., 1., 0., 0., 0.], [0., 0., 0., 1., 0., 0.], [0., 0., 0., 0., 1., 0.], [0., 0., 0., 0., 0., 1.]])
        
        for k in observe:
                            
            x = self.dict_x[k[0]]
            P = self.dict_p[k[0]]
            F = np.matrix([[1., 1., 1., 0., 0., 0.], [0., 1., 1., 0., 0., 0.], [0., 0., 1., 0., 0., 0.], [0., 0., 0., 1., 1., 1.], [0., 0., 0., 0., 1., 1.], [0., 0., 0., 0., 0., 1.]]) 
            H = np.matrix([[1., 0., 0., 0., 0., 0.], [0., 1., 0., 0., 0., 0.], [0., 0., 1., 0., 0., 0.], [0., 0., 0., 1., 0., 0.], [0., 0., 0., 0., 1., 0.], [0., 0., 0., 0., 0., 1.]])
            R = np.matrix([[1., 0., 0., 0., 0., 0.], [0., 1., 0., 0., 0., 0.], [0., 0., 1., 0., 0., 0.], [0., 0., 0., 1., 0., 0.], [0., 0., 0., 0., 1., 0.], [0., 0., 0., 0., 0., 1.]])
            I = np.matrix([[1., 0., 0., 0., 0., 0.], [0., 1., 0., 0., 0., 0.], [0., 0., 1., 0., 0., 0.], [0., 0., 0., 1., 0., 0.], [0., 0., 0., 0., 1., 0.], [0., 0., 0., 0., 0., 1.]])
            
            
             # prediction
            x = F * x 
            P = F * P * F.transpose()
            
            # measurement update
            Z = np.matrix([[k[1]], [0.], [0.], [k[2]], [0.], [0.]])
            y = Z - (H * x)
            S = H * P * H.transpose() + R
            K = P * H.transpose() * np.linalg.inv(S)
            x = x + K * y
            P = (I - K * H) * P
            
            self.dict_x[k[0]] = x
            self.dict_p[k[0]] = P
            
            x_est+=((k[0],x[0],x[3]),)
            
        return x_est