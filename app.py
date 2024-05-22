import numpy as np
import torch
from tqdm import tqdm

from sixdrepnet import SixDRepNet, utils
import cv2

if __name__ == '__main__':

    device = 0 if torch.cuda.is_available() else -1
    model = SixDRepNet(device)

    cap_input_test_video = cv2.VideoCapture('test_video.mp4')

    fourcc = cv2.VideoWriter.fourcc(*'mp4v')
    fps = cap_input_test_video.get(cv2.CAP_PROP_FPS)
    video_width = int(cap_input_test_video.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap_input_test_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(cap_input_test_video.get(cv2.CAP_PROP_FRAME_COUNT))

    writer = cv2.VideoWriter('output.mp4', fourcc, fps, (video_width, video_height))
    pbar = tqdm(total=length)
    pbar.set_description("Video processing")
    for i in range(length):
        ret, frame = cap_input_test_video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            pitch, yaw, roll = model.predict(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            x_min = int(.15 * video_width)
            x_max = int(.2 * video_width)
            y_min = int(.2 * video_height)
            y_max = int(.25 * video_height)
            bbox_width = int(.01 * video_width * .01 * video_height)
            model.draw_axis(frame, yaw, pitch, roll)
            utils.plot_pose_cube(frame, yaw, pitch, roll, x_min + int(.5 * (
                    x_max - x_min)), y_min + int(.5 * (y_max - y_min)), size=bbox_width)

            writer.write(frame)
            pbar.update(1)
        else:
            cap_input_test_video.release()
            writer.release()
            pbar.update(length - i)
            pbar.close()
            break

    pbar = tqdm(total=length)
    pbar.set_description("Check frames")
    cap_output = cv2.VideoCapture('output.mp4')
    cap_ground_truth_video = cv2.VideoCapture('gt_video.mp4')
    psnr_list = []
    for i in range(length):
        ret, frame = cap_output.read()
        _, gt_frame = cap_ground_truth_video.read()
        if ret:
            mean_psnr = np.mean((gt_frame - frame) ** 2)
            psnr = 10 * np.log10(255 * 255 / mean_psnr) if mean_psnr != 0 else 100
            psnr_list.append(psnr)
            pbar.update(1)
        else:
            cap_output.release()
            cap_ground_truth_video.release()
            pbar.update(length - i)
            pbar.close()
            break

    result_psnr_mean = np.mean(psnr_list)
    print(f"\nMean PSNR: {result_psnr_mean}")
    print(f"Min PSNR: {min(psnr_list)}")
    if result_psnr_mean > 40:
        print(f"The application worked correctly")
    else:
        print("The application did not work correctly")
