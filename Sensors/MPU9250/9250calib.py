import os
import sys
import time
import smbus
import numpy as np

from imusensor.MPU9250 import MPU9250
'''
def caliberateAccelerometer(self):
  """Caliberate Accelerometer by positioning it in 6 different positions
  This function expects the user to keep the imu in 6 different positions while caliberation. 
  It gives cues on when to change the position. It is expected that in all the 6 positions, 
  at least one axis of IMU is parallel to gravity of earth and no position is same. Hence we 
  get 6 positions namely -> +x, -x, +y, -y, +z, -z.
  """

  currentAccelRange = self.AccelRange
  currentFrequency = self.Frequency
  currentSRD = self.CurrentSRD
  self.setAccelRange("AccelRangeSelect2G")
  self.setLowPassFilterFrequency("AccelLowPassFilter20")
  self.setSRD(19)

  xbias = []
  ybias = []
  zbias = []
  xscale = []
  yscale = []
  zscale = []

  print ("Acceleration calibration is starting and keep placing the IMU in 6 different directions based on the instructions below")
  time.sleep(2)
  for i in range(6):
    print ("Put the IMU in {0} position".format(i+1))
    time.sleep(3)
    meanvals = self.__getAccelVals()
    print (meanvals)
    xscale, xbias = self.__assignBiasOrScale(meanvals[0], xscale, xbias)
    yscale, ybias = self.__assignBiasOrScale(meanvals[1], yscale, ybias)
    zscale, zbias = self.__assignBiasOrScale(meanvals[2], zscale, zbias)
    print (xscale)
    print (yscale)
    print (zscale)

  if len(xscale) != 2 or len(yscale) != 2 or len(zscale) != 2:
    print ("It looks like there were some external forces on sensor and couldn't get proper values. Please try again")
    return


  self.AccelBias[0] = -1*(xscale[0] + xscale[1])/(abs(xscale[0]) + abs(xscale[1]))
  self.AccelBias[1] = -1*(yscale[0] + yscale[1])/(abs(yscale[0]) + abs(yscale[1]))
  self.AccelBias[2] = -1*(zscale[0] + zscale[1])/(abs(zscale[0]) + abs(zscale[1]))

  self.AccelBias = -1*self.cfg.Gravity*self.AccelBias

  self.Accels[0] = (2.0*self.cfg.Gravity)/(abs(xscale[0]) + abs(xscale[1]))
  self.Accels[1] = (2.0*self.cfg.Gravity)/(abs(yscale[0]) + abs(yscale[1]))
  self.Accels[2] = (2.0*self.cfg.Gravity)/(abs(zscale[0]) + abs(zscale[1]))

  self.setAccelRange(currentAccelRange)
  self.setLowPassFilterFrequency(currentFrequency)
  self.setSRD(currentSRD)

def __getScale(self, scale):
  if len(scale) == 0:
    return 1
  else:
    return sum(scale)/(2*self.cfg.Gravity)

def __assignBiasOrScale(self, val, scale, bias):

  if val > 6.0 or val < -6.0 :
    scale.append(val)
  else:
    bias.append(val)
  return scale, bias


def __getAccelVals(self):

  accelvals = np.zeros((100,3))
  for samples in range(1,100):
    self.readSensor()
    vals = self.AccelVals/self.Accels + self.AccelBias
    accelvals[samples] = vals
    time.sleep(0.02)
  meanvals = np.array([accelvals[:,0].mean(), accelvals[:,1].mean(), accelvals[:,2].mean()])
  return meanvals


def caliberateMagApprox(self):
  """Caliberate Magnetometer
  This function uses basic methods like averaging and scaling to find the hard iron
  and soft iron effects.
  Note: Make sure you rotate the sensor in 8 shape and cover all the 
  pitch and roll angles.
  """

  currentSRD = self.CurrentSRD
  self.setSRD(19)
  numSamples = 1000
  magvals = np.zeros((numSamples,3))
  for sample in range(1,numSamples):
    self.readSensor()
    magvals[sample] = self.MagVals/self.Mags + self.MagBias
    time.sleep(0.02)
  minvals = np.array([magvals[:,0].min(), magvals[:,1].min(), magvals[:,2].min()])
  maxvals = np.array([magvals[:,0].max(), magvals[:,1].max(), magvals[:,2].max()])

  self.MagBias = (minvals + maxvals)/2.0
  averageRad = (((maxvals - minvals)/2.0).sum())/3.0
  self.Mags = ((maxvals - minvals)/2.0)*(1/averageRad)

  self.setSRD(currentSRD)

def caliberateMagPrecise(self):
  """Caliberate Magnetometer Use this method for more precise calculation
  This function uses ellipsoid fitting to get an estimate of the bias and
  transformation matrix required for mag data
  Note: Make sure you rotate the sensor in 8 shape and cover all the 
  pitch and roll angles.
  """

  currentSRD = self.CurrentSRD
  self.setSRD(19)
  numSamples = 1000
  magvals = np.zeros((numSamples,3))
  for sample in range(1,numSamples):
    self.readSensor()
    magvals[sample] = self.MagVals/self.Mags + self.MagBias
    time.sleep(0.05)
  centre, evecs, radii, v = self.__ellipsoid_fit(magvals)

  a, b, c = radii
  r = (a * b * c) ** (1. / 3.)
  D = np.array([[r/a, 0., 0.], [0., r/b, 0.], [0., 0., r/c]])
  transformation = evecs.dot(D).dot(evecs.T)

  self.MagBias = centre
  self.Magtransform = transformation

  self.setSRD(currentSRD)

def __ellipsoid_fit(self, X):
  x = X[:, 0]
  y = X[:, 1]
  z = X[:, 2]
  D = np.array([x * x + y * y - 2 * z * z,
        x * x + z * z - 2 * y * y,
        2 * x * y,
        2 * x * z,
        2 * y * z,
        2 * x,
        2 * y,
        2 * z,
        1 - 0 * x])
  d2 = np.array(x * x + y * y + z * z).T # rhs for LLSQ
  u = np.linalg.solve(D.dot(D.T), D.dot(d2))
  a = np.array([u[0] + 1 * u[1] - 1])
  b = np.array([u[0] - 2 * u[1] - 1])
  c = np.array([u[1] - 2 * u[0] - 1])
  v = np.concatenate([a, b, c, u[2:]], axis=0).flatten()
  A = np.array([[v[0], v[3], v[4], v[6]],
        [v[3], v[1], v[5], v[7]],
        [v[4], v[5], v[2], v[8]],
        [v[6], v[7], v[8], v[9]]])

  center = np.linalg.solve(- A[:3, :3], v[6:9])

  translation_matrix = np.eye(4)
  translation_matrix[3, :3] = center.T

  R = translation_matrix.dot(A).dot(translation_matrix.T)

  evals, evecs = np.linalg.eig(R[:3, :3] / -R[3, 3])
  evecs = evecs.T

  radii = np.sqrt(1. / np.abs(evals))
  radii *= np.sign(evals)

  return center, evecs, radii, v

'''
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()
print ("Acceleration calib start")

imu.caliberateAccelerometer()
print ("Acceleration calib successful")
#imu.caliberateMag()

print("1234")
imu.caliberateMagPrecise()

print ("Mag calib successful")

accelscale = imu.Accels
accelBias = imu.AccelBias
gyroBias = imu.GyroBias
mags = imu.Mags 
magBias = imu.MagBias



print ("Mag caliberation Finished")
print (imu.MagBias)
print (imu.Magtransform)
print (imu.Mags)

imu.saveCalibDataToFile("/home/simurgh/Codes/calib.json")
print ("calib data saved")



imu.loadCalibDataFromFile("/home/simurgh/Codes/calib.json")
if np.array_equal(accelscale, imu.Accels) & np.array_equal(accelBias, imu.AccelBias) & \
	np.array_equal(mags, imu.Mags) & np.array_equal(magBias, imu.MagBias) & \
	np.array_equal(gyroBias, imu.GyroBias):
	print ("calib loaded properly")

