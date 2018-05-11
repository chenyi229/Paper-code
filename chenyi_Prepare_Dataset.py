#coding:utf-8

"""
    Name: IMSLJYH_Prepare_Dataset.py
    Function:
        读取分词过后文件 PersonProfileForWordSeg_seg.txt, 建立Dataset。
    Output:
        
"""

from IMSLJYH_Lib_ComPersonProfileAnalysis import *
import os
import sys

reload(sys)

LabelData_Dir = "LabelData_Dir"
PersonProfileForWordSeg_Filename = "PersonProfileForWordSeg.txt"
PersonProfile_Seg_Filename = "PersonProfile_Seg.txt"
Dataset_Filename = "Dataset.pkl"

def Read_All_LabelFile(LabelData_Dir):
    '''函数：生成三个List（FileName，Sentence_Str, Sentence_Label）。
        Input:
        LabelData_Dir, 存放已标记的简历文本的文件夹
        Output: 
        SPP_FileName_List, SPP_Sentence_Str_List, SPP_Sentence_Label_List
    '''
    SPP_FileName_List = []
    SPP_Sentence_Str_List = []
    SPP_Sentence_Label_List = []    
    
    LabelProfileResult_Path_Prefix = os.path.join(os.getcwd(), LabelData_Dir)
    for f_name in os.listdir(LabelData_Dir):
        if f_name.endswith(".txt"):  
            f_full_name = os.path.join(LabelProfileResult_Path_Prefix, f_name)
            filename_list, sentence_str_list, sentence_label_list = Read_Single_LabelFile(f_full_name)
            SPP_FileName_List.extend(filename_list)
            SPP_Sentence_Str_List.extend(sentence_str_list)
            SPP_Sentence_Label_List.extend(sentence_label_list)
    
    return SPP_FileName_List, SPP_Sentence_Str_List, SPP_Sentence_Label_List


def Write_PersonProfile_For_Seg(LabelData_Dir,PersonProfileForWordSeg_Filename):    
    ''' 函数：写入待分词文件 PersonProfileForWordSeg_Filename
    ''' 
    SPP_FileName_List, SPP_Sentence_Str_List, SPP_Sentence_Label_List = Read_All_LabelFile(LabelData_Dir)      
    PersonProfileForWordSeg_File = file(PersonProfileForWordSeg_Filename, 'w')
    assert len(SPP_FileName_List) == len(SPP_Sentence_Str_List)
    nperson = len(SPP_FileName_List)
    for psn_idx in xrange(nperson):
        PersonProfileForWordSeg_File.write("<SPP-FileName>" + SPP_FileName_List[psn_idx] + "\n")
        nsentence = len(SPP_Sentence_Str_List[psn_idx])
        for stn_idx in xrange(nsentence):
            PersonProfileForWordSeg_File.write(SPP_Sentence_Str_List[psn_idx][stn_idx] + "\n")   
    PersonProfileForWordSeg_File.close()
    
    
def Build_Dataset(PersonProfile_Seg_Filename):
    SPP_FileName_List, SPP_Sentence_Str_List, SPP_Sentence_Label_List = Read_All_LabelFile(LabelData_Dir)
    SPP_Word_Label_List = []
    SPP_Word_Str_List = []
    
    PPSeg_File = open(PersonProfile_Seg_Filename, 'r')
    PPSeg_All_Lines = PPSeg_File.readlines()
    #PPSeg_All_Lines = ChangeUnicode(PPSeg_All_Lines)
    PPSeg_File.close()
           
    psn_idx = -1  #从0开始计数
    label_stn_idx = 0
    str_stn_idx = 0    
    for eachLine in PPSeg_All_Lines:
        eachLine = eachLine.strip()
        eachLine = ChangeUnicode(eachLine)
        #简历文本文件名
        if (re.match(r"(<+)", eachLine) and re.search(r"SPP-FileName", eachLine)):  
            psn_idx += 1
            stn_idx = 0
            continue
            
        #简历正文内容
        else:   
            # 正则表达式，删除标签，用空格分隔每个单词。
            eachLine = re.sub(r"/([a-zA-Z0-9]+)([_]?)([a-zA-Z0-9]*)([\s]*)"," ", eachLine)
            eachLine = eachLine.strip()
            eachLine_word_list = eachLine.split(" ")
            
            if (len(SPP_Word_Str_List) == psn_idx): #每个psn的第一句话 
                SPP_Word_Str_List.append(eachLine_word_list)
                cur_label = SPP_Sentence_Label_List[psn_idx][stn_idx]
                cur_label_list = []
                for i in range(len(eachLine_word_list)):
                    cur_label_list.append(cur_label) 
                SPP_Word_Label_List.append(cur_label_list)
                stn_idx += 1
                
            else:   #每个psn的第二句及以后的话
                SPP_Word_Str_List[psn_idx].extend(eachLine_word_list)
                cur_label = SPP_Sentence_Label_List[psn_idx][stn_idx]
                cur_label_list = []
                for i in range(len(eachLine_word_list)):
                    cur_label_list.append(cur_label) 
                SPP_Word_Label_List[psn_idx].extend(cur_label_list)
                stn_idx += 1
    #将标签换成（IOB）表示
    SPP_Word_Label_List = Change_To_IOB_Label(SPP_Word_Label_List)
    
    #分别对label和word建立Dictionary，初始Dict为空（如需利用已有Dict，则Build_Dict()第一个参数设为已有Dict）
    Dict_labels2idx = Build_Dict({},SPP_Word_Label_List)
    Dict_words2idx = Build_Dict({},SPP_Word_Str_List)
    SPP_Dict = dict(labels2idx = Dict_labels2idx, words2idx = Dict_words2idx)
    
    #建立Dataset
    Dataset = SPP_FileName_List, SPP_Word_Str_List, SPP_Word_Label_List, SPP_Dict
    return  Dataset               

def Change_To_IOB_Label(SPP_Word_Label_List):
    '''函数：Using the Inside Outside Beginning (IOB) representation.
    '''
    for list_idx, label_list in enumerate(SPP_Word_Label_List):
        #print "list_idx", list_idx
        #print "list:", SPP_Word_Label_List[list_idx]
        pre_label = u'O'
        for word_idx, cur_label in enumerate(label_list):
            if cur_label == u'O':
                SPP_Word_Label_List[list_idx][word_idx] = cur_label
            elif cur_label == pre_label:
                SPP_Word_Label_List[list_idx][word_idx] = 'I-' + cur_label
            else:
                SPP_Word_Label_List[list_idx][word_idx] = 'B-' + cur_label
            pre_label = cur_label
    return SPP_Word_Label_List


def Build_Dict(Dict, SPP_Word_List):
    for word_list in SPP_Word_List:
        for word_key in word_list:
            if (word_key not in Dict):
                new_value = len(Dict) + 1
                assert new_value not in Dict.values()
                Dict[word_key] = new_value
            else:
                continue
    return Dict

def Save_Dataset(Dataset, Dataset_Filename):
    Dataset_File = open(Dataset_Filename, "wb")
    cPickle.dump(Dataset, Dataset_File)
    Dataset_File.close()    

def Create_Dataset():
    Dataset = Build_Dataset(PersonProfile_Seg_Filename)
    Save_Dataset(Dataset, Dataset_Filename)
    SPP_FileName_List, SPP_Word_Str_List, SPP_Word_Label_List, SPP_Dict = Dataset
    
   
    
                        
def main():
    #Write_PersonProfile_For_Seg(LabelData_Dir,PersonProfileForWordSeg_Filename)
    
    Create_Dataset()
    
    print "Finished"
    
    pass

if __name__ == '__main__':
    main()


    



