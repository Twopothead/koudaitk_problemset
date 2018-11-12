# -*- coding:utf-8 -*-
import urllib
import json
import requests
from requests.exceptions import RequestException
import random 
import re
import os
import pathlib
from w3lib.html import remove_tags
import pypandoc
# you should pip install 'w3lib' & 'pypandoc' first
api4_koudaitiku_com_url = "http://api4.koudaitiku.com/"
current_dir = os.getcwd()  #/home/curie/gitcode/koudaitk_get
def get_name_pwd():
    # read userID and pwd from txt
    account = []
    f = open("name_pwd.txt", "r")   # 读取user.txt文件的账户和密码信息
    for user in f:     
        tmp = []                    # 每一行的信息临时列表    
        tmpUser, tmpPassword = user.split(" ", 1)   # 以空格拆分出每一行的用户名和密码，并存入tmpUser和tmpPassword变量中    
        tmp.append(tmpUser.strip())
        tmp.append(tmpPassword.strip())# 把tmp列表存入account列表中    
        account.append(tmp)         # 读取每一行
    f.close()
    name = account[0][0]
    pwd = account[0][1]
    return (name,pwd)

name,pwd = get_name_pwd()
sess = requests.session() # 创建可传递cookies的会话

login_url = "http://api4.koudaitiku.com/login.htm"
koudai_user = "kdtk/4.3.1 (com.yunti.kdtk; build:63 Android 23) okhttp/3.5.0"
ContentType = "application/x-www-form-urlencoded"
Host = "api4.koudaitiku.com"

login_headers_to_send = {
        'User-Agent': koudai_user,
        'Content-Type': ContentType,
        # 'Content-Length': 34,
        'Host': Host ,
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
        # Cookie: _kdsess=shjbun6avlukkhpyy5cplxy5qh4lhulaij2srmcbpsvqt2i64gcbtxyne6zdpw44rvnxohj7q
}

def login():
    login_form_data = 'name='+name+'&'+'pwd='+pwd
    l_response = sess.post(url=login_url, headers=login_headers_to_send,data=login_form_data)
    l_r=l_response.text
    print(l_r)
    return


def get_subject_id():
    subject_url = api4_koudaitiku_com_url+"/member/mistake/subject.htm"
    subject_r = sess.get(url=subject_url, headers=login_headers_to_send)
    # {"id":24076,"name":"组成原理","score":0}
    # print(json.dumps(json.loads(subject_r.text),ensure_ascii=False,indent=4))
    # json_save_to_path(subject_r.text, current_dir+"/get_json/subjectId.json")
    return
# subjectId :  政治 2; 英语一 18; 数学一 15; 计算机联考 5

subjects_dict = {'政治': 2, '英语一': 18, '数学一': 15,'计算机联考':5}

def json_save_to_path(text,json_file_path):
    with open(json_file_path, 'w') as f:
        json.dump(json.loads(text), f,ensure_ascii=False,indent=4)
    print("[already saved]:",json_file_path)
    return


def get_mistaked_problems_list_by_id_test(subjectId):
    mistakes_url = api4_koudaitiku_com_url+"/member/mistake/detail.htm"+"?"
    # NOTE! this "?" is very important!
    # 我的错题
    # subjectId :  政治 2; 英语一 18; 数学一 15; 计算机联考 5
    query_json = {'subjectId':subjectId,
    'page':1,
    'pageSize':10000
    }
    get_mistakes_url = mistakes_url + urllib.parse.urlencode(query_json) # "subjectId=2&page=1&pageSize=20"
    mistaked_problems_r = sess.get(url= get_mistakes_url, headers=login_headers_to_send)
    text = json.loads(mistaked_problems_r.text)
    print(json.dumps(text,ensure_ascii=False,indent=4))
    return 

def get_mistaked_problems_list_by_name(subject_name):
    subjectId = subjects_dict[subject_name]
    mistakes_url = api4_koudaitiku_com_url+"/member/mistake/detail.htm"+"?"
    # NOTE! this "?" is very important!
    # 我的错题
    # subjectId :  政治 2; 英语一 18; 数学一 15; 计算机联考 5
    query_json = {'subjectId':subjectId,
    'page':1,
    'pageSize':100000
    }
    get_mistakes_url = mistakes_url + urllib.parse.urlencode(query_json) # "subjectId=2&page=1&pageSize=20"
    mistaked_problems_r = sess.get(url= get_mistakes_url, headers=login_headers_to_send)
    path = current_dir+"/get_json/mistaked_problems_list_by_subject/"
    path_things(path)
    json_save_to_path(mistaked_problems_r.text,current_dir+"/get_json/mistaked_problems_list_by_subject/"+subject_name+".json")
    return 

def get_mistaked_problems_lists_and_save():
# 把各个学科所有错题的id按学科保存下来
    get_mistaked_problems_list_by_name('政治')
    # get_mistaked_problems_list_by_name(英语一)
    get_mistaked_problems_list_by_name('计算机联考')
    return

