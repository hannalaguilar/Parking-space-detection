import cv2
import pickle

from parking import ROOT_DIR

# Initialize
img_path = ROOT_DIR / 'data/parking_car.png'
width = 107
height = 48

# Don't allow duplicate positions if we've run the code before
try:
    with open(ROOT_DIR / 'data/car_positions', 'rb') as f:
        position_list = pickle.load(f)
except:
    position_list = []


def mouse_click(events: int,
                x: int,
                y: int,
                flags, params):
    # We need to set flags and params to setMouseCallback works!
    # Draw rectangle
    if events == cv2.EVENT_LBUTTONDOWN:
        position_list.append((x, y))
    # Delete wrong rectangle
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, position in enumerate(position_list):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                position_list.pop(i)

    with open(ROOT_DIR / 'data/car_positions', 'wb') as f:
        pickle.dump(position_list, f)


while True:
    img = cv2.imread(str(img_path))  # BGR
    for pos in position_list:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height),
                      (255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouse_click)
    cv2.waitKey(1)
