
import cv2

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1080,
    capture_height=1920,
    display_width=540,
    display_height=960,
    framerate=30,
    flip_method=1,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


def show_camera():


	video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=1), cv2.CAP_GSTREAMER)
	width=int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
	height=int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
	if video_capture.isOpened():
		try:
			while True:
				ret_val, frame = video_capture.read()
				cv2.imshow("aa", frame)
				keyCode = cv2.waitKey(10) & 0xFF
				if keyCode == 27 or keyCode == ord('q'):
					break
		finally:
			video_capture.release()
			cv2.destroyAllWindows()
	else:
		print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()