def test_get_exam_problem_details_by_Id(examId):
# 根据题目的id获取相应题目内容，在本代码文件中目前暂不使用    
    exam_details_url = api4_koudaitiku_com_url + "/examitem/detail.htm"+"?"
    # NOTE! this "?" is very important!
    query_json ={
        'examId': examId # eg.5719
    }

    get_exam_problem_details_by_Id_url = exam_details_url  + urllib.parse.urlencode(query_json)
    exam_details_by_id_r = sess.get(url= get_exam_problem_details_by_Id_url, headers=login_headers_to_send)
    text = json.loads(exam_details_by_id_r.text)
    print(json.dumps(text,ensure_ascii=False,indent=4))
    print(text['data']['description'])#　这里已经好了，没有反斜杠了
    return
def get_exam_problem_details_by_Id(examId):
# 根据题目的id获取相应题目内容，在本代码文件中目前暂不使用    
    exam_details_url = api4_koudaitiku_com_url + "/examitem/detail.htm"+"?"
    # NOTE! this "?" is very important!
    query_json ={
        'examId': examId # eg.5719
    }
    get_exam_problem_details_by_Id_url = exam_details_url  + urllib.parse.urlencode(query_json)
    exam_details_by_id_r = sess.get(url= get_exam_problem_details_by_Id_url, headers=login_headers_to_send)
    return exam_details_by_id_r.text

def get_dict_from_json_file(json_file_path):
    with open(json_file_path, 'r') as f:
        temp_dict = json.loads(f.read())
        # json.dump(json.loads(text), f,ensure_ascii=False,indent=4)
    return temp_dict

def test_problems_info(subject_name):
    data_dict_list = get_dict_from_json_file(current_dir+"/get_json/mistaked_problems_list_by_subject/"+subject_name+".json")['data']
    i = 1
    for data_dict in data_dict_list:
        # 这里的data_dict就是包含错题控制信息的单个东西
        print(str(i).zfill(3),"_",data_dict['name'])
        i += 1
        examItems = data_dict['examItems']
        for it in examItems:
            print(it['id'],end=" ")
            get_exam_problem_details_by_Id(it['id'])
        print("")
    return


def path_things(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True) 
    return


def problem_detail_html_save_to_path(problems_detail_json,detail_base_path,int_id):
    # print(problems_detail_json["data"]["description"])
    # print(problems_detail_json["data"]["solveGuide"])
    # 112_政治权利与义务 里　111111.txt有个服务器异常 {"msg": "服务器异常","code": "500"}
    if(problems_detail_json["code"]=="200"):
        with open(detail_base_path+str(int_id)+"_"+"description"+".htm", 'w') as f1:
            f1.write(problems_detail_json["data"]["description"])
        with open(detail_base_path+str(int_id)+"_"+"solveGuide"+".htm", 'w') as f2:
            f2.write(problems_detail_json["data"]["solveGuide"])
# 来．日哥再利用pandoc把保存的具体题目html页面转为latex
        name_description_htm = detail_base_path+str(int_id)+"_"+"description"+".htm"
        name_description_tex = detail_base_path+str(int_id)+"_"+"description"+".tex"
        name_solveGuide_htm = detail_base_path+str(int_id)+"_"+"solveGuide"+".htm"
        name_solveGuide_tex = detail_base_path+str(int_id)+"_"+"solveGuide"+".tex"
        out1 = pypandoc.convert_file(name_description_htm, 'tex', outputfile = name_description_tex, format='html')
        out2 = pypandoc.convert_file(name_solveGuide_htm, 'tex', outputfile = name_solveGuide_tex, format='html')
# 若是选择题，保存四个选项  
        if((problems_detail_json["data"]['answerTypeText']=="单选题") | (problems_detail_json["data"]['answerTypeText']=="多选题")):  
            handle_multiple_choice(problems_detail_json,detail_base_path,int_id)
            get_problem_detail_tex_sum(detail_base_path,int_id)

        # 事后删除中间文件
        # 这次只是选择
        os.remove(name_description_tex)
        os.remove(name_solveGuide_tex)
       

    else:
        print(problems_detail_json) # 服务器异常
    # grep -o "\"http.*\"" 5238_description.htm > 题目图片.txt
    return

def get_problem_detail_tex_sum(detail_base_path,int_id):
    # print("整合")
    name_description_tex = detail_base_path+str(int_id)+"_"+"description"+".tex"
    name_choices_tex = detail_base_path+str(int_id)+"_"+"choices"+".tex"
    name_solveGuide_tex = detail_base_path+str(int_id)+"_"+"solveGuide"+".tex"
    with open(name_description_tex, 'r') as f1:
            description = f1.readlines()
    with open(name_solveGuide_tex, 'r') as f2:
            solveGuide  = f2.readlines()
    with open(name_choices_tex, 'r') as f3:
            choices  = f3.readlines()
    with open(detail_base_path+str(int_id)+".tex", 'w') as f:
            f.write("\\question ")
            f.writelines(description)
            f.write("\\par") #题目与选项换行
            f.writelines(choices)
            f.write("\n\\begin{solution}")
            f.writelines(solveGuide)
            f.write("\\end{solution}")
            f.write("\n")
