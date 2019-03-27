# -*- coding: utf-8 -*-
import unittest, requests


class TestEc(unittest.TestCase):

	def test_01search(self):
		url = 'http://www.errcode.tk/errcode.php?ErrCode=14410'
		content = requests.get(url)
		
if __name__=='__main__':
	unittest.main()