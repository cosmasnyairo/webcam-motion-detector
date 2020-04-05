import cv2
from datetime import datetime
import pandas

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=['Start', 'END'])

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    status = 0
    check, frame = video.read()

    # convert frame to grayscale
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

    # increase the contour value to allow detection of larger objects
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1

        # draws rectangle over moving object
        (a, b, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (a, b), (a+w, b+h), (0, 255, 0), 2)

    status_list.append(status)

    # no motion(0) to motion(1)
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())

    #  motion(1) to no motion(0)
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow('Grayscale Frame Capture', grayscale_frame)
    cv2.imshow('Delta Frame Capture', delta_frame)
    cv2.imshow('Threshold Frame Capture', threshold_frame)
    cv2.imshow('Color Frame', frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(times.append(datetime.now()))
        break

# add time to dataframe using range of 2
# e.g appends times[0] to start and times[0+1] to end
# uses range of 2 so goes to 0+2
# appends time[2] to start and time[2+1]

for i in range(0, len(times), 2):
    df = df.append({'Start': times[i], 'End': times[i+1]}, ignore_index=True)

print('Generating csv')
df.to_csv('motion_times.csv')

video.release()
cv2.destroyAllWindows()
