import cv2
import pickle
import numpy as np
from parking import ROOT_DIR

# Initialize
video_path = ROOT_DIR / 'data/car_park.mp4'
width = 107
height = 48
area = width * height

with open(ROOT_DIR / 'data/car_positions', 'rb') as f:
    position_list = pickle.load(f)

# Video
cap = cv2.VideoCapture(str(video_path))


def check_parking(processed_img,
                  original_img):
    space_counter = 0

    for (x, y) in position_list:
        img_crop = processed_img[y:y + height, x:x + width]
        # cv2.imshow(str(x + y), img_crop)
        count = cv2.countNonZero(img_crop) * (100 / area)

        if count < 10:
            color = [0, 255, 0]
            thickness = 5
            space_counter += 1
        else:
            color = [0, 0, 255]
            thickness = 2

        # cv2.putText(original_img,
        #             str(round(count, 0)),
        #             (x, y),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             1,
        #             (255, 0, 0),
        #             2)
        cv2.rectangle(original_img,
                      (x, y),
                      (x + width, y + height),
                      color,
                      thickness)

    cv2.putText(original_img,
                f'Free parking: {space_counter}/{len(position_list)}',
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                3)


def processing_img(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255,
                                          cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                          cv2.THRESH_BINARY_INV, 25, 16)
    img_median_blur = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median_blur, kernel, iterations=1)
    return img_dilate


while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    if success:
        processed_img = processing_img(img)
        check_parking(processed_img, img)
        cv2.imshow('Binarized image', processed_img)
        cv2.imshow('Image', img)
        cv2.waitKey(10)
