import cv2
import numpy as np

imgfolder='positive_imgs'
# Charger une image
for i in range (1,79):
    image_path='./imgs/'+imgfolder+'/'+str(i)+'.jpg'
    image = cv2.imread(image_path)

    # Exemple de rotation
    angle = 45
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, M, (cols, rows))

    # Exemple de miroir horizontal
    flipped_image = cv2.flip(image, 1)

    # Exemple de changement d'échelle
    scaled_image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # Exemple de changement de luminosité et de contraste
    alpha = 1.5  # contraste
    beta = 50  # luminosité
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Affichage des images augmentées
    cv2.imwrite('./imgs/'+imgfolder+'/'+str(i)+'rotated.jpg', rotated_image)
    cv2.imwrite('./imgs/'+imgfolder+'/'+str(i)+'flipped.jpg', flipped_image)
    cv2.imwrite('./imgs/'+imgfolder+'/'+str(i)+'scaled.jpg', scaled_image)
    cv2.imwrite('./imgs/'+imgfolder+'/'+str(i)+'adjusted.jpg', adjusted_image)
