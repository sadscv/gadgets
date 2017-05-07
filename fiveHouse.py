#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 17-5-4 下午11:45
# @Author  : sadscv
# @File    : fiveHouse.py
import copy
import random as rd
global is_satisfied

host = [1, 2, 3, 4, 5]
house_position = [1, 2, 3, 4, 5]
house_color = ['red', 'white', 'green', 'yellow', 'blue']
drink = ['tea', 'coffee', 'milk', 'beer',  'water']
tobacco = ['PALL MALL','DUNHILL','BLEND','BLUE MASTER','PRINCE']
pet = ['dog', 'bird', 'cat', 'horse', 'fish']
country = ['England', 'Sweden', 'Denmark', 'Norway', 'German']

list_names = ('house_position', 'house_color', 'country', 'drink', 'tobacco', 'pet')

class Host(object):
    def __init__(self):
        pass

def print_p(person):
    print(''.join(['%s:%-12s' % item for item in person.__dict__.items()]))


def get_one(type):
    random = rd.randint(0, 100)
    pop = type.pop(random % len(type))
    return pop

def re_adjust(p_list, lists, conditions):
     for p in p_list:
         for condition in conditions:
            if getattr(p, condition[0][0], None) == condition[0][1]:
                setattr(p, condition[1][0], condition[1][1])
                list = lists[condition[1][0]]
                list.remove(condition[1][1])

def remove_element(lists, p, a, b):
    if b in lists[a]:
        lists[a].remove(b)
        setattr(p, a, b)

def constrained(person, conditions):
    for p in person:
        for condition in conditions:
            if getattr(p, condition[0][0]) == condition[0][1]:
                if getattr(p, condition[1][0]) != condition[1][1]:
                    is_satisfied = 0
                    return 0

    return 1

def constrained_position(person, conditions):
    constrain_satisfied = 0
    for c in conditions:
        _tmp_dict = []
        for p in person:
            if getattr(p, c[0][0]) == c[0][1] or getattr(p, c[1][0]) == c[1][1]:
                _tmp_dict.append(p)
        if len(_tmp_dict) == 2:
            if _tmp_dict[0].house_position - _tmp_dict[1].house_position == 1:
                constrain_satisfied += 1
    if constrain_satisfied == len(conditions):
        return 1
    return - constrain_satisfied

def assign(house_position, house_color, country, drink, tobacco, pet, conditions):

    lists = {
        'house_position' : house_position,
        'house_color' : house_color,
        'country' : country,
        'drink': drink,
        'tobacco' : tobacco,
        'pet' : pet
    }
    p_list = []
    for i in range(5):
        p_list.append(Host())
    for list_name in list_names:
        for p in p_list:
            if getattr(p, list_name, None) is None:
                random = rd.randint(0, 100)
                pop = lists[list_name].pop(random % len(lists[list_name]))
                setattr(p, list_name, pop)
        for p in p_list:
            for condition in conditions:
                if getattr(p, condition[0][0], None) == condition[0][1]:
                    tmp_a, tmp_b = condition[1][0], condition[1][1]
                    if getattr(p, tmp_a, None) is None:
                        if tmp_b in lists[tmp_a]:
                            setattr(p, tmp_a, tmp_b)
                            lists[tmp_a].remove(tmp_b)
    print('#' * 120)
    for p in p_list:
        print_p(p)
    print('@' * 120)
    return p_list


def main():
    is_satisfied = -1
    data = (house_position, house_color, country, drink, tobacco, pet)
    while(is_satisfied != 1):
        _data = copy.deepcopy(data)
        condition_1 = [('house_color', 'red' ), ('country', 'England')]
        condition_2 = [('country', 'Sweden'), ('pet', 'dog')]
        condition_3 = [('country', 'Denmark'), ('drink', 'tea')]
        condition_4 = [('house_color', 'green'), ('drink', 'coffee')]
        condition_5 = [('tobacco', 'PALL MALL'), ('pet', 'bird')]
        condition_6 = [('house_position', '3'), ('drink', 'milk')]
        condition_7 = [('house_color', 'yellow'), ('tobacco', 'DUNHILL')]
        condition_8 = [('house_position', '1'), ('country', 'Norway') ]
        condition_9 = [('drink', 'beer'), ('tobacco', 'BLUE MASTER')]
        condition_10 = [('country', 'German'), ('tobacco', 'PRINCE')]
        conditions = [condition_1, condition_2, condition_3, condition_4, condition_5,
                      condition_6, condition_7,condition_8, condition_9, condition_10]
        restriction_1 = [('pet', 'horse'), ('tobacco', 'DUNHILL')]
        restriction_2 = [('house_color', 'green'), ('house_color', 'white')]
        restriction_3 = [('tobacco', 'BLEND'), ('pet', 'cat')]
        restriction_4 = [('country', 'Norway'), ('house_color', 'blue')]
        restriction_5 = [('tobacco', 'BLEND'), ('drink', 'water')]
        restrictions = [restriction_1, restriction_2, restriction_3, restriction_4, restriction_5]
        person = assign(_data[0], _data[1], _data[2], _data[3], _data[4], _data[5], conditions)
        is_satisfied = constrained(person, conditions)
        print(is_satisfied)
        if is_satisfied ==1:
            is_satisfied = constrained_position(person, restrictions)
        print(is_satisfied)

def test():
    sum =1
    for i in range(9):
        sum = sum * (i + 1)
    print(sum)



if __name__ == '__main__':
    # main()
    test()