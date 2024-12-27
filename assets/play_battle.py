import os
import cv2
import numpy as np
import pyautogui
from PIL import Image
import random

def find_template_in_image(image, template_path, threshold=0.8):
    """
    Find a template in a screenshot image using OpenCV template matching in grayscale.

    Parameters:
        image (ndarray): The screenshot image for detection.
        template_path (str): The file path to the template image being matched.
        threshold (float): A matching threshold between 0.0 and 1.0.

    Returns:
        tuple: Coordinates (x, y) of the top-left corner of the detected template.
        None: If no match is found above the threshold.
    """
    if len(image.shape) == 3:  # Color image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise FileNotFoundError(f"Template image at {template_path} could not be loaded.")
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= threshold:
        return max_loc  # Coordinates of the top-left corner of the detected template

    # Return None if no match is found
    return None


def tap_on_device(x, y, template):
    """
    Send a tap command to the device using ADB, tapping at a random point
    within the dimensions of the detected template.
    
    Parameters:
        x (int): Top-left x-coordinate of the detected template.
        y (int): Top-left y-coordinate of the detected template.
        template (ndarray): The template image used for detection (to get dimensions).
    """
    try:
        # Get the width and height of the template image
        height, width, _ = template.shape

        # Generate random coordinates within the image
        random_x = x + random.randint(0, width - 1)
        random_y = y + random.randint(0, height - 1)

        # Send the tap command
        subprocess.run(['adb', 'shell', f'input tap {random_x} {random_y}'], check=True)
        print(f"Tapped randomly at ({random_x}, {random_y}) inside the image bounds.")
    except Exception as e:
        print(f"Error tapping on device: {e}")


def main_loop():
    """Main loop for automating actions."""
    # Path to the template image to match
    template_path = 'button.png'

    while True:
        # Capture screenshot
        screenshot = capture_screenshot()
        if screenshot is None:
            break

        # Find the template in the screenshot
        location = find_template_in_image(screenshot, template_path)
        if location:
            x, y = location
            print(f"Found target at ({x}, {y})")
            tap_on_device(x, y)
        else:
            print("Target not found. Retrying...")

        # Wait before the next iteration
        pyautogui.sleep(2)

if __name__ == '__main__':
    connect_device()
    print("Starting main loop...")
    main_loop()
