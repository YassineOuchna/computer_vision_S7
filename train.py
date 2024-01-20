import os

# Get parameters
w, h = 24, 24
numPos = len(os.listdir("imgs/positive_imgs")) - 5
numNeg = len(os.listdir("imgs/negative_imgs_gray"))
numStages = 6
path = ".\cascade\cascade7"

# Command opencv_createsamples
createsamples = "opencv_createsamples "
createsamples += "-bg bg.txt "
createsamples += "-info annotations.txt "
createsamples += "-num " + str(numPos) + " "
createsamples += "-w " + str(w) + " "
createsamples += "-h " + str(h) + " "
createsamples += "-vec positives.vec"
os.system(createsamples)  # Run command

# Command opencv_traincascadecascade
traincascade = "opencv_traincascade "
traincascade += f"-data {path} "
traincascade += "-vec positives.vec "
traincascade += "-bg bg.txt "
traincascade += "-numPos " + str(numPos) + " "
traincascade += "-numNeg " + str(numNeg) + " "
traincascade += "-numStages " + str(numStages) + " "
traincascade += "-w " + str(w) + " "
traincascade += "-h " + str(h) + " "
traincascade += "-precalcValBufSize 4048 "
traincascade += "-precalcIdxBufSize 4048 "
traincascade += "-maxFalseAlarmRate 0.05 "
os.system(traincascade)  # Run command
