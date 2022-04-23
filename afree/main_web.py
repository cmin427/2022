# -*- coding: UTF-8 -*-
import cv2 as cv
import argparse
import numpy as np
import time
from utils import choose_run_mode, load_pretrain_model, set_video_writer
from Pose.pose_visualizer import TfPoseVisualizer
from Action.recognizer import load_action_premodel, framewise_recognize

def afree(vis):
    parser = argparse.ArgumentParser(description='Action Recognition by OpenPose')
    parser.add_argument('--video', help='Path to video file.')
    # vis = 'kick.mp4'
    # for vi in vis:
    v=cv.VideoCapture(vis)
    v.set(cv.CAP_PROP_POS_AVI_RATIO,1)
    max_frame = v.get(cv.CAP_PROP_POS_FRAMES)
    args = parser.parse_args(['--video', vis])
    # print(max_frame)
    # print(args)
    # Import related models
    estimator = load_pretrain_model('VGG_origin')
    action_classifier = load_action_premodel('Action/a-free-1.h5')

    # Parameter initialization
    realtime_fps = '0.0000'
    start_time = time.time()
    fps_interval = 1
    fps_count = 0
    run_timer = 0
    frame_count = 0


    # Read and write video files (only tested for webcam input)
    cap = choose_run_mode(args)
    video_writer = set_video_writer(cap, write_fps=int(7.0))
    # print(str(args.video[:-4]))

    # 훈련 용 관절 데이터를 저장하는 txt 파일 (훈련 용)
    # f = open(str(args.video[:-4])+'.txt', 'a+')

    while cv.waitKey(1) < 0:
        has_frame, show = cap.read()
        cv.startWindowThread()
        if has_frame:
            fps_count += 1
            frame_count += 1

            # pose estimation
            humans = estimator.inference(show)
            # get pose info
            pose = TfPoseVisualizer.draw_pose_rgb(show, humans)  # return frame, joints, bboxes, xcenter
            # recognize the action framewise
            show = framewise_recognize(pose, action_classifier)

            height, width = show.shape[:2]
            # Display real-time FPS value
            if (time.time() - start_time) > fps_interval:
                # 인터벌 프로세스의 프레임 수를 계산합니다. 인터벌이 1 초이면 FPS입니다.
                realtime_fps = fps_count / (time.time() - start_time)
                fps_count = 0  # Clear the number of frames
                start_time = time.time()
            fps_label = 'FPS:{0:.2f}'.format(realtime_fps)
            cv.putText(show, fps_label, (width-160, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Show the number of people detected
            num_label = "Human: {0}".format(len(humans))
            cv.putText(show, num_label, (5, height-45), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Display the current running time and total number of frames
            if frame_count == 1:
                run_timer = time.time()
            run_time = time.time() - run_timer
            time_frame_label = '[Time:{0:.2f} | Frame:{1}]'.format(run_time, frame_count)
            cv.putText(show, time_frame_label, (5, height-15), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            cv.imshow('Action Recognition based on OpenPose', show)
            video_writer.write(show)
            # # Collect data for training (for training)
            # joints_norm_per_frame = np.array(pose[-1]).astype(np.str)
            # f.write(' '.join(joints_norm_per_frame))
            # f.write('\n')
            if frame_count > (max_frame-1):
                break
    video_writer.release()
    cap.release()
    cv.destroyAllWindows()
    # f.close()
