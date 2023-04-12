import sys
import cv2
import numpy as np
import svgwrite

def png_to_svg(input_file, output_file):
    # Read the input image
    img = cv2.imread(input_file)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Scale the image to fit within 24x24 pixels while maintaining aspect ratio
    height, width = gray.shape
    new_width, new_height = 24, 24
    if width > height:
        new_height = int(height * (24 / width))
    else:
        new_width = int(width * (24 / height))

    gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Create a 24x24 white canvas and place the scaled image at the center
    gray_padded = np.full((24, 24), 255, dtype=np.uint8)
    y_offset = (24 - new_height) // 2
    x_offset = (24 - new_width) // 2
    gray_padded[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = gray

    # Apply edge detection using the Canny algorithm
    edges = cv2.Canny(gray_padded, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create an SVG canvas
    dwg = svgwrite.Drawing(output_file, size=('24px', '24px'), profile='tiny')

    # Loop through contours
    for cnt in contours:
        # Simplify the contour
        epsilon = 0.001 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # Convert the contour points to SVG path
        path_data = 'M' + ' L'.join(f'{point[0][0]},{point[0][1]}' for point in approx)
        path_data += ' Z'

        # Add the path to the SVG
        dwg.add(dwg.path(d=path_data, fill='black'))

    # Save the SVG file
    dwg.save()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python png_to_svg.py <input_png> <output_svg>')
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    png_to_svg(input_file, output_file)
