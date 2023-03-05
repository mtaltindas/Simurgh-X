
import cv2

""" 
gstreamer_pipeline returns a GStreamer pipeline for capturing from the CSI camera
Flip the image by setting the flip_method (most common values: 0 and 2)
display_width and display_height determine the size of each camera pane in the window on the screen
Default 1920x1080 displayd in a 1/4 size window
"""

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
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

	window_title = "CSI Camera"
	video_capture = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
	width=int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
	height=int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
	writer=cv2.VideoWriter('ccc.avi',cv2.VideoWriter_fourcc(*'XVID'),20,(960,540))
	if video_capture.isOpened():
		try:
			window_handle = cv2.namedWindow(window_title, cv2.WINDOW_AUTOSIZE)
			while True:
				ret_val, frame = video_capture.read()
				if cv2.getWindowProperty(window_title, cv2.WND_PROP_AUTOSIZE) >= 0:
					cv2.imshow(window_title, frame)
					writer.write(frame)
				else:
					break 
				keyCode = cv2.waitKey(10) & 0xFF
				if keyCode == 27 or keyCode == ord('q'):
					break
		finally:
			video_capture.release()
			writer.release()
			cv2.destroyAllWindows()
	else:
		print("Error: Unable to open camera")


if __name__ == "__main__":
    show_camera()
