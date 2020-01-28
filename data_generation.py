'''This script is for generating data
1. Provide desired path to store images.
2. Press 'c' to capture image and display it.
3. Press any button to continue.
4. Press 'q' to quit.
'''

import cv2
from os import getcwd, path
import arducam_mipicamera as arducam


camera = arducam.mipi_camera()
camera.init_camera()
camera.set_mode(0)
camera.software_auto_white_balance(enable=True)
camera.software_auto_exposure(enable=True)
fmt = camera.get_resolution()


def align_down(size, align):
    return (size & ~((align) - 1))


def align_up(size, align):
    return align_down(size + align - 1, align)


def read_img():
    frame = camera.capture(encoding='i420')
    height = int(align_up(fmt[1], 16))
    width = int(align_up(fmt[0], 32))
    image = frame.as_array.reshape(int(height * 1.5), width)
    return cv2.flip(cv2.cvtColor(image, cv2.COLOR_YUV2BGR_I420), -1)


path = path.join(getcwd(), "aruco_data")
count = 0
while True:
    name = path + str(count) + ".jpg"
    ret, img = read_img()

    if input("") != "q":
        cv2.imwrite(name, img)
        print("Wrote", name)
        count += 1
    else:
        camera.close_camera()
        break
