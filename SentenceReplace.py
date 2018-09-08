# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 21:05:43 2018

@author: MB207-1
"""

import json
import jieba.posseg as pseg
from argparse import ArgumentParser


class Sentence_transform:
    
    def __init__(self, as_lib = False):
        
        self.BeingReplaceVerbList = []
        self.BeingReplaceNounList = []
        self.ReplaceNounList = []
        self.ReplaceVerbList = []
        
        parser = ArgumentParser()
        parser.add_argument("-o", default = "BlackCat_QAList(1).json" , type = str , help = "origin_path")
        parser.add_argument("-t", default = "Samsung_LocalCombination(1).json" , type = str , help = "transform_path")
        parser.add_argument("-s", type = str , help = "output_path")
        parser.add_argument("-name", type = str , help = "output_name")
        args = parser.parse_args()
        
        if not as_lib:
            self.transform(args.o, args.t, args.s, args.name)
        
    
    #檢查長度funtion
    def length(self, list1 = [], list2 = []):
        if (len(list1) == len(list2)):
            return True
        else:
            return False

    # 載入檔案
    def transform(self, origin_file, tranform_file,output_path, output_name):
        with open(origin_file, 'r', encoding = 'utf-8') as BeingReplaceFile:
            BeingReplaceData = json.load(BeingReplaceFile)
         
        BeingReplaceFile.close()
        
        with open(tranform_file, 'r', encoding = 'utf-8') as AfterReplaceFile:
            AfterReplaceData = json.load(AfterReplaceFile)
        
        AfterReplaceFile.close()
        
        #被替換的名詞與動詞 N V 
        for BeingReplaceKey, BeingReplaceItem in BeingReplaceData.items():
            for BeingReplaceValue in BeingReplaceItem:
                words = pseg.cut(BeingReplaceValue)
                for word, flag in words:
                    if(flag == 'n' and len(word) > 1):
                        self.ReplaceNounList.append(word)
                    if(flag == 'v' and len(word) > 1):
                        self.ReplaceVerbList.append(word)
                        
                self.BeingReplaceNounList.append(self.ReplaceNounList)
                self.BeingReplaceVerbList.append(self.ReplaceVerbList)
                self.ReplaceNounList = []
                self.ReplaceVerbList = []
        
        
        #處理list空的陣列
        Noun_BeingReplace= []
        for n in self.BeingReplaceNounList:
            if(len(n) > 0 ):
                Noun_BeingReplace.append(n)
         
        Verb_BeingReplace= []
        for v in self.BeingReplaceVerbList:
            if(len(v) > 0 ):
                Verb_BeingReplace.append(v)
        #################################
        
        
        #欲替換的名詞動詞list N V
        AfterReplaceNounList = []
        AfterReplaceVerbList = []
        for keys, item in AfterReplaceData.items():
            for value in item:
                try:
                    AfterReplaceNounList.append(value['n'])
                    AfterReplaceVerbList.append(value['v'])
                except:
                    pass
        
       
        #替換function
        def replaces(sentence ,FindList,ReplaceList):
            for FindItem, ReplaceItem in zip(FindList, ReplaceList):
                sentence = sentence.replace(FindItem, ""+ReplaceItem+"")
            return sentence
        
        
        # 先替換名詞
        sentenceNounList = []
        sentenceNounValue=""
        for BeingReplaceKey, BeingReplaceItem in BeingReplaceData.items():
            for BeingReplaceValue in BeingReplaceItem:
                 for N_BeingReplace, N_AfterReplace in zip(Noun_BeingReplace, AfterReplaceNounList):
                     sentenceNounValue= replaces(BeingReplaceValue, N_BeingReplace, N_AfterReplace)
                     sentenceNounList.append(sentenceNounValue)
                     
        FinalResultList = []
        sentenceVerb=""
        for sentenceNounItem in sentenceNounList:
            for V_BeingReplace, V_AfterReplace in zip(Verb_BeingReplace, AfterReplaceVerbList):
                sentenceVerb = replaces(sentenceNounItem, V_BeingReplace, V_AfterReplace)
                FinalResultList.append(sentenceVerb)
            
        
        print(FinalResultList)
       # with open(output_path + output_name + ".csv", "w", encoding = "utf-8-sig") as file:
           # for sv in sentenceVerb:
               # file.write(sv + "\n")
            
    
if __name__ == '__main__':
    s = Sentence_transform()       
    
    
    
    
    
    
    
    