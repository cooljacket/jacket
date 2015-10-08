# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from hw.models import College, School, Major, Course, Homework, ZAN, Suggestion
from hw.utils.bread import getBreadUrls, ObjNum, hw_zan_name
import datetime


# Create your views here.
def index(request):
	title = 'testing'
	return render(request, 'homework/test.html', locals())

def aboutMe(request):
	'''介绍网站'''
	title = '本站介绍'
	return render(request, 'about.html', locals())


def hw_detail(request, pk):
	'''作业详情'''
	title = '作业详情'
	
	try:
		hw = Homework.objects.get(id=pk)
	except Homework.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个作业'})

	breadUrls = getBreadUrls(ObjNum.HW, pk)
	return render(request, 'homework/hw.html', locals())


def hw_all_now(request, myMajor_id):
	'''某专业的所有正进行中的作业'''

	try:
		major = str(Major.objects.get(id=myMajor_id))
	except Major.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个专业'})

	title = '进行中的作业'
	now = datetime.datetime.now()
	courses = Course.objects.filter(myMajor_id=myMajor_id)
	breadUrls = getBreadUrls(ObjNum.MAJOR, myMajor_id)
	
	now_hws = []
	for c in courses:
		now_hws = now_hws + list(Homework.objects.filter(myCourse_id=c.id).filter(deadline__gt = now))
	now_hws.sort(key=lambda x:x.deadline, reverse=False)
	goto = reverse('hw.views.hw_all_pass', args=(myMajor_id,))
	for hw in now_hws:
		hw.myCourse.howToSubmit = hw.myCourse.howToSubmit.replace('\n', '<br>')
		hw.deadline = hw.deadline.strftime("%Y-%m-%d %H:%M %a")
	return render(request, 'homework/now_hws.html', locals())


def hw_all_pass(request, myMajor_id):
	'''某专业的所有已截止的作业'''

	try:
		major = str(Major.objects.get(id=myMajor_id))
	except Major.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个专业'})

	title = '已截止的作业'
	now = datetime.datetime.now()
	courses = Course.objects.filter(myMajor_id=myMajor_id)
	breadUrls = getBreadUrls(ObjNum.MAJOR, myMajor_id)

	pass_hws = []
	for c in courses:
		pass_hws = pass_hws + list(Homework.objects.filter(myCourse_id=c.id).filter(deadline__lte = now).order_by('deadline'))
	goto = reverse('hw.views.hw_all_now', args=(myMajor_id,))
	for hw in pass_hws:
		hw.myCourse.howToSubmit = hw.myCourse.howToSubmit.replace('\n', '<br>')
		hw.deadline = hw.deadline.strftime("%Y-%m-%d %H:%M %a")
	return render(request, 'homework/pass_hws.html', locals())


# 根据major来展示该专业开设的所有课程
def course_all(request, myMajor_id):
	'''某专业开设的所有课程'''

	try:
		myMajor = str(Major.objects.get(id=myMajor_id))
	except Major.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个专业'})

	title = '课程'
	courses = Course.objects.filter(myMajor_id=myMajor_id)
	breadUrls = getBreadUrls(ObjNum.MAJOR, myMajor_id)

	for c in courses:
		c.teachers = ', '.join([str(t.name) for t in c.mentor.all()])
		c.howToSubmit = c.howToSubmit.replace('\n', '<br>')
	return render(request, 'course/courses.html', locals())


def course_detail(request, pk):
	'''课程详情'''
	title = '课程详情'

	try:
		course = Course.objects.get(id=pk)
	except Course.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个课程'})

	breadUrls = getBreadUrls(ObjNum.COURSE, pk)[0:-1]
	
	if course is not None:
		course.teachers = ', '.join([str(t.name) for t in course.mentor.all()])
		course.howToSubmit = course.howToSubmit.replace('\n', '<br>')
		hws = Homework.objects.filter(myCourse_id=course.id).order_by('-deadline').values('name', 'id')
	return render(request, 'course/course.html', locals())


