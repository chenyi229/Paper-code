#coding:utf-8
'''
#########################################
#   Title:IMSLJYH_Lib_ComPersonProfileAnalysis.py
    Function:
        人物信息提取准备数据。
    Date:2016.05.09
#########################################
'''
import re
import sys
import copy
import cPickle
import numpy
#import openpyxl


# File Coding.
# print "Old File Encoding = ",sys.getfilesystemencoding()
reload(sys)
sys.setdefaultencoding("utf-8")
# print "New File Encoding = ",sys.getfilesystemencoding()

# PersonProfile_Filename = "PersonProfileData.txt"

PersonProfile_Filename = "./PersonProfileDataDir/PProfile_Single_0.txt"
Seg_PersonProfile_Filename = "./PersonProfileDataDir/PProfile_Single_Seg_0.txt"
LabelDataResult_Filename = "./IMSLJYH-LabelResult.xlsx"
#LabelProfileResult_Filename = "./LabelData_1.txt"

Cur_CompanyName = u""
Cur_PersonName = u""
TEST_PERSON_NUM = 1

# Unicode 格式转换，并进行空格去除
def ChangeUnicode(Contents):
    if type(Contents) != unicode:
        Contents = unicode(Contents, "UTF-8")
        pass
    #Contents = re.sub("\s","",Contents)
    return Contents
    pass    


def Divide_ProfileStr(PP_ProfileStr):
    
    """
    :param PP_ProfileStr: "公司|||姓名|||简历"
    :return: ProfileStr:"简历"
    :global: Cur_CompanyName, Cur_PersonName
    """

    global Cur_CompanyName, Cur_PersonName
    ProfileStr = ChangeUnicode(PP_ProfileStr)
    print "Original Person Profile Contents = ", ProfileStr
    Cur_CompanyName, Cur_PersonName, ProfileStr = ProfileStr.split('|||')
    return ProfileStr
    
def Segment_ProfileStr(PersonProfile_Filename):
    # Load and read file.
    PP_File = open(PersonProfile_Filename)
    PP_ProfileStr = PP_File.read()   # PP_ProfileStr = "公司|||姓名|||简历"

    ProfileStr = Divide_ProfileStr(PP_ProfileStr)   #ProfileStr = "简历"
    
    # 将简历内容分词
    # Seg_ProfileStr = Segment_ProfileStr(ProfileStr)
    Seg_File = open(Seg_PersonProfile_Filename)
    Seg_ProfileStr = Seg_File.read()    #word1\label1 word2\label2 ...
    
    # 正则表达式，删除标签，用回车代替空格
    FinalSeg_ProfileStr = re.sub(r"/([a-zA-Z0-9]+)([_]?)([a-zA-Z0-9]*)([\s]*)","\n", Seg_ProfileStr)
    
    Seg_File.close()
    PP_File.close()
    
    return FinalSeg_ProfileStr  #word1\nword2\n...

def WriteProfileStrIntoExcel(FinalSeg_ProfileStr, Seg_PersonProfile_Filename, LabelDataResult_Filename):
    work_book = openpyxl.load_workbook(LabelDataResult_Filename)
    # print work_book.get_sheet_names()
    cur_work_sheet = work_book.get_sheet_by_name("DataForLabel")

    print "work_sheet_title=",cur_work_sheet.title
    cnt_row = cur_work_sheet.max_row
    print cnt_row
    if cnt_row == 1:
        cnt_row = 0
        #PProfile_Single_Index_Number = 1
    else:
        cnt_row = cnt_row + 2
        '''
        Last_PProfile_Single_Index_Content = cur_work_sheet.cell(row = cnt_row, column = 1).value
        Last_PProfile_Single_Index_Number = int(re.findall("\d+", Last_PProfile_Single_Index_Content)[0])
        PProfile_Single_Index_Number = Last_PProfile_Single_Index_Number + 1
        '''
    # PProfile_Single_Index_Content = 'Text_Single_' + str(PProfile_Single_Index_Number)
        
    # 写入Excel：
    # ：第一列为原始分词后文本的文件名； 
    # ：第二列为分词结果（以从1计数的Begin_Text_Single_Index开始，End_Text_Single_Index结尾）
    
    # 1）写入第一行：标签Begin_Text_Single_Index
    cur_work_sheet.cell(row = cnt_row + 1,column = 1).value = Seg_PersonProfile_Filename    
    #cur_work_sheet.cell(row = cnt_row + 2,column = 1).value='Begin'
    
    # 2）将分词结果依次写入随后各行中
    Word_Items_List = re.split("\n", FinalSeg_ProfileStr)
    for word_id, word_item  in enumerate(Word_Items_List):
        #cur_work_sheet.cell(row = cnt_row + word_id + 2,column = 1).value = Seg_PersonProfile_Filename
        cur_work_sheet.cell(row = cnt_row + 2,column = word_id + 1).value=word_item
        
    # 3）写入最后一行：标签End_Text_Single_Index
    #cur_work_sheet.cell(row = cnt_row + word_id + 2,column = 1).value = Seg_PersonProfile_Filename
    cur_work_sheet.cell(row = cnt_row + 2,column = word_id + 1).value='End'
    
    work_book.save(LabelDataResult_Filename)
    
    pass
    
def PrepareLabelingData(PersonProfile_Filename,LabelDataResult_Filename):
    FinalSeg_ProfileStr = Segment_ProfileStr(PersonProfile_Filename)
    print "FinalSeg_ProfileStr=\n", FinalSeg_ProfileStr
    
    WriteProfileStrIntoExcel(FinalSeg_ProfileStr, LabelDataResult_Filename)
    pass    


