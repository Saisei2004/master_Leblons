#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import math
import sys
import rospy
import rosparam
import roslib
import os
import smach
import smach_ros
#from fmmmod import FeatureFromVoice, FeatureFromRecog,  LocInfo, SaveInfo
#Debug中

from std_msgs.msg import Float64
from happymimi_msgs.srv import SimpleTrg, StrTrg
from happymimi_navigation.srv import NaviLocation, NaviCoord
#音声
file_path = roslib.packages.get_pkg_dir('rcp_opl') + '/src/'
sys.path.insert(0, file_path)
import sp_receptionist as sp
from happymimi_recognition_msgs.srv import RecognitionFind,RecognitionFindRequest,RecognitionLocalize,RecognitionLocalizeRequest,MultipleLocalize
file_path = roslib.packages.get_pkg_dir('happymimi_teleop') + '/src/'
sys.path.insert(0, file_path)
from base_control import BaseControl
import pickle
teleop_path = roslib.packages.get_pkg_dir('recognition_processing')
sys.path.insert(0, os.path.join(teleop_path, 'src/'))
from recognition_tools import RecognitionTools
#V8 no ki ri ka e
#from recognition_tools_v8 import RecognitionToolsV8 

from happymimi_recognition_msgs.srv import Clip, ClipResponse
# speak
tts_srv = rospy.ServiceProxy('/tts', StrTrg)
# wave_play
wave_srv = rospy.ServiceProxy('/waveplay_srv', StrTrg)
from pathlib import Path
pickle_path = "/home/mimi-orin/ws/noetic_ws/src/receptionist/config/guest_feature.pkl"
#rt = RecognitionToolsV8()
rt = RecognitionTools()


with open(pickle_path , "wb") as f:
    feature_dic = {"guest1":{"name":"","drink":"","age":""},
                "guest2":{"name":"","drink":"","age":""}}
    pickle.dump(feature_dic, f)

RANGE = 3

class MoveInitalPosition(smach.State):#ゲストの検出のための位置へ移動
    def __init__(self):
        smach.State.__init__(self,outcomes = ['move_finish'],
                             input_keys = ['g_count_in'],
                             output_keys = ['feature_out']
                             )
        self.gen_coord_srv = rospy.ServiceProxy('/human_coord_generator', SimpleTrg)
        #self.ap_srv = rospy.ServiceProxy('/approach_person_server', StrTrg)
        self.navi_srv = rospy.ServiceProxy('navi_location_server', NaviLocation)
        self.head_pub = rospy.Publisher('/servo/head',Float64, queue_size = 1)
        self.bc = BaseControl()
        self.multiple = rospy.ServiceProxy('/recognition/multiple_localize',MultipleLocalize)

    def execute(self,userdata):
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        # self.navi_srv('start_pos_cml')
        # self.navi_srv('start_1_cml')
        # self.navi_srv('start_2_cml')
        # self.navi_srv('start_3_cml')
        # self.navi_srv('parking_cml')
        # self.navi_srv('parking_side_cml')
        # self.navi_srv('start_1_cml')
        # self.navi_srv('start_2_cml')
        # self.navi_srv('start_3_cml')
        # self.navi_srv('host_rcp')
        # self.navi_srv('chairs_1_rcp')
        # self.navi_srv('chairs_2_rcp')
        # self.navi_srv('chairs_3_rcp')
        #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        
        rospy.loginfo("Executing state:MOVE_INITAL_POSITION")
        rospy.loginfo("始まりました〜")
        guest_num = userdata.g_count_in
        
        if guest_num == 0:
           #dooropen
            tts_srv("start receptionist")
            return 'move_finish'
            #pass
        if guest_num == 1:
            self.navi_srv('start_1_rcp')  
            tts_srv("Moved to entrance.")
            #self.bc.rotateAngle(,0.2)#入り口の方を向く
            rospy.sleep(3.5)
            return 'move_finish'

