# -*- coding: UTF-8 -*-
import cv2 as cv
import argparse
import numpy as np
import time
from utils import choose_run_mode, load_pretrain_model, set_video_writer
from Pose.pose_visualizer import TfPoseVisualizer
from Action.recognizer import load_action_premodel, framewise_recognize

parser = argparse.ArgumentParser(description='Action Recognition by OpenPose')
parser.add_argument('--video', help='Path to video file.')
# args = parser.parse_args()
vis = ['111_tf_out.mp4']

args = parser.parse_args(['--video', vis])
# 관련 모델 가져 오기
estimator = load_pretrain_model('VGG_origin')
action_classifier = load_action_premodel('Action/a-free.h5')

# 매개 변수 초기화
realtime_fps = '0.0000'
start_time = time.time()
fps_interval = 1
fps_count = 0
run_timer = 0
frame_count = 0

#비디오 파일 읽기 및 쓰기 (웹캠 입력에 대해서만 테스트 됨)
cap = choose_run_mode(args)
video_writer = set_video_writer(cap, write_fps=int(7.0))


# #훈련 과정을위한 관절 데이터를 저장하는 txt 파일(for training)
filename = 'output.txt'
f = open(filename, 'a+')

while cv.waitKey(1) < 0:
    has_frame, show = cap.read()
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
        # 실시간 FPS 값 표시
        if (time.time() - start_time) > fps_interval:
            # 인터벌 프로세스의 프레임 수를 계산합니다. 인터벌이 1 초이면 FPS입니다.
            realtime_fps = fps_count / (time.time() - start_time)
            fps_count = 0  # 프레임 수 지우기
            start_time = time.time()
        fps_label = 'FPS:{0:.2f}'.format(realtime_fps)
        cv.putText(show, fps_label, (width-160, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # 감지 된 사람 수 표시
        num_label = "Human: {0}".format(len(humans))
        cv.putText(show, num_label, (5, height-45), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # 현재 실행 시간과 총 프레임 수를 표시합니다.
        if frame_count == 1:
            run_timer = time.time()
        run_time = time.time() - run_timer
        time_frame_label = '[Time:{0:.2f} | Frame:{1}]'.format(run_time, frame_count)
        cv.putText(show, time_frame_label, (5, height-15), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv.imshow('Action Recognition based on OpenPose', show)
        video_writer.write(show)

        # 훈련 과정을위한 데이터 수집(for training)
        joints_norm_per_frame = np.array(pose[-1]).astype(np.str)
        f.write(' '.join(joints_norm_per_frame))
        f.write('\n')

video_writer.release()
cap.release()
f.close()



