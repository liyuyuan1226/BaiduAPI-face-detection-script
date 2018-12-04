# -*- coding: utf-8 -*-
import base64
import json
import requests
import os
import re
 
class BaiduPicIndentify:
    def __init__(self,img):
        self.AK = "your own AK"
        self.SK = "your own SK"
        self.img_src = img
        self.headers = {
            "Content-Type": "application/json; charset=UTF-8"
        }
        self.result_beaty = 0
        self.gender = ''
        self.age = ''
        self.race = ''
 
    def get_accessToken(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.AK + '&client_secret=' + self.SK
        response = requests.get(host, headers=self.headers)
        json_result = json.loads(response.text)
        return json_result['access_token']
 
    def img_to_BASE64(slef,path):
        with open(path,'rb') as f:
            base64_data = base64.b64encode(f.read())
            return base64_data
 
    def detect_face(self):
       
        img_BASE64 = self.img_to_BASE64(self.img_src)
        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
        post_data = {
            "image": img_BASE64,
            "image_type": "BASE64",
            "face_field": "gender,age,beauty,gender,race,expression",
            "face_type": "LIVE"
        }
        access_token = self.get_accessToken()
        request_url = request_url + "?access_token=" + access_token
        response = requests.post(url=request_url, data=post_data, headers=self.headers)
        json_result = json.loads(response.text)
        if json_result['error_msg']!='pic not has face':
            try:
                print("face_number:", json_result['result']['face_num'])
                print("beauty:", json_result['result']['face_list'][0]['beauty'])
                print("age:", json_result['result']['face_list'][0]['age'])
                print("gender:", json_result['result']['face_list'][0]['gender']['type'])
                print("race:", json_result['result']['face_list'][0]['race']['type'])

                self.gender = json_result['result']['face_list'][0]['gender']['type']
                self.age = json_result['result']['face_list'][0]['age']
                self.race = json_result['result']['face_list'][0]['race']['type']
                self.result_beaty = json_result['result']['face_list'][0]['beauty']
            except KeyError, e:
                print e.message
            
            # print("emotion:", json_result['result']['face_list'][0]['expression']['type'])

def readTxtByLine(path):
    dst = []
    if os.path.exists(path):
        f = open(path,'r')
        for line in f.readlines():
            line = line.strip()
            if not len(line) or line.startswith('#'):
                continue
            dst.append(line)
        f.close
    else:
        f = open(path,'w')
        f.close
    return dst

if __name__=='__main__':
    # # step1: write into a txt  
    # img_path = '/home/liyuyuan/Datasets/beauty_test/liyuyuan/'
    # # img_path = '/home/liyuyuan/Datasets/age+emotion_children_elder/beautiful/'
    # f1 = open('beauty_test.txt', 'w')
    
    # for file in os.listdir(img_path):
    #     img_src = img_path + file
    #     baiduDetect = BaiduPicIndentify(img_src)
    #     baiduDetect.detect_face()
    #     str_bea = str(baiduDetect.result_beaty) + "\n"
    #     # str_bea = str(result_beaty)
    #     f1.write(img_path + '@' + file + '@')
    #     f1.write(str_bea)
    # f1.close()

    # #step2: devide the face pictures into different score degrees
    # f2 = open('n000003_highmark50-60.txt', 'w')
    # gt_path = '/home/liyuyuan/Workspaces/baiduAPI/test/n000003.txt'
    # target_file = '/home/liyuyuan/Datasets/beauty_test/n03highmark50-60/'
    # os.mkdir(target_file)

    # pathlist = readTxtByLine(gt_path)
    # for line in pathlist:
    #     tmp = re.split(r'[@]', line)
    #     bea_value = float(tmp[2])
    #     if (bea_value > 50 and bea_value < 60):
    #         str_tmp = tmp[2] + "\n"
    #         f2.write(tmp[1] + '@')
    #         f2.write(str_tmp)
    #         try:
    #             os.symlink(tmp[0] + tmp[1], target_file + tmp[1])
    #         except:
    #             print target_file + 'exists'
    # f2.close()

    #step3
    img_txt = '/home/liyuyuan/Workspaces/python-workspace/baiduAPI/test/ImgAfterChoose.txt'
    f1 = open('/home/liyuyuan/Workspaces/python-workspace/baiduAPI/test/fullinformation.txt', 'w')
    f2 = open('/home/liyuyuan/Workspaces/python-workspace/baiduAPI/test/groundtruth.txt', 'w')
    pathlist = readTxtByLine(img_txt)
    count_male = 0
    count_female = 0
    for line in pathlist:
        tmp = re.split(r'[@]', line)
        person_name = tmp[0]
        person_id = tmp[1]
        img_src = tmp[2]
        baiduDetect = BaiduPicIndentify(img_src)
        baiduDetect.detect_face()
        if (baiduDetect.gender == 'male'):
            count_male += 1
        else:
            count_female += 1
        str_bea = str(baiduDetect.result_beaty) + "\n"
        str_age = str(baiduDetect.age) + "\n"
        f1.write(person_name + '@' + person_id + '@' + img_src + '@')
        f1.write(str(baiduDetect.age) + '@' + baiduDetect.race + '@' + baiduDetect.gender + '@')
        f1.write(str_bea)
        f2.write(person_name + '@' + person_id + '@' + img_src + '@')
        f2.write(str_bea)
    f1.write('count_male:' + str(count_male) + '\n')
    f1.write('count_female:' + str(count_female) )

    f1.close()
	f2.close()