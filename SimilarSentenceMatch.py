# vim: set ts=4 sw=4 et: -*- coding: utf-8 -*-
import distance
import json
import csv
from argparse import ArgumentParser


class Similar():

    def __init__(self, as_lib=False):

        # 相似度指標
        self.Similarity_threshold = 0.1

        # 參數設定
        parser = ArgumentParser()

        parser.add_argument("-th", default="0.1", type=float,
                            help="threshold 0.1-1.0 ")
        parser.add_argument("-s",  type=str, help="save_path ")
        parser.add_argument("-name", type=str, help="save_name ")
        parser.add_argument(
            "-t", default="GenerateSentenceList(1).json", type=str, help="tranform json file")
        parser.add_argument("-g", default="ReferenceSentenceList.json",
                            type=str, help="Good sentence json file ")
        args = parser.parse_args()

        if not as_lib:
            self.Comparison(args.th, args.s, args.name,  args.t, args.g)

    def similarity(self, stringOne, stringTwo):
        d = distance.levenshtein(stringOne, stringTwo)
        longest = max(len(stringOne), len(stringTwo))
        return (longest - d) / longest

    def Comparison(self, threshold, save_path, save_name, GenerateSentenceListPath="ReferenceSentenceList.json"
                   ):

         # 替換後生成句的檔案
        GS_path = GenerateSentenceListPath

        # 優良句檔案(作為匹配生成句相似度用)
        RS_path = ReferenceSentenceListPath

        save = []

        with open(GS_path, 'r', encoding='utf-8') as GenerateSentenceData:
            GenerateSentenceListPath = json.load(GenerateSentenceData)

            GenerateSentenceData.close()

        with open(RS_path, 'r', encoding='utf-8') as ReferenceSentenceData:
            ReferenceSentenceListPath = json.load(ReferenceSentenceData)

            ReferenceSentenceData.close()

        for GenerateSentence in GenerateSentenceListPath:
            for ReferenceSentence in ReferenceSentenceListPath:
                if(self.similarity(GenerateSentence, ReferenceSentence) > self.Similarity_threshold):
                    print('相似度=', round(self.similarity(GenerateSentence, ReferenceSentence),
                                        3), '優良句=', ReferenceSentence, '相似句=', GenerateSentence)
                    save.append('相似度= ' + str(round(self.similarity(GenerateSentence, ReferenceSentence), 3)) +
                                '優良句= ' + str(ReferenceSentence) +
                                '相似句= ' + GenerateSentence)

        with open(save_path + save_name + '.csv', "w", encoding="utf-8-sig") as file:
            write = csv.writer(file)
            for s in save:
                write.writerows(zip([s]))


if __name__ == '__main__':
    S = Similar()
