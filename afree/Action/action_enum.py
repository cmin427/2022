from enum import Enum


class Actions(Enum):
    """
    Actions enum
    """
    # framewise_recognition.h5
    # squat = 0
    # stand = 1
    # walk = 2
    # wave = 3

    # framewise_recognition_under_scene.h5
    # stand = 0
    # walk = 1
    # operate = 2
    # fall_down = 3
    # run = 4

    #CLASS 6개
    stand = 0 # 0 : 그 외
    m_kick = 1 # 1 : 몸통 공격(발차기)
    h_kick = 2 # 2 : 머리 공격(발차기)
    # -----추후 데이터 추가----------
    # m_punch = 3 # 3 : 몸통 공격(주먹)
    # h_paul = 4 # 4 : (반칙)머리 공격(주먹)
    # l_paul = 5 # 5 : (반칙)다리 공격(로우킥)