def Divide_LPProfileStr_To_SinglePerson(LP_ProfileStr):
    SPP_FileName_List = []
    SPP_SinglePerson_Str_List = []
    ProfileStr = ChangeUnicode(LP_ProfileStr)
    ProfileStr = re.sub(r"([\n]*)(</Turn>\n</Section>\n</Episode>\n</Trans>)([\n]*)", "", ProfileStr)   #去掉文件尾 
    ProfileStr = ProfileStr.split('\n<Sync time="0"/>\n')
    profilestr_list = ProfileStr[1:]  #去掉文件头
    for index, profilestr_item in enumerate(profilestr_list):
        if index%2 == 0:
            SPP_FileName_List.append(profilestr_item)
        else:
            SPP_SinglePerson_Str_List.append(profilestr_item)        
        
    return SPP_FileName_List, SPP_SinglePerson_Str_List

def Divide_SinglePerson_To_Sentence(SinglePerson_Str_Item):    
    spp_sentence_str_item = [] 
    spp_sentence_label_item = []

    stritem_line_list = SinglePerson_Str_Item.split('\n')
    line_idx = 0
    while line_idx < len(stritem_line_list):
        line_item = stritem_line_list[line_idx]
        if (line_item == '' or re.match(r"([\s]+)", line_item)):     #空行
            line_idx += 1
            continue
        else:                   #非空行
            tag_label = re.match(r'<Event desc=', line_item)
            if not tag_label:   #无标签,标签记为‘O’
                spp_sentence_str_item.append(line_item)
                spp_sentence_label_item.append(u'O')
                line_idx += 1
                continue
            elif re.search(r'extent="begin"/>', line_item):
                                #有效标签起始行<extent="begin">
                label = re.findall( r'(?<=desc=").+?(?=")' , line_item )
                assert len(label) == 1
                label = label[0]
                line_idx += 1   #有效标签内容行
                line_item = stritem_line_list[line_idx]
                while(re.match(r'<Event desc=', line_item)):
                    line_idx += 1
                    line_item = stritem_line_list[line_idx]
                assert not re.match(r'<Event desc=', line_item)
                spp_sentence_str_item.append(line_item)
                spp_sentence_label_item.append(label)
                
                line_idx += 1   #有效标签终止行<extent="end">
                line_item = stritem_line_list[line_idx]
                while(not re.search(r'extent="end"/>', line_item)):
                    line_idx += 1
                    line_item = stritem_line_list[line_idx]
                assert re.search(r'extent="end"/>', line_item)
                
                line_idx += 1
                continue     
            else:               #无效标签
                assert re.search(r'extent="instantaneous"/>', line_item)
                line_idx += 1
                continue 
        
    return spp_sentence_str_item, spp_sentence_label_item
      
        
def Read_Single_LabelFile(LabelProfileResult_Filename):
    '''函数：读取并处理标注文件
    Input：原始单个标注文件
    Output：
        <1>SPP_FileName_List,原始简历文件名
            -[SFN1,SFN2,...] 
        <2>SPP_Sentence_Str_List, 简历内容按SinglePerson-Sentence划分结果
            -[[SS11,SS12,...],[SS21,SS22,...],...]
        <3>SPP_Sentence_Label_List, 每个SinglePerson-Sentence对应的标签
            -[[SL11,SL12,...],[SL21,SL22,...],...]
    '''
    # Load and read file.
    LP_File = open(LabelProfileResult_Filename)
    LP_ProfileStr = LP_File.read()   #LabelProfile_ProfileString
    
    # 将原始标记文件初步处理，以SinglePerson划分文本
    SPP_FileName_List, SPP_SinglePerson_Str_List = Divide_LPProfileStr_To_SinglePerson(LP_ProfileStr)   
    
    # 在SinglePerson下，以Sentence划分
    SPP_Sentence_Str_List = []
    SPP_Sentence_Label_List = []
    for SinglePerson_Str_Item in SPP_SinglePerson_Str_List:
        spp_sentence_str_item, spp_sentence_label_item = Divide_SinglePerson_To_Sentence(SinglePerson_Str_Item)
        SPP_Sentence_Str_List.append(spp_sentence_str_item)
        SPP_Sentence_Label_List.append(spp_sentence_label_item)
    
    return SPP_FileName_List, SPP_Sentence_Str_List, SPP_Sentence_Label_List
    
def Load_Dataset(Dataset_Filename):
    Dataset_File = open(Dataset_Filename, "rb")
    Dataset = cPickle.load(Dataset_File)
    SPP_FileName_List, SPP_Word_Str_List, SPP_Word_Label_List, SPP_Dict = Dataset
    Dataset_File.close()
    
    return SPP_FileName_List, SPP_Word_Str_List, SPP_Word_Label_List, SPP_Dict

def Index_Dataset(SPP_Word_List, Dict):
    SPP_Idx_List = copy.deepcopy(SPP_Word_List)    
    for psn_idx, psn_item in enumerate(SPP_Idx_List):
        for word_idx, word_item in enumerate(psn_item):
            SPP_Idx_List[psn_idx][word_idx] = Dict[word_item]
    
    SPP_Idx_Array = copy.deepcopy(SPP_Idx_List)
    for psn_idx, psn_item in enumerate(SPP_Idx_List):
        SPP_Idx_Array[psn_idx] = numpy.array(SPP_Idx_List[psn_idx], dtype = 'int32')
    
    return SPP_Idx_Array
    
def main():
    Load_Dataset(Dataset_Filename)
    
    
    
    pass

if __name__ == '__main__':
    main()