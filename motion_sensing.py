import cv2

cap = cv2.VideoCapture(0)

def motion(frame1, frame2):
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        if cv2.contourArea(contour) < 5000:
            continue
        else:
            cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 250, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement detected'), (10, 20), cv2.FONT_HERSHEY_COMPLEX,
                        1, (0, 255, 200), 3)
            return frame1
    frame1 = frame2
    ret, frame2 = cap.read()
    return frame2



while True:
    ret, first_frame = cap.read()
    ret, second_frame = cap.read()
    motion(first_frame, second_frame)
    cv2.imshow("Motion_frame", first_frame)

    if cv2.waitKey(30) & 0xff == ord('q'):
        break
cv2.destroyAllWindows