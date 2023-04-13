import sys
import cv2
import numpy as np
import potrace
import svgwrite
import argparse


def png_to_svg(input_file, output_file, output_size=None):
    # Read the input image
    img = cv2.imread(input_file)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if output_size:
        new_width, new_height = output_size, output_size
    else:
        # Keep the original size
        new_width, new_height = gray.shape[::-1]

    # Scale the image to fit within the specified dimensions while maintaining aspect ratio
    height, width = gray.shape
    if width > height:
        new_height = int(height * (new_width / width))
    else:
        new_width = int(width * (new_height / height))

    gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Threshold the image
    _, bitmap = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    # Convert the bitmap to a potrace bitmap
    potrace_bitmap = potrace.Bitmap(bitmap)

    # Create a potrace path from the bitmap
    path = potrace_bitmap.trace()

    # Create an SVG canvas
    dwg = svgwrite.Drawing(output_file, size=(f'{output_size}px', f'{output_size}px'), profile='tiny')

    # Loop through paths
    for curve in path:
        # Create a path element
        path_element = dwg.path(d="", fill="black")

        # Add the starting point (moveto)
        start_x, start_y = curve.start_point.x, curve.start_point.y
        path_element.push(f"M {start_x} {start_y}")

        # Add the curve segments
        for segment in curve.segments:
            end_x, end_y = segment.end_point.x, segment.end_point.y
            c1_x, c1_y = segment.end_point.x, segment.end_point.y
            path_element.push(f"C {c1_x} {c1_y} {end_x} {end_y}")

        # Close the path (lineto)
        path_element.push("Z")

    # Add the path element to the SVG
        dwg.add(path_element)
# Save the SVG file
    dwg.save()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a PNG image to an SVG icon')
    parser.add_argument('input_png', help='Input PNG file path')
    parser.add_argument('output_svg', help='Output SVG file path')
    parser.add_argument('--size', type=int, help='Output icon size (width and height)')

    args = parser.parse_args()

    output_size = args.size if args.size else None
    png_to_svg(args.input_png, args.output_svg, output_size)
