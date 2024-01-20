import cv2


def convert_to_grayscale(input_path, output_path):
    # Read the input color image
    color_image = cv2.imread(input_path)

    # Convert the color image to grayscale
    grayscale_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image
    cv2.imwrite(output_path, grayscale_image)

    print(f"Grayscale image saved at: {output_path}")


# Specify the paths for the input and output images
for i in range(1, 115):
    input_image_path = "./imgs/negative_imgs/" + str(i) + ".jpg"
    output_image_path = "./imgs/negative_imgs_gray/" + str(i) + ".jpg"
    convert_to_grayscale(input_image_path, output_image_path)

"""for i in range(32):
    input_image_path = "./imgs/positive_imgs/new_im" + str(i) + ".png"
    output_image_path = "./imgs/positive_imgs_gray/new_im" + str(i) + ".jpg"
    convert_to_grayscale(input_image_path, output_image_path)"""