class DiscoverGuests(smach.State):#ゲストの検出、受付
    def __init__(self):
        smach.State.__init__(self, outcomes = ['discover_finish'],
                             input_keys = ['feature_in'],
                             output_keys = ['feature_out']
                             )
        self.ap_srv = rospy.ServiceProxy('/approach_person_server', StrTrg)
        #self.head_pub = rospy.ServiceProxy('/servo/head',Float64, queue_size = 1)
        self.find_srv = rospy.ServiceProxy('/recognition/find',RecognitionFind)
        self.head_pub = rospy.Publisher('/servo/head', Float64, queue_size = 1)
        self.age_srv = rospy.ServiceProxy('/person_feature/gpt',Clip)
        self.fea_srv = rospy.ServiceProxy('/person_feature/gpt',Clip)
        self.multiple = rospy.ServiceProxy('/recognition/multiple_localize',MultipleLocalize)


    def execute(self,userdata):
        

        rospy.loginfo("Executing state:DISCOVERGUESTS")
        self.head_pub.publish(-15)
        rospy.sleep(1.0)
        g_range = 1.5 # 1.5m 以下に人がいるとき
        self.find_result = False
        #人の検知
        while(1):
            points = self.multiple("person").points
            if points:
                for i in range(len(points)):
                    point_x,point_y = self.guide.Calculate_Angle(points,i)
                    if (point_x < g_range)and(point_y < g_range):
                        self.find_result = True
                        break
                    
                        

            rospy.sleep(1.0)
            rospy.loginfo("人見つけました〜")
            if self.find_result == True:
                print('found a person')
                req  = RecognitionLocalizeRequest()
                req.target_name  = "person"
                #rt = RecognitionTools()
                centroid = rt.localizeObject(request = req).point
                person_height = centroid.z
                self.head_pub.publish(-10)
                rospy.sleep(1.0)
                #self.head_pub.publish(20)
                #rospy.sleep(1.0)
                wave_srv('/receptionist/hello.wav')
                rospy.sleep(0.5)
                get_feature = sp.GetFeature()
                rospy.loginfo("名前聞きます〜")
                name = get_feature.getName()
                rospy.loginfo("飲み物聞きます〜")
                drink = get_feature.getFavoriteDrink()
                rospy.loginfo("特徴見ます〜")
                self.fea_srv = rospy.ServiceProxy('/person_feature/gpt',Clip)

            # ###############################################

            #     age = str(self.fea_srv("age"))
                feature_list = [1,1,1,1]
                
                feature_list = str(self.fea_srv("all"))
            #     self.f_age = str("Age is" + age)

            #     a = str(self.fea_srv("glass"))
            #     self.f_glass = a.replace("result: a photo of ", "")

            #     b = str(self.fea_srv("gender"))
            #     self.f_gender = a.replace("result: a photo of ", "")

            #     self.f_cloth = str(self.fea_srv("cloth"))

            #     self.f_pants = str(self.fea_srv("pants"))

            #     feature_list = [self.f_age, self.f_glass, self.f_gender, self.f_cloth, self.f_pants]
            #   feature_list = [1,1,1,1]
            #     #書き換える
                userdata.feature_out = feature_list

            #     rospy.loginfo("特徴見ますた〜")


            # ################################################

                wave_srv("/receptionist/thank.wav")
                rospy.sleep(0.5)
                break

            elif(self.find_result==False):
                #print("found a person")
                tts_srv("i wait person")
                rospy.sleep(3.0)
                continue

        return 'discover_finish'
        
    def Calculate_Angle(self,points,i):
        print(points,"chair_num:" + str(i))
        point = str(points[i]).split()
        print(points)
        point_x = float(point[1])
        point_y = float(point[3])
        return point_x,point_y

