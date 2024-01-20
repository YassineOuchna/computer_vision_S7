import os

os.system(
    "opencv_annotation.exe -a=annotations_gray.txt -i=imgs/positive_imgs_gray opencv/build/x64/vc15/bin"
)
