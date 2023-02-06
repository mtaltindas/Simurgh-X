import numpy as np
from numpy import sin, cos, arccos, pi, round
from .latloncalc import getDistanceBetweenPointsNew

#heading değişkeni de olacak?
heading=0#I ASSUMED AS A DEGREE OF ANGLE
def simurgh_estimate(startPixel,endPixel,delTime):
    estimatedLocation=np.array((-1,-1),dtype=np.float32)

 


    if (heading<=90):
        #koordinat I
        #sin theta -> boylam değişimi
        #cos theta -> enlem değişimi
        pass
    elif(heading>90 and heading<=180):
        #koordinat II
        heading=heading-90
        #cos theta ->boylam
        #sintheta -> enlem

        
    elif(heading>180 and heading<270):
        #koordinat III
        heading=heading-90
        #sin theta ->boylam
        #cos theta -> enlem
        pass
    elif(heading>270 and heading<360):
        #koordinat IV
        heading=heading-270
        #cos theta ->boylam
        #sintheta -> enlem
        pass
    return estimatedLocation



    #mesafe / zaman ile hızı tespit et kontrol et uygunsuz değeri basma be aga
    #endPixel-startPixel== metre cinsinden olarak ortantıla bu farkı
    #delTime hız hesaplaması için
