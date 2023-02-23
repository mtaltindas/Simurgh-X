import numpy as np
from numpy import sin, cos, arccos, pi, round
from .latloncalc import getDistanceBetweenPointsNew

#heading değişkeni de olacak?
#TODO: dünyanın yarıçapına göre formül,chrome bookmarklarında var.


def rad2deg(radians):
    degrees = radians * 180 / pi
    return degrees

def deg2rad(degrees):
    radians = degrees * pi / 180
    return radians

def simurgh_estimate(startPixel,endPixel,delTime):
    heading=90#dummyvar
    calibrationConst=10#dummyvar
    meter2angleLat=(8.99*(10**-6))
    meter2angleLon=(1.17*(10**-5))
    delPixel=endPixel-startPixel
    calibratedMeter=delPixel*calibrationConst



    if (heading<=90):
        #koordinat I
        #sin theta -> boylam değişimi(LONGITUDE)
        #cos theta -> enlem değişimi(LATITUDE)
        latAngleAdj=cos(deg2rad(heading))#gives north direction component
        lonAngleAdj=sin(deg2rad(heading))#gives east direction component
       
    elif(heading>90 and heading<=180):
        #koordinat II
        heading=heading-90
        #cos theta ->boylam
        #sintheta  ->enlem
        latAngleAdj=(-1)*sin(deg2rad(heading))#south direction component
        lonAngleAdj=cos(deg2rad(heading))#east direction component
    
    elif(heading>180 and heading<270):
        #koordinat III
        heading=heading-180
        #sin theta ->boylam
        #cos theta -> enlem
        latAngleAdj=(-1)*cos(deg2rad(heading))#south direction component
        lonAngleAdj=(-1)*sin(deg2rad(heading))#west direction component
        
    elif(heading>270 and heading<360):
        #koordinat IV
        heading=heading-270
        #cos theta ->boylam
        #sintheta -> enlem
        latAngleAdj=sin(deg2rad(heading))#north direction component
        lonAngleAdj=(-1)*cos(deg2rad(heading))#west direction component
    
    # Enlem  -> Latitude -> X axis 0.0001 difference 11.1227 meters
    # Boylam -> Longitude -> Y axis       difference 8.5210 meters
    #           LatLon Constant* Angle Cosine/Sine* Camera Calibrated Meter Value
    delLatitude= latAngleAdj*calibratedMeter*meter2angleLat
    delLongitude= lonAngleAdj*calibratedMeter*meter2angleLon

    return delLatitude,delLongitude



    #mesafe / zaman ile hızı tespit et kontrol et uygunsuz değeri basma be aga
    #endPixel-startPixel== metre cinsinden olarak ortantıla bu farkı
    #delTime hız hesaplaması için
