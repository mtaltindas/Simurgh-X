
import cv2
import numpy as np
import time

from .location_estimater import simurgh_estimate


trajectory_len = 100
lk_params = dict(winSize  = (15, 15),
                maxLevel = 2,
                criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))



def simurgh_flow(prev_gray,frame_gray,trajectories,img,startTime):
    estimatedLocation=np.array((-1,-1),dtype=np.float32)
    img0, img1 = prev_gray, frame_gray
    p0 = np.float32([trajectory[-1] for trajectory in trajectories]).reshape(-1, 1, 2)
    p1, _st, _err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
    p0r, _st, _err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
    d = abs(p0-p0r).reshape(-1, 2).max(-1)
    good = d < 1

    new_trajectories = []

    # Get all the trajectories
    #x,y yi trajectory e al -> artanı sil ->  traj0 ı new_traj sonuna ekle-> x,y yi ekrana daire olarak ekle
    #burda x,y son konum oluyo
    for trajectory, (x, y), good_flag in zip(trajectories, p1.reshape(-1, 2), good):
        if not good_flag:
            continue
        trajectory.append((x, y))
        if len(trajectory) > trajectory_len:# 100 den fazla sınır alırsa en başı siliyor
            ##
            ##      Burada bütün trajectoryleri sıfırlayıp konum hesaplaması yapılacak.
            ##
            end=time.time()
            delTime=end-startTime
            print(delTime)
            estimatedLocation=simurgh_estimate(startPixel=trajectory[0],
                                                endPixel=trajectory[trajectory_len],
                                                delTime=delTime)
            del trajectory
            print("RESET")
            timeFlag=True
            break 
        new_trajectories.append(trajectory)
        # Newest detected point
        cv2.circle(img, (int(x), int(y)), 2, (0, 0, 255), -1)
    return new_trajectories,estimatedLocation