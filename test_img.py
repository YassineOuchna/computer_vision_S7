import cv2
import os

watch_cascade = cv2.CascadeClassifier("cascade/cascade5/cascade.xml")

list_img = os.listdir("imgs/positive_imgs")

for img_name in list_img:
    img = cv2.imread("imgs/positive_imgs/" + img_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    watches = watch_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
    # print(watches)

    for x, y, w, h in watches:
        cv2.rectangle(
            img, (x - 4, y + h), (x + w + 5, y + h + 16), (255, 0, 0), cv2.FILLED
        )
        cv2.putText(
            img,
            "Turtlebot3",
            (x - 4, y + h + 13),
            cv2.FONT_ITALIC,
            0.42,
            (255, 255, 255),
            1,
        )
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("img", img)
    # cv2.imwrite(img_name+'.png',img)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
