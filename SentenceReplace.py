# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 21:05:43 2018

@author: MB207-1
"""

import json
import jieba.posseg as pseg
from argparse import ArgumentParser
from gensim import models
import re

word2vecModel = models.Word2Vec.load('./file/word2vec.model')

class Sentence_transform:

    def __init__(self, as_lib=False):

        self.BeingReplaceVerbList = []
        self.BeingReplaceNounList = []
        self.ReplaceNounList = []
        self.ReplaceVerbList = []

        parser = ArgumentParser()
        parser.add_argument(
            "-o", default="C:/Users/USER/Desktop/NLP/8_30/Yuntech/sentence_transform/file/Phone_1.json", type=str, help="origin_path")
        parser.add_argument(
            "-t", default="C:/Users/USER/Desktop/NLP/8_30/Yuntech/sentence_transform/file/Samsung_Combination.json", type=str, help="transform_path")
        parser.add_argument("-s", type=str, help="output_path")
        parser.add_argument("-name", type=str, help="output_name")
        args = parser.parse_args()

        if not as_lib:
            self.transform(args.o, args.t, args.s, args.name)

    # 檢查長度funtion
    def length(self, list1=[], list2=[]):
        if (len(list1) == len(list2)):
            return True
        else:
            return False

    # 載入檔案
    def transform(self, origin_file, tranform_file, output_path, output_name):
        with open(origin_file, 'r', encoding='utf-8') as BeingReplaceFile:
            BeingReplaceData = json.load(BeingReplaceFile)

        BeingReplaceFile.close()

        with open(tranform_file, 'r', encoding='utf-8') as AfterReplaceFile:
            AfterReplaceData = json.load(AfterReplaceFile)

        AfterReplaceFile.close()

        #doubtSentencePatter ='\?|？|嗎|為什麼|什麼|如何|如果|若要|是否|請將|在哪|可能|多少|什麼|請教|請問|請益|問題|有沒有'
        for BeingReplaceDataValue in BeingReplaceData:
            #if(re.match(doubtSentencePatter,BeingReplaceDataValue['article_title'])):
            words = pseg.cut(BeingReplaceDataValue['article_title'])
            for word , flag in words:
                if(flag == 'n' and len(word) > 1):
                    self.ReplaceNounList.append(word)
                if(flag == 'v' and len(word) > 1 ):
                    self.ReplaceVerbList.append(word)
                    
            if(len(self.ReplaceNounList) > 0 ):
                for AfterReplaceDataItem in AfterReplaceData:
                    for AfterReplaceValue in AfterReplaceDataItem['item']:
                        if(self.length(AfterReplaceValue['n'],self.ReplaceNounList)):
                            try:
                                if(word2vecModel.wv.similarity(AfterReplaceValue['n'][0],self.ReplaceNounList[0]) > 0.5 and word2vecModel.wv.similarity(AfterReplaceValue['n'][1],self.ReplaceNounList[1]) > 0.5):
                                    sentence = BeingReplaceDataValue['article_title'].replace(self.ReplaceNounList[0],"("+AfterReplaceValue['n'][0]+")")
                                    sentence1 = sentence.replace(self.ReplaceNounList[1],"("+AfterReplaceValue['n'][1]+")")
                                    print(sentence1,AfterReplaceValue['sourceText'])
                            except:
                                pass
            
            self.ReplaceNounList = []
            self.ReplaceVerbList = []
                
        
        
        
        
        # with open(output_path + output_name + ".csv", "w", encoding = "utf-8-sig") as file:
        # for sv in sentenceVerb:
        # file.write(sv + "\n")
if __name__ == '__main__':
    s = Sentence_transform()
