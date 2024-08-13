import cv2
import pytesseract

# Specify the paths for the input and output images
image_path = r'Data/8.png'
output_path = r'Data/7.jpg'

# Read the image in grayscale mode
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Check if the image was successfully loaded
if img is None:
    print(f"Error: Image not found at {image_path}")
else:
    # Apply binary thresholding to the image
    threshold_value = 150
    max_value = 255
    _, binary_image = cv2.threshold(img, threshold_value, max_value, cv2.THRESH_BINARY_INV)

    # Save the processed binary image to the specified output path
    cv2.imwrite(output_path, binary_image)
    print(f"Processed image saved at {output_path}")

    # Use PyTesseract to extract text from the binary image
    extracted_text = pytesseract.image_to_string(binary_image)

    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)