import sys
import traceback

import torch
from sixdrepnet import SixDRepNet
import cv2


def smoke_test():
    device = 0 if torch.cuda.is_available() else -1
    model = SixDRepNet(device)
    img = cv2.imread('test_image.jpg')
    pitch, yaw, roll = model.predict(img)


if __name__ == '__main__':
    try:
        smoke_test()
        print("Smoke test passed")
    except Exception as e:
        print("Smoke test failed with traceback: ")
        traceback.print_exc()
        sys.exit(1)
