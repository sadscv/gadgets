#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-4-18
# @Author  : sadscv
# @File    : textExtract.py
import json
import re


def readfile():
    save = None
    count = 0
    with open("data/trainSessionDeepMedic.txt", "r") as f:
        tmpfile = open("data/Epoch.txt", "wb")
        # split file
        for line in f:
            print(save)
            head = re.search("Starting new Epoch! Epoch", line, flags=0)
            if head:
                pos = re.search("#", line).span()[1]
                num = line[pos:pos + 2].rstrip("/")
                save = num
                open("data/Epoch_{}.txt".format(save), "wb")
                count += 1
                tmpfile = open("data/Epoch_{}.txt".format(save), "a")
            elif save:
                tmpfile.write(line)
        return count


def subfile_extract(epoch):
    with open("data/Epoch_{}.txt".format(epoch), "r") as f:
        class_json = {}
        for line in f:
            # 两行 whole epoch
            if re.search("finished. Reporting Accuracy over whole epoch.", line):
                tmp = []
                tmp_flag = False
                for i in range(4):
                    current_line = next(f)
                    if re.search('Finished sampling segment', current_line):
                        tmp_flag = True
                    if re.search("VALIDATION", current_line):
                        tmp.append(current_line)
                if tmp_flag:
                    tmp.append(next(f))
                class_json.update(json_generater(tmp, "whole"))
            # 8行 subepoch
            if re.search("Reporting Accuracy over whole epoch for Class", line):
                tmpval = []
                tmptrain = []
                for i in range(8):
                    current_line = next(f)
                    if re.search("VALIDATION", current_line):
                        tmpval.append(current_line)
                    if re.search("TRAINING", current_line):
                        tmptrain.append(current_line)
                if tmpval:
                    class_json.update(json_generater(tmpval, "validation"))
                if tmptrain:
                    class_json.update(json_generater(tmptrain, "training"))
        return json.dumps(class_json, indent=4)


def json_generater(lines, key=None):
    # 送进来8行，输出一个json. 代表epoch*-validation(or training)-class* 包含的数据
    # 如果长度为2，则是overall validation
    if len(lines) == 2:
        p0 = re.search("mean accuracy of epoch:", lines[0]).span()[1]
        p1 = re.search("mean accuracy of each subepoch:", lines[1]).span()[1]
        mean_accuracy = lines[0][p0:].split("=>")[0].strip()
        subepoch_accuracy = lines[1][p1:].strip()
        output_dict = {
            "mean accuracy of epoch": mean_accuracy,
            "mean accuracy of each subepoch": subepoch_accuracy
        }
        return {"overall": output_dict}

    if len(lines) == 8:
        accuracy = {}
        sensitivity = {}
        specificity = {}
        dice = {}
        # Todo 添加函数，重构重复代码。
        for i in range(len(lines)):
            if re.search("accuracy", lines[i]):
                accuracyidx = re.search("mean accuracy of epoch:", lines[i])
                accuracysubidx = re.search("mean accuracy of each subepoch:", lines[i])
                if accuracyidx:
                    accuracy.update({"epoch": lines[i][accuracyidx.span()[1]:].split("=>")[0].strip()})
                if accuracysubidx:
                    accuracy.update({"subepoch": lines[i][accuracysubidx.span()[1]:].strip()})
            elif re.search("sensitivity", lines[i]):
                sen_idx = re.search("mean sensitivity of epoch:", lines[i])
                sen_subidx = re.search("mean sensitivity of each subepoch:", lines[i])
                if sen_idx:
                    sensitivity.update({"epoch": lines[i][sen_idx.span()[1]:].split("=>")[0].strip()})
                if sen_subidx:
                    sensitivity.update({"subepoch": lines[i][sen_subidx.span()[1]:].strip()})
            elif re.search("specificity", lines[i]):
                spc_idx = re.search("mean specificity of epoch:", lines[i])
                spc_subidx = re.search("mean specificity of each subepoch:", lines[i])
                if spc_idx:
                    specificity.update({"epoch": lines[i][spc_idx.span()[1]:].split("=>")[0].strip()})
                if spc_subidx:
                    specificity.update({"subepoch": lines[i][spc_subidx.span()[1]:].strip()})
            elif re.search("dice", lines[i]):
                dice_idx = re.search("mean dice of epoch:", lines[i])
                dice_subidx = re.search("mean dice of each subepoch:", lines[i])
                if dice_idx:
                    dice.update({"epoch": lines[i][dice_idx.span()[1]:].strip()})
                if dice_subidx:
                    dice.update({"subepoch": lines[i][dice_subidx.span()[1]:].strip()})

        output = {
            "accuracy": accuracy,
            "sensitivity": sensitivity,
            "specificity": specificity,
            "dice": dice
        }
        l = lines[0][re.search("Class-", lines[0]).span()[1]:re.search("Class-", lines[0]).span()[1] + 1]
        return {key + '_class_' + l: output}


def main():
    count = readfile()
    for i in range(count):
        with open('data/Epoch_{}.json'.format(i), 'w+') as f:
            f.write(subfile_extract(i))

if __name__ == "__main__":
    main()
