import cv2

first_frame = None

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()

    grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    grayscale_frame = cv2.GaussianBlur(grayscale_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = grayscale_frame
        continue

    delta_frame = cv2.absdiff(first_frame, grayscale_frame)
    threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    cv2.dilate(threshold_frame, None, iterations=2)

    # finds contours
    (cnts, _) = cv2.findContours(threshold_frame.copy(),
                                 cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        
        (a, b, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (a, b), (a+w, b+h), (0, 255, 0), 2)

    cv2.imshow('Grayscale Frame Capture', grayscale_frame)
    cv2.imshow('Delta Frame Capture', delta_frame)
    cv2.imshow('Threshold Frame Capture', threshold_frame)
    cv2.imshow('Color Frame', frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