class IntroduceGuests(smach.State):#オーナーのもとへ移動、ゲストの紹介
    def __init__(self):
        smach.State.__init__(self, outcomes = ['introduce_finish'],
                             input_keys = ['g_count_in']
                             )
        self.navi_srv = rospy.ServiceProxy('navi_location_server', NaviLocation)
        self.arm_srv = rospy.ServiceProxy('/servo/arm', StrTrg)
        self.bc = BaseControl()
        self.save_srv = rospy.ServiceProxy('/recognition/save',StrTrg)
        self.multiple = rospy.ServiceProxy('/recognition/multiple_localize',MultipleLocalize)
        self.sentence_list = []
        self.coord_gen_srv = rospy.ServiceProxy('/human_coord_generator',SimpleTrg)
        self.ap_srv = rospy.ServiceProxy('/approach_person_server', StrTrg)

    def execute(self,userdata):
      #１ついてこさせる
      #２後ろむく
      #３移動する
      #４紹介を始めると宣言する
      #５後ろを向く
      #６ゲストの方向を向く
      #７腕を伸ばす
      #８紹介をする
      #9元の向きに戻る
      #１０アームをひっこめる
      #１１End of introduction of guests.という
      #
      #
      
      
        rospy.loginfo("Executing state:INTRODUCE_GUESTS")
      
       #1ついてこさせる
        tts_srv("please follow me.")
        rospy.sleep(1.0)
        guest_num = userdata.g_count_in

        #2後ろむく
        self.bc.rotateAngle(-150,0.3)
        rospy.sleep(1.0)
        g_name = "human_0"
        #result = self.coord_gen_srv().result
        #print("result")
        #print(result)
        
        #self.ap_srv(data = g_name)#ナヴィゲーションで代用
        
        #3移動する
        self.navi_srv("host_rcp")
    
        tts_srv("Approached by owner.")
        # self.bc.rotateAngle(180, 0.2)
        # self.bc.translateDist(1.8, 0.2)
        # self.bc.rotateAngle(-90, 0.2)

        #４紹介を始めると宣言する
        tts_srv("We'll start introducing our guests.")
        introduce = sp.IntroduceOfGuests()
        #self.bc.rotateAngle(150,0.3)
        rospy.sleep(0.5)

        #５後ろを向く
        self.bc.rotateAngle(180,0.3)

        #６ゲストの方向を向く        
        points = self.multiple("person").points
        if points:
            points = str(points[0]).split()
            print(points)
            point_x = float(points[1])
            point_y = float(points[3])
            angle = math.atan2(point_y,point_x) * (180/ math.pi)
            rospy.sleep(1.0)
            self.bc.rotateAngle(int(angle),0.2)
        rospy.sleep(1.0)
        #７腕を伸ばす
        self.arm_srv('point')
        rospy.sleep(5.0)

        #８紹介をする
        introduce.main(guest_num)

        #9元の向きに戻る
        ### 4/10記入
        if points:
            self.bc.rotateAngle(int(angle * -1),0.2)
        self.bc.rotateAngle(180,0.3)
        rospy.sleep(1.0)

        #１０アームをひっこめる
        self.arm_srv('carry')

        #１１End of introduction of guests.という
        tts_srv("End of introduction of guests.")
        
        rospy.sleep(5.0)
        return 'introduce_finish'

    def Calculate_Angle(self,points,i):
        print(points,"chair_num:" + str(i))
        point = str(points[i]).split()
        print(points)
        point_x = float(point[1])
        point_y = float(point[3])
        return point_x,point_y

