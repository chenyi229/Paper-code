#coding:utf-8

"""
    Name: IMSLJYH_Prepare_Files_For_Label.py
    Function:
        1) 生成单个高管信息文件，到目录 PersonProfile_Single_DataDir/ 下。
        2) 生成待标记的文件，到目录 LabelData_Dir/ 下。
    Usage:
        python IMSLJYH_Prepare_Files_For_Label.py 
        param:-Div_Person_Num, 限定的人数量.
        param:-Num_Person, 每个待标注文件含有简历数量
        An Example:
            >python
"""


import os
import sys

reload(sys)

Div_Person_Num = 5000 #限定的人数量，高管信息中的前Div_Person_Num个

Num_Person = 100    # 每个文件包含100条简历文件

All_PersonProfile_File_Name = "All_PersonProfile_File.txt"  #未分词高管个人信息整体
Seg_All_PersonProfile_File_Name = "All_PersonProfile_File_Seg.txt"  #高管个人信息整体



PersonProfile_Single_Dirname = "PersonProfile_Single_DataDir"
Seg_PersonProfile_Single_Dirname = "Seg_PersonProfile_Single_DataDir"

PersonProfile_Single_Prefix = "PProfile_Single_"    # 未分词文本文件名前缀
Seg_PersonProfile_Single_Prefix = "Seg_PProfile_Single_"    # 分词文本文件名前缀

LabelData_Dirname = "DataForLabel_Dir"
LabelData_Prefix = "LabelData_"


# 1. 生成若干个单个任务简介文件
# 1.1 生成未分词单个任务简介文件
All_PersonProfile_File = open(All_PersonProfile_File_Name, 'r')
for profile_id in range(Div_Person_Num):
    if profile_id % 100 == 0:
        print "Single Id = ", profile_id
    pprofile_readline = All_PersonProfile_File.readline().strip()
    while (pprofile_readline == ''):
        pprofile_readline = All_PersonProfile_File.readline().strip()
    pprofile_file = file(os.path.join(PersonProfile_Single_Dirname, PersonProfile_Single_Prefix + str(profile_id) + ".txt") , 'w')
    pprofile_file.write(pprofile_readline)
    pprofile_file.close()
All_PersonProfile_File.close()

'''
# 1.2 生成分词单个任务简介文件
Seg_All_PersonProfile_File = open(Seg_All_PersonProfile_File_Name, 'r')
for profile_id in range(Div_Person_Num):
    if profile_id % 100 == 0:
        print "Single Id = ", profile_id
    pprofile_readline = Seg_PersonProfile_Single_Prefix.readline().strip()
    while (pprofile_readline == ''):
        pprofile_readline = Seg_All_PersonProfile_File.readline().strip()
    pprofile_file = file(os.path.join(Seg_PersonProfile_Single_Dirname, Seg_PersonProfile_Single_Prefix + str(profile_id) + ".txt") , 'w')
    pprofile_file.write(pprofile_readline)
    pprofile_file.close()
Seg_All_PersonProfile_File.close()
'''

# 读取单个未分词文件，每组个数：Num_Person，生成待标注文件
for label_id in range(1,11,1):    #1到10共10个文件，每个文件100条
    labeldata_file = file(os.path.join(LabelData_Dirname, LabelData_Prefix + str(label_id) + ".txt") , 'w')
    labeldata_file.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n' \
                        +'<!DOCTYPE Trans SYSTEM "trans-14.dtd">' + '\n' \
                        +'<Trans scribe="szpeter" audio_filename="frint980428" version="6" version_date="160526">' + '\n' \
                        +'<Episode>' + '\n' \
                        +'<Section type="report" startTime="0" endTime="20.0">' + '\n' \
                        +'<Turn startTime="0" endTime="20.0">' + '\n')
    for profile_id in range((label_id-1) * Num_Person, label_id * Num_Person, 1):
        f_name = os.path.join(PersonProfile_Single_Dirname, PersonProfile_Single_Prefix + str(profile_id) + ".txt")
        f_single = open(f_name, 'r')
        labeldata_readline = f_single.readline().strip()
        print f_name
        labeldata_file.write('<Sync time="0"/>' + "\n")
        labeldata_file.write(f_name + "\n")
        labeldata_file.write('<Sync time="0"/>' + "\n")
        labeldata_file.write(labeldata_readline + "\n\n")
        f_single.close()    
    labeldata_file.write('</Turn>' + '\n'\
                        +'</Section>' + '\n'\
                        +'</Episode>' + '\n'\
                        +'</Trans>')
    labeldata_file.close()


'''
# 2. 生成供测试的 test_lst.lst文件
Start_Person_Index = 0  #从0开始
End_Person_Index = 100   #不包含本身
Step_Person_Index = 1

if End_Person_Index >Div_Person_Num:
    End_Person_Index = Div_Person_Num
    
Test_Php_Lst_Filename = "test_lst.lst"
PersonProfile_Single_Path_Prefix = os.path.join(os.getcwd(), Seg_PersonProfile_Single_Dirname)
Test_Php_Lst_File = file(Test_Php_Lst_Filename, 'w')
#Test_Php_Lst_File.write(PersonProfile_Single_Path_Prefix + "\n")

for profile_id in range(Start_Person_Index,End_Person_Index,Step_Person_Index):    
    f_name = Seg_PersonProfile_Single_Prefix + str(profile_id) + ".txt"
    Test_Php_Lst_File.write(os.path.join(PersonProfile_Single_Path_Prefix, f_name) + "\n")
'''

'''    
for f_name in os.listdir(PersonProfile_Single_Dirname):
    if f_name.endswith(".txt"):
        Test_Php_Lst_File.write(os.path.join(PersonProfile_Single_Path_Prefix, f_name) + "\n")
'''



#Test_Php_Lst_File.close()
