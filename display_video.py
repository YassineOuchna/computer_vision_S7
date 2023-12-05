import argparse
import imutils
import time
import io
import cv2
import json
import random
import zenoh
import binascii
import numpy as np
import json
import capture_video
parser = argparse.ArgumentParser(
    prog='detect_faces',
    description='zenoh face recognition example display')
parser.add_argument('-m', '--mode', type=str, choices=['peer', 'client'],
                    help='The zenoh session mode.')
parser.add_argument('-e', '--connect', type=str, metavar='ENDPOINT', action='append',
                    help='zenoh endpoints to connect to.')
parser.add_argument('-l', '--listen', type=str, metavar='ENDPOINT', action='append',
                    help='zenoh endpoints to listen on.')
parser.add_argument('-i', '--id', type=int, default=random.randint(1, 999),
                    help='The Camera ID.')
parser.add_argument('-w', '--width', type=int, default=200,
                    help='width of the published faces')
parser.add_argument('-q', '--quality', type=int, default=95,
                    help='quality of the published faces (0 - 100)')
parser.add_argument('-a', '--cascade', type=str,
                    default='haarcascade_frontalface_default.xml',
                    help='path to the face cascade file')
parser.add_argument('-d', '--delay', type=float, default=0.05,
                    help='delay between each frame in seconds')
parser.add_argument('-p', '--prefix', type=str, default='demo/facerecog',
                    help='resources prefix')
parser.add_argument('-c', '--config', type=str, metavar='FILE',
                    help='A zenoh configuration file.')

args = parser.parse_args()
conf = zenoh.config_from_file(
    args.config) if args.config is not None else zenoh.Config()
if args.mode is not None:
    conf.insert_json5(zenoh.config.MODE_KEY, json.dumps(args.mode))
if args.connect is not None:
    conf.insert_json5(zenoh.config.CONNECT_KEY, json.dumps(args.connect))
if args.listen is not None:
    conf.insert_json5(zenoh.config.LISTEN_KEY, json.dumps(args.listen))

jpeg_opts = [int(cv2.IMWRITE_JPEG_QUALITY), args.quality]
cams = {}


def frames_listener(sample):
    # print('[DEBUG] Received frame: {}'.format(sample.key_expr))
    chunks = str(sample.key_expr).split('/')
    cam = chunks[-1]

    cams[cam] = bytes(sample.payload)


print('[INFO] Open zenoh session...')

zenoh.init_logger()
z = zenoh.open(conf)

detector = cv2.CascadeClassifier(args.cascade)

sub = z.declare_subscriber(args.prefix + '/cams/*', frames_listener)


def get_info():
    for cam in list(cams):
        npImage = np.frombuffer(cams[cam], dtype=np.uint8)
        img = cv2.imdecode(npImage, 1)
        w = img.shape[1]
        # OBJECT DETECTION
        info_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        L_limit = np.array([50, 50, 50])  # setting the lower limit
        U_limit = np.array([100, 255, 255])  # setting the upper limit
        mask = cv2.inRange(info_hsv, L_limit, U_limit)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            # Get the largest contour (assuming it's the target)
            largest_contour = max(contours, key=cv2.contourArea)
            # Get the moments to calculate the center of the contour
            moments = cv2.moments(largest_contour)

            if moments["m00"] != 0:
                # Calculate centroid x, y coordinates of the contour
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])

                # Draw a circle at the center
                cv2.circle(img, (cx, cy), 2, (255, 0, 0), -1)
                cv2.putText(img, f"Center: ({cx}, {cy})", (cx - 50, cy - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.imshow('Detected Center', img)
                return True, cx-w/2
            else:
                cv2.imshow('Detected Center', img)
                return False, 0
        else:
            cv2.imshow('Detected Center', img)
            return False, 0

    time.sleep(args.delay)


if __name__ == "__main__":
    while True:
        print(get_info())
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            z.close()
            cv2.destroyAllWindows()
            break
