import cv2
import numpy as np

feature_params = dict(maxCorners = 20,
                    qualityLevel = 0.3,
                    minDistance = 10,
                    blockSize = 7 )

   
def simurgh_feature(frame_gray,trajectories): 
        mask = np.zeros_like(frame_gray)
        mask[:] = 255

        # Lastest point in latest trajectory
        for x, y in [np.int32(trajectory[-1]) for trajectory in trajectories]:
            cv2.circle(mask, (x, y), 10,(0,0,0) , -1)

        # Detect the good features to track
        p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
        
        if p is not None:
            # If good features can be tracked - add that to the trajectories
            for x, y in np.float32(p).reshape(-1, 2):
                #print(x,y)
                trajectories.append([(x, y)])
        return (mask,trajectories)
