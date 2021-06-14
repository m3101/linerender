"""
Camera Projection library - Projections
Copyright (C) 2021 Amélia O. F. da S.
<a.mellifluous.one@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
For all calculations, the coordinate system used is the same as
depicted in Hartley & Zisserman's "Multiple View Geometry".
Row notation was used for matrices (row = vector) for simpler integration
with Numpy.
"""

"""
These methods are not at all optimised and were developed without
using direct references as an attempt to build a renderer fully from
memory and consolidating that knowledge, so there are bits (the rotations
in the camera constructor, for example) where redundant and unnecessary steps
are separated as a way to make it easier to think visually about
what's going on (which for me is the only way to do this at all :p)
"""

import numpy as np
from numpy.lib import math
class Camera():
    def __init__(self,position:np.ndarray,direction:np.ndarray,roll:float,f_dist:float):
        """
        Camera Object

        Takes the following arguments:

        * position: Vector pointing to the camera's origin
        * direction: Versor indicating the camera's direction.
        * roll: Angle (radians) between the camera's x axis and the world's
        * f_dist: Camera's focal distance
        """
        self.calibrate(position,direction,roll,f_dist)
    def calibrate(self,position:np.ndarray,direction:np.ndarray,roll:float,f_dist:float):
        """
        Calibration

        Takes the following arguments:

        * position: Vector pointing to the camera's origin
        * direction: Versor indicating the camera's direction.
        * roll: Angle (radians) between the camera's x axis and the world's
        * f_dist: Camera's focal distance
        """
        self.translation = position
        
        #Rotation matrix calculation
        
        #Our new Z axis will run along the direction vector
        nZ = direction
        nZ = nZ/np.linalg.norm(nZ)
        #Our X axis will be  Y X nZ
        nX = np.cross([0,1,0],nZ)
        nX = nX/np.linalg.norm(nX)
        #Our Y axis will be nZ X nX
        nY = np.cross(nZ,nX)
        nY = nY/np.linalg.norm(nY)

        mainRot = np.array(
            [nX,nY,nZ]
        )

        #The camera roll is another rotation on the XY plane
        #The new X axis goes to (cos(roll),-sin(roll),0)
        #The new Y axis goes to (sin(roll),cos(roll))
        rolltation = np.array([
            [math.cos(roll),-math.sin(roll),0],
            [math.sin(roll),math.cos(roll),0],
            [0,0,1]
        ])
        #I prefer representing it as a clockwise rotation
        rolltation = np.linalg.inv(rolltation)

        self.rotation = np.dot(mainRot,rolltation)

        fund = np.zeros((4,4))
        fund[0:3,0:3] = self.rotation.T
        fund[:3,2] = -position
        fund[2,2] = 1
        self.fundamental = fund.T
        self.position = position
        self.f_dist=f_dist

        self.projection = np.dot(fund.T,(np.append(np.identity(3),[[0,0,0]],axis=0)*f_dist))
    def perspective(self,point:np.ndarray)->np.ndarray:
        """
        Projects a 3d (homogeneous coordinates) point
        into 2d (homogeneous coordinates) point on the screen
        """
        return (np.dot(point[:3]-self.position,np.linalg.inv(self.rotation)))*np.array([1,1,1/self.f_dist])