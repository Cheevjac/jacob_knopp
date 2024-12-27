import subprocess
import cv2

class Device:

    def connect_device(self):
        """Ensure ADB is running and connect to the device."""
        try:
            # Start the ADB server
            subprocess.run(['adb', 'start-server'], check=True)
            # List connected devices
            devices = subprocess.check_output(['adb', 'devices']).decode()
            print(devices)
            if "device" not in devices:
                raise Exception("No connected devices found.")
            print("Device connected successfully!")
        except Exception as e:
            print(f"Error connecting to device: {e}")
            exit()

    def capture_screenshot(self):
        """Capture a screenshot from the device using ADB."""
        try:
            # Capture and pull screenshot to the local machine
            subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=open('screenshot.png', 'wb'))
            return cv2.imread('screenshot.png')
        except Exception as e:
            print(f"Error capturing screenshot: {e}")
            return None