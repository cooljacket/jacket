# -*- coding: utf-8 -*-
from hw.models import College, School, Major, Course, Homework, ZAN
from django.core.urlresolvers import reverse

class ObjNum:
	HW = 5
	COURSE = 4
	MAJOR = 3
	SCHOOL = 2
	COLLEGE = 1

hw_zan_name = '作业这个应用'


def calBreadCrumbUrl(num, pk):
	"""
	1: 大学详情
	2: 学院详情
	3: 专业详情
	4: 课程详情
	5: 作业详情

	返回所对应的url
	"""
	if num == 0:
		return reverse('hw.views.college_all', args=())
	if num == ObjNum.COLLEGE:
		return reverse('hw.views.college_detail', args=(pk,))
	if num == ObjNum.SCHOOL:
		return reverse('hw.views.school_detail', args=(pk,))
	if num == ObjNum.MAJOR:
		return reverse('hw.views.major_detail', args=(pk,))
	if num == ObjNum.COURSE:
		return reverse('hw.views.course_detail', args=(pk,))
	return None


def getBreadUrls(num, pk):
	urls = [calBreadCrumbUrl(num, pk)]
	for i in range(num, 1, -1):
		if i == ObjNum.SCHOOL:
			pk = School.objects.get(id=pk).myCollege_id
		elif i == ObjNum.MAJOR:
			pk = Major.objects.get(id=pk).mySchool_id
		elif i == ObjNum.COURSE:
			pk = Course.objects.get(id=pk).myMajor_id
		elif i == ObjNum.HW:
			pk = Homework.objects.get(id=pk).myCourse_id
		urls.insert(0, calBreadCrumbUrl(i-1, pk))

	return urls


def get_hw_zan_num(request):
	try:
		hw_zan_num = ZAN.get_zan_num(name=hw_zan_name)
	except ZAN.DoesNotExist:
		hw_zan_num = 0
	return {'hw_zan_num': hw_zan_num}


def sub_mail_for_hw(request):
	pass      