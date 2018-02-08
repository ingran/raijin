# -*- coding: utf-8 -*-

import unittest
from raijin.raijin import Raijin


class TestBasicMethods(unittest.TestCase):

    def setUp(self):
        self.raijin = Raijin()

    def test_curDate(self):
        self.assertRegex(self.raijin.getCurDate(), '^([0-9]{2}-[0-9]{2}-[0-9]{4})$')

    def test_curTime(self):
        self.assertRegex(self.raijin.getCurTime(), '^([0-9]{2}:[0-9]{2}:[0-9]{2})$')

    def test_getMonth(self):
        self.assertEqual(1, self.raijin.getMonth("17-01-2017"))
        self.assertEqual(2, self.raijin.getMonth("17-02-2017"))
        self.assertEqual(3, self.raijin.getMonth("17-03-2017"))
        self.assertEqual(4, self.raijin.getMonth("17-04-2017"))
        self.assertEqual(5, self.raijin.getMonth("17-05-2017"))
        self.assertEqual(6, self.raijin.getMonth("17-06-2017"))
        self.assertEqual(7, self.raijin.getMonth("17-07-2017"))
        self.assertEqual(8, self.raijin.getMonth("17-08-2017"))
        self.assertEqual(9, self.raijin.getMonth("17-09-2017"))
        self.assertEqual(10, self.raijin.getMonth("17-10-2017"))
        self.assertEqual(11, self.raijin.getMonth("17-11-2017"))
        self.assertEqual(12, self.raijin.getMonth("17-12-2017"))

    def test_getWeekday(self):
        self.assertEqual(1, self.raijin.getWeekDay("16-01-2017"))
        self.assertEqual(2, self.raijin.getWeekDay("24-01-2017"))
        self.assertEqual(3, self.raijin.getWeekDay("01-02-2017"))
        self.assertEqual(4, self.raijin.getWeekDay("09-02-2017"))
        self.assertEqual(5, self.raijin.getWeekDay("17-02-2017"))
        self.assertEqual(6, self.raijin.getWeekDay("25-02-2017"))
        self.assertEqual(7, self.raijin.getWeekDay("05-03-2017"))

    def test_inTime(self):
        self.assertTrue(self.raijin.inTime("09:22:00", "09:00-10:00"))
        self.assertTrue(self.raijin.inTime("09:22", "09:00-10:00"))
        self.assertTrue(self.raijin.inTime("09:01", "09:00-10:00"))
        self.assertTrue(self.raijin.inTime("09:01", "09:00:00-10:00:00"))
        self.assertTrue(self.raijin.inTime("09:01:00", "09:00:00-10:00:00"))
        self.assertTrue(self.raijin.inTime("09:59:59", "09:00-10:00"))
        self.assertTrue(self.raijin.inTime("10:00:00", "09:00-10:00"))
        self.assertFalse(self.raijin.inTime("10:00:01", "09:00-10:00"))
        self.assertFalse(self.raijin.inTime("22:54", "09:00-10:00"))

    def test_isWorkable(self):
        self.assertTrue(self.raijin.isWorkable("16-01-2017"))
        self.assertTrue(self.raijin.isWorkable("24-01-2017"))
        self.assertTrue(self.raijin.isWorkable("01-02-2017"))
        self.assertTrue(self.raijin.isWorkable("09-02-2017"))
        self.assertTrue(self.raijin.isWorkable("17-02-2017"))
        self.assertFalse(self.raijin.isWorkable("25-02-2017"))
        self.assertFalse(self.raijin.isWorkable("05-03-2017"))
        self.assertFalse(self.raijin.isWorkable("06-01-2017"))
        self.assertEqual(self.raijin.isWorkable("02-03-20177"), {'message': 'Wrong date format. Expected format: [0-9]{2}-[0-9]{2}-[0-9]{4}'})
        self.assertEqual(self.raijin.isWorkable("2-3-2017"), {'message': 'Wrong date format. Expected format: [0-9]{2}-[0-9]{2}-[0-9]{4}'})

    def test_getHolidays(self):
        self.assertEqual(self.raijin.getHolidays(2017), {'2017': [[6], [], [20], [13, 14], [1, 2, 15], [], [], [15], [], [12], [1, 9], [6, 8, 25]]})
        self.assertEqual(self.raijin.getHolidays(20177), {'message': 'Wrong year format. Expected format: [0-9]{4}'})
        self.assertEqual(self.raijin.getHolidays(), {"2018": [[1, 6], [], [29, 30], [], [1, 2, 15], [], [], [15], [], [12], [1, 9], [6, 8, 24, 25, 31]],
                                                     '2017': [[6], [], [20], [13, 14], [1, 2, 15], [], [], [15], [], [12], [1, 9], [6, 8, 25]]})
        self.assertEqual(self.raijin.getHolidays(None, True), {'2018': ['01-01-2018', '06-01-2018', '29-03-2018', '30-03-2018', '01-05-2018', '02-05-2018', '15-05-2018', '15-08-2018', '12-10-2018', '01-11-2018', '09-11-2018'],
                                                               '2017': ['06-01-2017', '20-03-2017', '13-04-2017', '14-04-2017', '01-05-2017', '02-05-2017', '15-05-2017', '15-08-2017', '12-10-2017', '01-11-2017', '09-11-2017']})
        self.assertEqual(self.raijin.getHolidays(2017, True), {'2017': ['06-01-2017', '20-03-2017', '13-04-2017', '14-04-2017', '01-05-2017', '02-05-2017', '15-05-2017', '15-08-2017', '12-10-2017', '01-11-2017', '09-11-2017']})

    def test_getTariff(self):
        self.assertEqual("peak", self.raijin.getTariff("3.1", "31-01-2017 17:40:31"))
        self.assertEqual("flat", self.raijin.getTariff("3.1", "09-08-2017 09:22"))
        self.assertEqual("flat", self.raijin.getTariff("3.1", "09-08-2017 09:22:00"))
        self.assertNotEqual("flat", self.raijin.getTariff("3.1", "9-08-2017 09:22"))
        self.assertNotEqual("flat", self.raijin.getTariff("3.1", "9-08-2017 09:22:00"))
        self.assertEqual("valley", self.raijin.getTariff("3.1", "12-08-2017 15:28:31"))
        self.assertEqual(self.raijin.getTariff("3.1", "2-3-2017 16:24:12"), {'message': 'Wrong date format. Expected format: [0-9]{2}-[0-9]{2}-[0-9]{4}'})
        self.assertEqual(self.raijin.getTariff("3.1", "02-03-20177 16:24:12"), {'message': 'Wrong date format. Expected format: [0-9]{2}-[0-9]{2}-[0-9]{4}'})
        self.assertEqual(self.raijin.getTariff("3.1", "02-03-2017 16:24:122"), {'message': 'Wrong time format. Expected format: [0-9]{2}:[0-9]{2}:[0-9]{2} or [0-9]{2}:[0-9]{2}'})
        self.assertEqual("flat", self.raijin.getTariff("3.1", "02-03-2017 16:24"))
        self.assertRegex(self.raijin.getTariff("3.1", "02-03-2017")["message"], 'Wrong datetime format. Try with: ([0-9]{2}-[0-9]{2}-[0-9]{4}) ([0-9]{2}:[0-9]{2}:[0-9]{2})')
        #print(self.raijin.changeTime("26-03-2017"))
        self.assertEqual("peak", self.raijin.getTariff("3.1", "24-03-2017 17:40:31"))
        self.assertEqual("valley", self.raijin.getTariff("3.1", "25-03-2017 17:40:31"))
        self.assertEqual("valley", self.raijin.getTariff("3.1", "26-03-2017 17:40:31"))
        self.assertEqual("flat", self.raijin.getTariff("3.1", "27-03-2017 17:40:31"))
        self.assertEqual("flat", self.raijin.getTariff("3.1", "27-10-2017 17:40:31"))
        self.assertEqual("valley", self.raijin.getTariff("3.1", "28-10-2017 17:40:31"))
        self.assertEqual("valley", self.raijin.getTariff("3.1", "29-10-2017 17:40:31"))
        self.assertEqual("peak", self.raijin.getTariff("3.1", "30-10-2017 17:40:31"))

    def test_timeChange(self):
        self.assertTupleEqual(self.raijin.timeChange("25-03-2017"), ('29-10-2017', 1))
        self.assertTupleEqual(self.raijin.timeChange("26-03-2017"), ('29-10-2017', 217))
        self.assertTupleEqual(self.raijin.timeChange("28-10-2017"), ('29-10-2017', 1))
        self.assertTupleEqual(self.raijin.timeChange("29-10-2017"), ('25-03-2018', 147))
        self.assertEqual(self.raijin.timeChange("06-11-200000017"), {'message': 'Wrong date format. Expected format: [0-9]{2}-[0-9]{2}-[0-9]{4}'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
