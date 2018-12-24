#coding:utf-8
#from util.excel import *
from excel import *
	
class GetCase():
	def __init__(self,case_path,sheet_name):
		self.ex = Excel_r_w(case_path,sheet_name)
	
	def get_index(self):
		cases_index = {}#初始化用例集
		max_row = self.ex.get_max_row()
		for i in range(2,int(max_row)+2):
			case_n = self.ex.get_value('A'+str(i))
			step_desc = self.ex.get_value('B'+str(i))
			if case_n != None:
				case_name = case_n
				cases_index[case_name]=''
				index_start = i
			if case_n == None and step_desc == None:
				index_end = i
				index = [index_start,index_end]
				cases_index[case_name]=index
		return cases_index
		
	def get_cases(self,cases_index):
		cases = {}
		for case in cases_index:
			case_name = case
			index_start = cases_index[case][0]
			index_end = cases_index[case][1]
			case_name = {}
			for i in range(int(index_start),int(index_end)):
				step_desc = self.ex.get_value('B'+str(i))
				url = self.ex.get_value('C'+str(i))
				control_id = self.ex.get_value('D'+str(i))
				control_action = self.ex.get_value('E'+str(i))
				data = self.ex.get_value('F'+str(i))
				expectation = self.ex.get_value('G'+str(i))
				option = self.ex.get_value('H'+str(i))
				step = {'url':url,'control_id':control_id,'control_action':control_action,'data':data,'expectation':expectation,'option':option}
				case_name[step_desc] = step
			cases[case] = case_name
		return cases
if __name__=='__main__':
	g = GetCase(r'D:\python\unittest\errcodeWeb_test\test_case\test_search.xlsx','Sheet1')
	index = g.get_index()
	g.get_cases(index)
	


