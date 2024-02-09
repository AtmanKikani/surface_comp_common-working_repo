#!/usr/bin/python3


import rospy
from sensor_msgs.msg import Image
import cv2 as cv
import os
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

  
CHESS_BOARD_DIM = (7, 7)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001) 
bridge = CvBridge()
n = 0  # image_counter

# checking if  images dir is exist not, if not then create images directory
image_dir_path = "images_down"

CHECK_DIR = os.path.isdir(image_dir_path)
# if directory does not exist create
if not CHECK_DIR:
    os.makedirs(image_dir_path)
    print(f'"{image_dir_path}" Directory is created')
else:
    print(f'"{image_dir_path}" Directory already Exists.')

def detect_checker_board(image, grayImage, criteria, boardDimension):
    ret, corners = cv.findChessboardCorners(grayImage, boardDimension) #"corners" is a 2D array containing the initial estimates of corner locations 
    if ret == True:
        corners1 = cv.cornerSubPix(grayImage, corners, (3, 3), (-1, -1), criteria)
        image = cv.drawChessboardCorners(image, boardDimension, corners1, ret)

    return image, ret


def image_callback(msg):
    global n
    try:
        # Convert ROS CompressedImage message to OpenCV image
        frame = bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="bgr8")
        copyFrame = frame.copy()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        image, board_detected = detect_checker_board(frame, gray, criteria, CHESS_BOARD_DIM)
        # print(ret)
        cv.putText(
            frame,
            f"saved_img : {n}",
            (30, 40),
            cv.FONT_HERSHEY_PLAIN,
            1.4,
            (0, 255, 0),
            2,
            cv.LINE_AA,
        )

        cv.imshow("frame", frame)
        # cv.imshow("copyFrame", copyFrame)

        key = cv.waitKey(1)
        if key == ord("s") and board_detected == True:
            # storing the checker board image
            n += 1  # incrementing the image counter
            cv.imwrite(f"{image_dir_path}/image{n}.png", copyFrame)
            print(f"saved image number {n}")
    except Exception as e:
        print(e)




print("Total saved Images:", n)

def main():
     
    rospy.init_node('bottom_cam_getimgs', anonymous=True)
    rospy.Subscriber("video_stream2", CompressedImage, image_callback)
    rospy.spin()

if __name__ == '__main__':
    main()





