import numpy as np
import cv2
lk_params = dict(winSize  = (15, 15),
                maxLevel = 2,
                criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
trajectory_len = 50

def simurgh_pixel_change(trajectories):
    i=0
    startingPointsY=np.array([],dtype=np.int32)
    endingPointsY=np.array([],dtype=np.int32)
    delPointsY=np.array([],dtype=np.int32)
    for simurghTraj in trajectories:
        if len(simurghTraj)>50:
            i+=1
            startingPointsY=np.append(startingPointsY,int(simurghTraj[0][1]))
            #startingPoints.append(simurghTraj[0])
            endingPointsY=np.append(endingPointsY,int(simurghTraj[len(simurghTraj)-1][1]))
            #endingPoints.append(simurghTraj[len(trajectory)-2])
            #print(startingPointsY,"&&&&&",endingPointsY)
    
    while i>0:
        delPixel=endingPointsY[i-1]-startingPointsY[i-1]
        #print(delPixel)

        
        delPointsY=np.append(delPointsY,delPixel)
        i-=1
    avgDelPixel=np.mean(delPointsY)
    return avgDelPixel
  
    #print(avgDelPixel)  



def simurgh_flow(prev_gray,frame_gray,trajectories,img,j,width,height):
        avgDelPixel=0
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
                avgDelPixel=simurgh_pixel_change(trajectories)
                j+=1
                del trajectory
                print("Reset")
                break
                
            new_trajectories.append(trajectory)
            # Newest detected point
            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
        return new_trajectories,img,avgDelPixel,j