# 事后删除中间文件
    # os.remove(name_description_tex)
    os.remove(name_choices_tex)
    # os.remove(name_solveGuide_tex)
    return

def handle_multiple_choice(problems_detail_json,detail_base_path,int_id):
        if((problems_detail_json["data"]['answerTypeText']=="单选题") | (problems_detail_json["data"]['answerTypeText']=="多选题")):  
            
            if(problems_detail_json["data"]['examAnswers'][0]['trueOption']==1):
                print("[正确选项]",end=" ")       
            print(remove_tags(problems_detail_json["data"]['examAnswers'][0]['description']))
# <p>在坚持唯物论的同时，没有把唯物论和辩证法相结合</p> 我们要remove_tags因为要吧p标签啥的去掉
            if(problems_detail_json["data"]['examAnswers'][1]['trueOption']==1):
                print("[正确选项]",end=" ")   
            print(remove_tags(problems_detail_json["data"]['examAnswers'][1]['description']))

            if(problems_detail_json["data"]['examAnswers'][2]['trueOption']==1):
                print("[正确选项]",end=" ")      
            print(remove_tags(problems_detail_json["data"]['examAnswers'][2]['description']))

            if(problems_detail_json["data"]['examAnswers'][3]['trueOption']==1):
                print("[正确选项]",end=" ")      
            print(remove_tags(problems_detail_json["data"]['examAnswers'][3]['description'])) 

            with open(detail_base_path+str(int_id)+"_"+"choices"+".tex", 'w') as f:
                if(len(problems_detail_json["data"]['examAnswers'][0]['description']) > 13 ):
                    f.write("\\fourch{")# 选择题一个一行
                else:
                    f.write("\\twoch{")# 选择题两个一行

                if(problems_detail_json["data"]['examAnswers'][0]['trueOption']==1):f.write("\\textcolor{red}{")
                f.write(remove_tags(problems_detail_json["data"]['examAnswers'][0]['description']))
                if(problems_detail_json["data"]['examAnswers'][0]['trueOption']==1):f.write("}")
                f.write("}{")
                if(problems_detail_json["data"]['examAnswers'][1]['trueOption']==1):f.write("\\textcolor{red}{")
                f.write(remove_tags(problems_detail_json["data"]['examAnswers'][1]['description']))
                if(problems_detail_json["data"]['examAnswers'][1]['trueOption']==1):f.write("}")
                f.write("}{")
                if(problems_detail_json["data"]['examAnswers'][2]['trueOption']==1):f.write("\\textcolor{red}{")
                f.write(remove_tags(problems_detail_json["data"]['examAnswers'][2]['description']))
                if(problems_detail_json["data"]['examAnswers'][2]['trueOption']==1):f.write("}")
                f.write("}{")
                if(problems_detail_json["data"]['examAnswers'][3]['trueOption']==1):f.write("\\textcolor{red}{")
                f.write(remove_tags(problems_detail_json["data"]['examAnswers'][3]['description']))
                if(problems_detail_json["data"]['examAnswers'][3]['trueOption']==1):f.write("}")
                f.write("}")
            return

def save_problems_detail(subject_name):
    path_problems_detail=current_dir+"/problems_detail"
    path_things(path_problems_detail+"/politics")
    path_things(path_problems_detail+"/computer")
    if(subject_name == '政治'):
        path_subject_details = path_problems_detail+"/politics"
    if(subject_name == '计算机联考'):
        path_subject_details = path_problems_detail+"/computer"
    data_dict_list = get_dict_from_json_file(current_dir+"/get_json/mistaked_problems_list_by_subject/"+subject_name+".json")['data']
    # data_dict_list = get_dict_from_json_file(current_dir+"/"+subject_name+".json")['data']
    i = 1
    for data_dict in data_dict_list:
        # 这里的data_dict就是包含错题控制信息的单个东西
        print(str(i).zfill(3)+"_"+data_dict['name'].strip()) # 删除空白字符
        # path_point_name = path_subject_details + "/"+str(i).zfill(3)+"_"+data_dict['name'].strip()+"/"
        path_point_name = path_subject_details + "/"+str(i).zfill(3)+"_"+data_dict['name'].strip().replace("/","_")+"/"
        # I/O 被当成路径了
        path_things(path_point_name)
        i += 1
        examItems = data_dict['examItems']
        for it in examItems:
            print(it['id'],end=" ")
            file_problem_detail = path_point_name+str(it['id'])+".txt"
            problem_detail_text = get_exam_problem_details_by_Id(int(it['id']))
            json_save_to_path(problem_detail_text,file_problem_detail)
            problems_detail_json = json.loads(problem_detail_text)
            problem_detail_html_save_to_path(problems_detail_json,path_point_name,it['id'])
            # 这里把题干和解答都保存为htm页面
            # get_exam_problem_details_by_Id(it['id']) # answerType: 单选0 多选1 综合题4
        print("")
    return

login()
get_subject_id()
get_mistaked_problems_lists_and_save() #获得错题们的id

save_problems_detail('政治')
save_problems_detail('计算机联考')

   

