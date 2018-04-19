#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-4-18
# @Author  : sadscv
# @File    : textExtract.py
import json
import re


def savelines(line=None, file=None):
    pass

def readfile():
    SAVE = None
    count = 0
    with open("data/trainSessionDeepMedic.txt","r") as f:
        tmpfile = open("data/Epoch.txt", "wb")
        # split file
        for line in f:
            print(SAVE)
            head = re.search("Starting new Epoch! Epoch", line, flags=0)
            if head:
                pos = re.search("#", line).span()[1]
                num = line[pos:pos+2].rstrip("/")
                SAVE = num
                open("data/Epoch_{}.txt".format(SAVE), "wb")
                count += 1
                tmpfile = open("data/Epoch_{}.txt".format(SAVE), "a")
                # savelines(file=tmpfile)
                # tmpfile.close()
            elif SAVE:
                tmpfile.write(line)
                # with open("data/Epoch_{}.txt".format(SAVE), "a") as subf:
                #     subf.write(line)
        return count
        # read sub_file


def subfileExtract(epoch):
    with open("data/Epoch_{}.txt".format(epoch), "r") as f:
        classJson = {}
        for line in f:

            if re.search("finished. Reporting Accuracy over whole epoch.", line):
                tmp = []
                tmp_flag = False
                for i in range(4):
                    currentLine = next(f)
                    if re.search('Finished sampling segment', currentLine):
                        tmp_flag = True
                    if re.search("VALIDATION", currentLine):
                        tmp.append(currentLine)
                if tmp_flag:
                    tmp.append(next(f))

                #Todo: bug! epoch_20.txt中， 多出一行 'Finished sampling segments...'
                classJson.update(JSONGenerater(tmp, "whole"))

            if re.search("Reporting Accuracy over whole epoch for Class", line):
                tmpval = []
                tmptrain = []
                for i in range(8):
                    currentLine = next(f)
                    if re.search("VALIDATION", currentLine):
                        tmpval.append(currentLine)
                    if re.search("TRAINING", currentLine):
                        tmptrain.append(currentLine)
                if tmpval:
                    classJson.update(JSONGenerater(tmpval, "validation"))
                if tmptrain:
                    classJson.update(JSONGenerater(tmptrain, "training"))
                # for t in tmptrain:
                #     print(t)
        return json.dumps(classJson, indent=4)



def JSONGenerater(lines,  key=None):
    # 送进来8行，输出一个json. 代表epoch*-validation(or training)-class* 包含的数据
    # 如果长度为2，则是overall validation
    if len(lines) == 2:
        p0 = re.search("mean accuracy of epoch:", lines[0]).span()[1]
        p1 = re.search("mean accuracy of each subepoch:", lines[1]).span()[1]
        meanAccuracy = lines[0][p0:].split("=>")[0].strip()
        subepochAccuracy = lines[1][p1:].strip()
        dict = {
                "mean accuracy of epoch":meanAccuracy,
                "mean accuracy of each subepoch":subepochAccuracy
                }
        return {"overall":dict}

    if len(lines) == 8:
        accuracy = {}
        sensitivity = {}
        specificity = {}
        Dice = {}
        # Todo 添加函数，重构重复代码。
        for i in range(len(lines)):
            if re.search("accuracy", lines[i]):
                accuracyidx = re.search("mean accuracy of epoch:", lines[i])
                accuracysubidx = re.search("mean accuracy of each subepoch:", lines[i])
                if accuracyidx:
                    accuracy.update({"epoch":lines[i][accuracyidx.span()[1]:].split("=>")[0].strip()})
                if accuracysubidx:
                    accuracy.update({"subepoch":lines[i][accuracysubidx.span()[1]:].strip()})
            elif re.search("sensitivity", lines[i]):
                sen_idx = re.search("mean sensitivity of epoch:", lines[i])
                sen_subidx = re.search("mean sensitivity of each subepoch:", lines[i])
                if sen_idx:
                    sensitivity.update({"epoch":lines[i][sen_idx.span()[1]:].split("=>")[0].strip()})
                if sen_subidx:
                    sensitivity.update({"subepoch":lines[i][sen_subidx.span()[1]:].strip()})
            elif re.search("specificity", lines[i]):
                spc_idx = re.search("mean specificity of epoch:", lines[i])
                spc_subidx = re.search("mean specificity of each subepoch:", lines[i])
                if spc_idx:
                    specificity.update({"epoch":lines[i][spc_idx.span()[1]:].split("=>")[0].strip()})
                if spc_subidx:
                    specificity.update({"subepoch":lines[i][spc_subidx.span()[1]:].strip()})
            elif re.search("Dice", lines[i]):
                Dice_idx = re.search("mean Dice of epoch:", lines[i])
                Dice_subidx = re.search("mean Dice of each subepoch:", lines[i])
                if Dice_idx:
                    Dice.update({"epoch":lines[i][Dice_idx.span()[1]:].strip()})
                if Dice_subidx:
                    Dice.update({"subepoch":lines[i][Dice_subidx.span()[1]:].strip()})

        output = {
            "accuracy":accuracy,
            "sensitivity":sensitivity,
            "specificity":specificity,
            "Dice":Dice
        }
        l = lines[0][re.search("Class-", lines[0]).span()[1]:re.search("Class-", lines[0]).span()[1]+1]
        return {key+'_class_'+l:output}





if __name__ == "__main__":
    count = readfile()
    # for i in range(1, 20):
    #     print("$"* 20, i)
    #     subfileExtract(i)
    for i in range(count):
        with open('data/Epoch_{}.json'.format(i), 'w+') as f:
            f.write(subfileExtract(i))