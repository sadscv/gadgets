#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-1-18
# @Author  : sadscv
# @File    : test_drone.py
import unittest

from drone import Drone


class TestDrone(unittest.TestCase):

    def test_init(self):
        drone1 = Drone()
        drone2 = Drone('testcase/test_check.txt')
        with self.assertRaises(SystemExit):
            drone3 = Drone('wrongpath.txt')

    def test_fly(self):
        file1 = 'testcase/test_check.txt'

        # regular test: a drone with wrong position
        d0 = Drone(filepath=file1)
        self.assertEqual(d0.paths[-1], ('NA', 'NA', 'NA'))

        # regular test with float number and negtive number
        d1 = Drone()
        self.assertEqual(tuple(d1.pos), (0, 0, 0))
        d1._fly((1, 2, 3))
        self.assertEqual(tuple(d1.pos), (1, 2, 3))
        d1._fly((-1.5, 2.0, 3))
        self.assertEqual(tuple(d1.pos), (-0.5, 4, 6))

        # test invalid 'offset'
        with self.assertRaises(AssertionError):
            d1._fly((1, 2, 3, 4))


    def test_read_file(self):
        '''
            ===================
            test_ok.txt
            ===================
            plane1 1 1 1
            plane1 1 1 1 1 2 3
            plane1 2 3 4 1 1 1
            plane1 3 4 5 1 1 1
            plane1 4 5 6 1 2 3
            ===================
            test_singal.txt:
            ===================
            plane1 1 1 1
            plane1 1 1 1 1 2 3
            plane1 2 3 4 1 1 1
            plane1 3 4 5
            plane1 1 1 1 1 2 3
        '''

        path0 = 'testcase/test_ok.txt'
        path1 = 'testcase/test_signal.txt'
        path2 = 'testcase/test_error_format.txt'
        path3 = 'testcase/test_error_location.txt'
        path4 = 'testcase/wrongpath.txt'

        drone = Drone()
        self.assertEqual(drone.read_file(path0), True)
        self.assertEqual(drone.read_file(path1), False)
        self.assertEqual(drone.read_file(path2), False)
        self.assertEqual(drone.read_file(path3), False)
        with self.assertRaises(FileNotFoundError):
            drone.read_file(path4)

    def test_valid_signal(self):
        drone1 = Drone()
        # here are some test case for first seen strings
        # if drone1.id == None:
        #  means drone1 has never recieved strings before
        self.assertEqual(drone1.valid_signal('plane1 1 1'), False)
        drone1.id = None
        self.assertEqual(drone1.valid_signal('plane1 1 1 1'), True)
        drone1.id = None
        self.assertEqual(drone1.valid_signal('plane1 1.23 4.56 7.89'), False)
        drone1.id = None
        self.assertEqual(drone1.valid_signal('plane1 1 1 1 2 3'), False)
        drone1.id = None
        self.assertEqual(drone1.valid_signal('plane1 1 2 3 4 5 1'), False)
        drone1.id = 'plane1'

        # if not first time
        self.assertEqual(drone1.valid_signal('plane1 1 1'), False)
        self.assertEqual(drone1.valid_signal('plane1 1 1 1'), False)
        self.assertEqual(drone1.valid_signal('plane1 1 1 1 2 3'), False)

        # test other lines
        drone2 = Drone()
        drone2.id = 'plane1'
        drone2.pos = [1, 2, 3]
        self.assertEqual(drone2.valid_signal('plane1 1 2 3 4 5 1'), True)
        self.assertEqual(drone2.valid_signal('plane1 1 2 3 what? 5 1'), False)
        self.assertEqual(drone2.valid_signal('plane1 1 1 1 1 3  1 1e14 2'), False)

        # wrong name test
        drone3 = Drone()
        drone3.id = 'plane1'
        drone3.pos = [2, 4, 1]
        self.assertEqual(drone2.valid_signal('wrongname 2 4 1 3 43 2\n'), False)

    def test_is_digit(self):

        pos_samples = [1, -1, 0, 9007199254740991]
        neg_samples = [1.23, -4.56, 'abcd123']
        neutral_samples = [1.0000, -9007199254740991.00, 0.0]

        self.assertEqual(all([Drone.is_digit(s, int_only=True) for s in pos_samples]), True)
        self.assertEqual(all([Drone.is_digit(s, int_only=False) for s in pos_samples]), True)
        self.assertEqual(any([Drone.is_digit(s, int_only=True) for s in neg_samples]), False)
        self.assertEqual(any([Drone.is_digit(s, int_only=False) for s in neg_samples]), False)
        self.assertEqual(any([Drone.is_digit(s, int_only=True) for s in neutral_samples]), False)
        self.assertEqual(all([Drone.is_digit(s, int_only=False) for s in neutral_samples]), True)

    def test_check(self):
        '''
            ===================
           test_check.txt
            ===================
            plane1 1 1 1
            plane1 1 1 1 1 2 3
            plane1 2 3 4 1 1 1
            plane1 3 4 5 1 1 1
            plane1 4 5 6 1 2 3
        '''
        file1 = 'testcase/test_check.txt'

        drone1 = Drone(filepath=file1)
        self.assertEqual(drone1.check(0), 'plane1 0 1 1 1')
        self.assertEqual(drone1.check(2), 'plane1 2 3 4 5')
        self.assertEqual(drone1.check(4), 'Error: 4')
        self.assertEqual(drone1.check(100), 'cannot find 100')
        self.assertEqual(drone1.check(-1), 'invalid input')
        self.assertEqual(drone1.check('abc123'), 'invalid input')

if __name__ == '__main__':
    unittest.main()