#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 必要なモジュールをインポート
import rospy
import smach
from happymimi_navigation.srv import NaviLocation
from enter_room.srv import EnterRoom
from happymimi_manipulation_msgs.srv import RecognitionToGrasping,StrTrg

# EnterTheRoomクラス
# 部屋に入る動作を制御
class EnterTheRoom(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["enter_finish"])
        self.navi = rospy.ServiceProxy("/navi_location_server", NaviLocation)
        self.enter_srv = rospy.ServiceProxy("enter_room_server", EnterRoom)

    def execute(self, userdata):
        self.enter_srv(0.5, 0.3)  # 距離、スピードを指定
        return 'enter_finish'

# Navigationクラス
# ナビゲーション（位置移動）を制御
class Navigation(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["Navi_fin"])
        self.navi = rospy.ServiceProxy("/navi_location_server", NaviLocation)

    def execute(self):
        self.navi('ロケーション名')
        return 'Navi_fin'

# Manipulationクラス
# 物をつかむ、渡す動作を制御
class Manipulation(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=["mani_fin"])
        self.grasp_cup = rospy.ServiceProxy('/recognition_to_grasping', RecognitionToGrasping)
        self.give = rospy.ServiceProxy('/servo/arm', StrTrg)

    def execute(self):
        self.grasp_cup('cup')  # カップをつかむ
        self.give('give')
        return 'mani_fin'

# メイン関数
def main():
    rospy.init_node('Leblons')

    sm_top = smach.StateMachine(outcomes=['All_fin'])
    with sm_top:
        smach.StateMachine.add('ENTER', EnterTheRoom(), transitions={'enter_finish':'NAVI'})
        smach.StateMachine.add('NAVI', Navigation(), transitions={'Navi_fin':'MANIPULATION'})
        smach.StateMachine.add('MANIPULATION', Manipulation(), transitions={'mani_fin': 'All_fin'})

    outcome = sm_top.execute()

if __name__ == '__main__':
    main()