def major_all(request, mySchool_id):
	'''某学院的所有专业'''
	title = '专业'

	try:
		mySchool = str(School.objects.get(id=mySchool_id))
	except School.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个学院'})

	majors = Major.objects.filter(mySchool_id=mySchool_id)
	breadUrls = getBreadUrls(ObjNum.SCHOOL, mySchool_id)
	return render(request, 'major/majors.html', locals())


def major_detail(request, pk):
	'''专业详情'''
	title = '专业'
	
	try:
		major = Major.objects.get(id=pk)
		majorName = str(major)
	except Major.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个专业'})

	courseList = Course.objects.filter(myMajor_id=pk)
	breadUrls = getBreadUrls(ObjNum.MAJOR, pk)[0:-1]

	for c in courseList:
		c.teachers = ', '.join([str(t.name) for t in c.mentor.all()])
		c.howToSubmit = c.howToSubmit.replace('\n', '<br>')
	return render(request, 'major/major.html', locals())


def school_all(request, myCollege_id):
	'''某大学的所有学院'''
	title = '学院'

	try:
		collegeName = str(College.objects.get(id=myCollege_id))
	except College.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个课程'})

	schools = School.objects.filter(myCollege_id=myCollege_id)
	breadUrls = getBreadUrls(ObjNum.COLLEGE, myCollege_id)
	return render(request, 'school/schools.html', locals())


def school_detail(request, pk):
	'''某大学的所有学院'''
	title = '学院详情'
	
	try:
		school = School.objects.get(id=pk)
	except School.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个学院'})

	majors = Major.objects.filter(mySchool_id=school.id)
	breadUrls = getBreadUrls(ObjNum.SCHOOL, pk)[0:-1]
	return render(request, 'school/school.html', locals())


def college_all(request):
	'''所有大学'''
	title = '大学'
	colleges = College.objects.all()
	return render(request, 'college/colleges.html', locals())


def college_detail(request, pk):
	'''大学详情'''
	title = '大学详情'
	
	try:
		college = College.objects.get(id=pk)
	except College.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个大学'})

	if college:
		schools = School.objects.filter(myCollege_id=college.id) 
	return render(request, 'college/college.html', locals())


def add_hw_zan(request):
	"""给所有关于hw这个app的页面点赞"""
	hw_zan = ZAN.objects.get(name=hw_zan_name)
	hw_zan.num = hw_zan.num + 1
	hw_zan.save()
	return HttpResponse('(' + str(hw_zan.num) + ')')


def add_ok_num(request):
	"""我完成了，Homework中的OK_num自增1"""
	hid = request.GET.get('hid')
	try:
		hw = Homework.objects.get(id=hid)
	except Homework.DoesNotExist:
		return render(request, 'errors/404.html', {'err_msg': '并没有这个作业'})

	hw.OK_num = hw.OK_num + 1
	hw.save()
	return HttpResponse(str(hw.OK_num))


# def giveSuggestion(request):
# 	name = request.POST.get('name', 'nobody')
# 	email = request.POST.get('email', '233@666.com')
# 	suggestion = request.POST.get('suggestion', None)

# 	print(request.POST)
# 	print(name, email, suggestion)

# 	if suggestion:
# 		sug = Suggestion()
# 		print(name, email, suggestion)
# 		return HttpResponse(name+email+suggestion)

# 	return HttpResponse('hehe')

def giveSuggestion(request):
	name = request.GET.get('name', 'nobody')
	email = request.GET.get('email', '233@666.com')
	suggestion = request.GET.get('suggestion', None)

	if suggestion:
		sug = Suggestion(name=name, email=email, suggestion=suggestion)
		sug.save()
		return HttpResponse('谢谢你的反馈意见')

	return HttpResponse('反馈意见为空或传输数据出了故障，请稍后再试')

