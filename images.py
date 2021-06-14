"""
Camera Projection library - Image generation
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
from images import *
from projections import *
import numpy as np
from cv2 import cv2
def image(cam:Camera,points:np.ndarray,lines:list,width:int=320,height:int=240,base:np.ndarray=None):
    """
    Generates an image from a list of points and lines connecting them
    """
    img = np.zeros((height,width,3),dtype=np.uint8) if base is None else base
    translation = np.array([width/2,height/2])
    for p in range(len(points)):
        proj = cam.perspective(points[p])
        proj = proj[:2]/proj[2] + translation
        if proj[0]<= 0 or proj[0]>width or proj[1]<0 or proj[1]>height:
            continue
        cv2.circle(img,(int(proj[0]),height-int(proj[1])),1,(0,255,0),2)
    for l in lines:
        A = cam.perspective(points[l[0]])
        A = A[:2]/A[2] + translation
        B = cam.perspective(points[l[1]])
        B = B[:2]/B[2] + translation
        cv2.line(img,(int(A[0]),height-int(A[1])),(int(B[0]),height-int(B[1])),(0,255,0),1)
    return img