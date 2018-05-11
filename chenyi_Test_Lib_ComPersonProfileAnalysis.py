#coding:utf-8

'''
    Title: IMSLJYH_Test_Lib_ComPersonProfileAnalysis rpy
    Function:
        对 IMSLJYH_Lib_ComPersonProfileAnalysis.py 进行测试，对每个函数进行测试，注意，每个。
    Date: 2016.01.25

'''
from IMSLJYH_Lib_ComPersonProfileAnalysis import *
import os

def Test_WriteProfileStrIntoExcel():
    FinalSeg_ProfileStr = "林飞\n先生\n，\n中国\n国籍\n,\n无\n永久\n。\n"
    LabelDataResultFilename = "./IMSLJYH-LabelResult.xlsx"
    WriteProfileStrIntoExcel(FinalSeg_ProfileStr, LabelDataResultFilename)

def Test_Segment_ProfileStr():
    Final_Seg_ProfileStr = Segment_ProfileStr(PersonProfile_Filename)
    print Final_Seg_ProfileStr    
    
def Test_Divide_LPProfileStr_To_SinglePerson():
    LabelDataResult_Filename = "./LabelData_1.txt"
    LP_File = open(LabelDataResult_Filename)
    LP_ProfileStr = LP_File.read()
    SinglePerson_Profile_FileName_List, SinglePerson_Profile_LabelStr_List = Divide_LPProfileStr_To_SinglePerson(LP_ProfileStr)
    print "SinglePerson_Profile_FileName_List = ", SinglePerson_Profile_FileName_List
    #print len(SinglePerson_Profile_FileName_List)
    print "SinglePerson_Profile_LabelStr_List[0] = ", SinglePerson_Profile_LabelStr_List[0]
    #print len(SinglePerson_Profile_LabelStr_List)
    
    '''
    LabelData_Dirname = "LabelData_Dir"
    labeldata_file = file(os.path.join(LabelData_Dirname, "Test_SinglePerson_Profile_LabelStr_List" + ".txt") , 'w')
    labeldata_file.write(SinglePerson_Profile_LabelStr_List[0])
    labeldata_file.close()
    '''

def Test_Read_Single_LabelFile():
    LabelProfileResult_Filename = "./LabelData_1.txt"
    SPP_FileName_List, SPP_Sentence_Str_List, SPP_Sentence_Label_List = Read_Single_LabelFile(LabelProfileResult_Filename)
    print SPP_Sentence_Str_List[0]
    #print SPP_Sentence_Label_List
    print len(SPP_Sentence_Str_List[2])
    print len(SPP_Sentence_Label_List[2])
    print SPP_Sentence_Label_List[2][0]
    
def main():
    #Test_WriteProfileStrIntoExcel()
    #Test_Segment_ProfileStr()
    Test_Divide_LPProfileStr_To_SinglePerson()
    #Test_ReadLabelData()
    pass


if __name__ == '__main__':
    main()