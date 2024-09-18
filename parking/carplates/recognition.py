import easyocr
import imutils
import numpy as np
import cv2


def recognition(img_path):
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError(f"Image at {img_path} could not be loaded.")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 11, 11, 17)
    edged = cv2.Canny(bfilter, 30, 200)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    if location is None:
        raise ValueError("Could not find a contour with 4 points.")

    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2 + 1, y1:y2 + 1]
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)[0][1]
    result = str(result)
    result = result.replace(" ", '')

    return result
