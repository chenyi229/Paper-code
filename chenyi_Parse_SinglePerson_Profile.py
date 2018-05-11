#coding:utf-8



"""
    Name: IMSLJYH_Parse_SinglePerson_Profile.py
    Function: 对于单个人物简历文本内容，进行分析。
    IO:
        In: 单个人物文本内容，一行，格式为：公司名|||姓名|||人物简介。
        Out: 分词后用于标注的数据，保存为 Excel文件。
    Useage:
        命令行使用格式为：
            > python IMSLZY_Parse_SinglePerson_Profile.py -Single_Person_Profile_File [-LabelDataResult_Filename]
            param:-Single_Person_Profile_File,已分词的单个简历文本
            param:-LabelDataResult_Filename，目标Excel文件，.xlsx
        例如：
            > python IMSLZY_Parse_SinglePerson_Profile.py Seg_PProfile_Single_0.txt [.xlsx文件名]
    Date: 2016.5.11
        
"""
from IMSLJYH_Lib_ComPersonProfileAnalysis import *

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# print "New File Encoding = ", sys.getfilesystemencoding()
Seg_PersonProfile_Filename = (sys.argv)[1]

# 如果指定了.xlsx文件名，则保存至指定位置。默认位置为./LabelResult.xlsx
if len(sys.argv) >=3:        
    LabelDataResult_Filename = (sys.argv)[2]
    pass
else:
    LabelDataResult_Filename = "./IMSLJYH-LabelResult.xlsx"    


# PersonProfile_Filename = "data.txt"
def PrepareLabelingData(Seg_PersonProfile_Filename,LabelDataResult_Filename):
    # Load and read segmented file.
    Seg_File = open(Seg_PersonProfile_Filename)
    Seg_ProfileStr = Seg_File.read()    #word1\label1 word2\label2 ...
    
    ''''
    PProfile_Single_Index_Number = int(re.findall("\d+", Seg_PersonProfile_Filename)[0])
    print PProfile_Single_Index_Number
    '''
    
    # 正则表达式，删除标签，用回车代替空格
    FinalSeg_ProfileStr = re.sub("/([a-zA-Z0-9]+)([_]?)([a-zA-Z0-9]*)([\\s]*)","\n", Seg_ProfileStr)
    
    Seg_File.close()
    WriteProfileStrIntoExcel(FinalSeg_ProfileStr, Seg_PersonProfile_Filename, LabelDataResult_Filename)
    pass    
    


def main():
    PrepareLabelingData(Seg_PersonProfile_Filename,LabelDataResult_Filename)
    pass

if __name__ == '__main__':
    main()