class GuideGuests(smach.State):#ゲストのガイド
    def __init__(self):
        smach.State.__init__(self, outcomes = ['guide_finish','all_finish'],
                             input_keys = ['g_count_in','feature_in'],
                             output_keys =  ['g_count_out'])
        self.bc = BaseControl()
        self.arm_srv = rospy.ServiceProxy('/servo/arm', StrTrg)
        self.navi_srv = rospy.ServiceProxy('navi_location_server', NaviLocation)
        self.head_pub =rospy.Publisher('/servo/head', Float64, queue_size=1)
        self.localize =rospy.ServiceProxy('/recognition/localize', RecognitionLocalize)
        self.multiple = rospy.ServiceProxy('/recognition/multiple_localize',MultipleLocalize)
        #self.guide = GuideGuests()

    def execute(self, userdata):
      #1ついてこさせる
      #2移動する
      #3
      #4
      #5
      #6
      #7
      #8
      #9
      #10
      #11
      #12
      #13
      #14
      #15
      #16
      #



      #ファイルの読み込み
        with open(pickle_path,'rb') as f:
            self.feature_dic = pickle.load(f)
          
        rospy.loginfo("Executing state:GUIDE_GUESTS")
        print('dict:')
        print(self.feature_dic)
        guest_num = userdata.g_count_in
        rospy.sleep(2.0)

       #ついてこさせる
        tts_srv("plese follow me")
        rospy.sleep(1.0)

        #移動する
        self.navi_srv('chairs_1_rcp')#テスト用にコメントアウト
        
        tts_srv("Moved to Order.")
        rospy.sleep(2.0)
        if guest_num == 0 :
            pass
            
        #空いている椅子を指す
          #やりたいこと
          #椅子の座標をとる
          #1つだけ取れたら、その椅子の座標をとる
          #2つ取れたら、人の座標もとって、その座標と遠いほうの椅子の座標をとる
          
        while 1:
            RANGE = 3.0 #　m 以下に椅子がある
            self.find_result = False
            #人の検知
            chairs = []
            points = self.multiple("chair").points #椅子の座標をとる
            if points: #指定した距離内の椅子だけ残す               
                for point in points:
                    i = 0
                    point_x,point_y = self.Calculate_Angle(points,i)#処理ができるようになるまで
                                
                    if (point_x < RANGE)and(point_y < RANGE): #指定した距離より近い椅子だけ残す
                        chairs.append([point_x,point_y]) #リストに追加
                        self.find_result= True
                rospy.sleep(1.0)
    
                if len(points) == 2:  # 2つの椅子の位置が取得できた時
                    points = self.multiple("person").points  # 人の座標を取得
    
                    nearest_distance = float('inf')  # 最も近い人との距離を無限大で初期化
                    nearest_person = None  # 最も近い人の座標を格納する変数を初期化
    
                    for person_point in points:  # 取得した人の座標に対してループ
                        point_x,point_y = person_point  # x座標とy座標を取り出す
    
                        distance = point_x**2 + point_y**2  # 原点からの距離を三平方の定理を用いて計算
    
                        if distance < nearest_distance:  # もし現在の人がこれまでで最も原点に近い場合
                            nearest_distance = distance  # 最も近い距離を更新
                            nearest_person = person_point  # 最も近い人の座標を更新
    
                    # この時点で nearest_person には最も原点に近い人の座標が格納されている
    
    
                    # 最も原点に近い人から一番近い椅子を見つける
                    most_dist = float('inf')
                    remove_chair = None
                
                    for chair_point in points:
                        point_x, point_y = chair_point  # 椅子のx座標とy座標を取り出す
                        dist = abs(nearest_person[0] - point_x) + abs(nearest_person[1] - point_y)  # マンハッタン距離を計算？？？
                
                        if dist < most_dist:
                            most_dist = dist
                            remove_chair = chair_point
    
                    if remove_chair:
                        points.remove(remove_chair)  # 最も近い椅子を椅子リストから取り除く
                        break
                    
                elif len(points) == 1:  # 椅子の位置が1つだけ取得できた場合
                    point_x, point_y = points[0]  # 最初の椅子の座標を取得
                    break
                
                else:  # 椅子が1つもないか、3つ以上の場合（要対策）
                    point_x, point_y = points[0]  # とりあえず最初の椅子の座標を使用
            
            # 検索結果がTrueの場合、椅子の位置点を出力
            if self.find_result == True:
                print(points)
                        
                angle = math.atan2(point_y,point_x) * (180/ math.pi)
                rospy.sleep(1.0)
                self.bc.rotateAngle(int(angle),0.2)
                rospy.sleep(0.5)
                self.arm_srv('point')
                rospy.sleep(0.5)
                wave_srv("/receptionist/sit.wav")#("Please sit in this chair.")
                rospy.sleep(0.5)
                
                rospy.sleep(1.0)
                
                self.arm_srv('carry')
                rospy.sleep(5.0)

                if guest_num == 0 :
                    guest_num += 1
                    userdata.g_count_out = guest_num
                    return 'guide_finish'

                    
                else:
                    self.sentence_list = userdata.feature_in
                    print(self.sentence_list)

                    # for i in range(len(self.sentence_list)):
                    #     tts_srv(self.sentence_list[i])
                    
                    #     i += 1
                    #tts_srv("Guest's name is Mike. His clothes are white. He wearing a hat. He is 180 centi miter tall.")

                    guest_num += 1
                    userdata.g_count_out = guest_num

                    tts_srv('finish receptionist')
                    return 'all_finish'
        

    
    def Calculate_Angle(self,points,i):
        print(points,"chair_num:" + str(i))
        point = str(points[i]).split()
        print(points)
        point_x = float(point[1])
        point_y = float(point[3])
        return point_x,point_y
        
                    

if __name__ == '__main__':
    
    rospy.init_node('receptionist_master')
    rospy.loginfo("Start receptionist")
    sm_top = smach.StateMachine(outcomes = ['finish_sm_top'])
    sm_top.userdata.guest_count = 0
    sm_top.userdata.features = []

    with sm_top:
        smach.StateMachine.add(
                'MOVE_INITAL_POSITION',
                MoveInitalPosition(),
                transitions = {'move_finish':'DISCOVERGUESTS_GUEST'},
                remapping = {'g_count_in':'guest_count',
                             "feature_in":"features",
                             "feature_out":"features"})

        smach.StateMachine.add(
                'DISCOVERGUESTS_GUEST',
                DiscoverGuests(),
                transitions = {'discover_finish':'INTRODUCE_GUESTS'},
                remapping = {'g_count_in':'guest_count',
                             "feature_in":"features",
                             "feature_out":"features"})

        smach.StateMachine.add(
                'INTRODUCE_GUESTS',
                IntroduceGuests(),
                transitions = {'introduce_finish':'GUIDE_GUESTS'},
                remapping = {"feature_in":"features",
                             "feature_out":"features",
                             'g_count_in':'guest_count'})

        smach.StateMachine.add(
                'GUIDE_GUESTS',
                GuideGuests(),
                transitions = {'guide_finish':'MOVE_INITAL_POSITION',
                               'all_finish':'finish_sm_top'},
                remapping = {'g_count_in':'guest_count',
                             'g_count_out':'guest_count',
                             "feature_in":"features",
                             "feature_out":"features",})

    outcome = sm_top.execute()
 
#rosrun person_feature_extraction gpt2_exam_realsense.py
