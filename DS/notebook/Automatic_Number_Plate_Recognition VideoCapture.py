import cv2
import matplotlib.pyplot as plt
import numpy as np
import imutils
import easyocr

def process_frame(img):
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
        return img, None
    
    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)
    
    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    
    cropped_image = gray[x1:x2+3, y1:y2+3]
    
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    
    if len(result) > 0:
        text = result[0][1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.putText(img, text, org=(approx[0][0][0], approx[1][0][1] + 60), 
                          fontFace=font, fontScale=1, color=(0, 255, 0), thickness=5)
        img = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0, 255, 0), 3)
    
    return img, result

# Запуск відеопотоку з веб-камери
cap = cv2.VideoCapture(0)  # Використання камери (0 - перша підключена камера)
while True:
    ret, frame = cap.read()  # Читання кадру з камери
    if not ret:
        break
    
    processed_frame, result = process_frame(frame)
    
    # Виведення обробленого зображення
    cv2.imshow('Car License Plate Detection', processed_frame)
    
    # Зупинка програми при натисканні 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Відпуск камери і закриття вікон
cap.release()
cv2.destroyAllWindows()