from mongoengine import *
import datetime
from .models import *
import datetime
import re

def create_group(user_list, group_name):
	grps = WorkGroup.objects(name=group_name)
	if len(grps) > 0:
		raise ValueError("Group name '{}' has been used!")

	new_grp = WorkGroup(name=group_name, 
						members=user_list)
	new_grp.save()
	return new_grp

def today_isoformat():
	today = datetime.date.today()
	return today.isoformat()

def extract_xml_positions(s):
	"""
	Ignore the existence of the self-ending tags for now.
	This is a standard regex task. Check it.
	"""
	regex = re.compile(r'<.*?>')
	position_list = []
	tag_stack = []
	s_pointer = 0
	regex_iter = regex.finditer(s)
	for m in regex_iter:
		tag = m.group(0)
		

