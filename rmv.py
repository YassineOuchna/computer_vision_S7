import os

for i in range(1, 79):
    os.remove("imgs/positive_imgs/" + str(i) + "adjusted.jpg")
    os.remove("imgs/positive_imgs/" + str(i) + "flipped.jpg")
    os.remove("imgs/positive_imgs/" + str(i) + "rotated.jpg")
    os.remove("imgs/positive_imgs/" + str(i) + "scaled.jpg")
