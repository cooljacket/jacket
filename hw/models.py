# -*- coding: utf-8 -*-
from django.db import models
from DjangoUeditor.models import UEditorField
from django.core.urlresolvers import reverse

name_len = 30
icon_len = 30
longText = 400

# Create your models here.
class College(models.Model):
	"""College"""
	name = models.CharField('学校', max_length=name_len)
	icon = models.FileField(verbose_name='校徽')
	# intro = models.UEditorField('大学介绍', max_length=longText, blank=True, height=300, width='100%', toolbars='besttome')

	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		return reverse('college_detai', args=(self.id,))

	class Meta:
		verbose_name_plural = '大学'


class School(models.Model):
	"""School"""
	myCollege = models.ForeignKey(College, verbose_name='所属大学')
	name = models.CharField('学院', max_length=name_len)
	icon = models.ImageField('院徽')
	#intro = models.UEditorField('学院介绍', max_length=longText, blank=True, height=300, width='100%', toolbars='besttome')

	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		return reverse('school_detai', args=(self.id,))

	class Meta:
		verbose_name_plural = '学院'


class Teacher(models.Model):
	"""Teacher"""
	mySchool = models.ForeignKey(School, verbose_name='所属学院')
	name = models.CharField('姓名', max_length=name_len)
	phoneNumber = models.CharField('手机号码', max_length=11, blank=True)
	email = models.EmailField('邮箱', max_length=35, blank=True)

	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		return reverse('teacher_detai', args=(self.id,))

	class Meta:
		verbose_name_plural = '教师'


class Major(models.Model):
	"""Major"""
	mySchool = models.ForeignKey(School, verbose_name='所属学院')
	name = models.CharField('专业', max_length=name_len)
	year = models.DecimalField('年级', max_digits=4, decimal_places=0)

	def __str__(self):
		return str(self.name) + '(' + str(self.year) + ')'

	def get_absolute_url(self):
		return reverse('major_detail', args=(self.id,))

	class Meta:
		verbose_name_plural = '专业'


class Course(models.Model):
	"""Course"""
	myMajor = models.ForeignKey(Major, verbose_name='所属专业')
	mentor = models.ManyToManyField(Teacher, verbose_name='老师', max_length=name_len)
	name = models.CharField('课程', max_length=name_len)
	# howToSubmit = models.TextField('提交方式', max_length=longText)
	howToSubmit = UEditorField('提交方式', max_length=longText, height=300, width='100%', toolbars='besttome')
	homepage = models.URLField('课程主页', max_length=80, blank=True)
	# notice = models.CharField(max_length=longText)	# later
	# grading = UEditorField('给分方法', max_length=longText, height=300, width='100%', toolbars='besttome')

	def __str__(self):
		return str(self.name)

	def get_absolute_url(self):
		return reverse('course_detai', args=(self.id,))

	class Meta:
		verbose_name_plural = '课程'


class Homework(models.Model):
	"""Homework"""
	myCourse = models.ForeignKey(Course, verbose_name='所属课程')
	name = models.CharField('作业名称', max_length=name_len)
	deadline = models.DateTimeField('DDL')
	OK_num = models.SmallIntegerField('完成人数', default=0, editable=False)
	# memo = models.TextField('备注', max_length=longText, blank=True)
	# description = models.TextField('作业内容', max_length=longText)
	memo = UEditorField('备注', height=300, width='100%', toolbars='besttome', blank=True)
	description = UEditorField('作业内容', max_length=longText, height=300, width='100%', toolbars='besttome')
	topIt = models.BooleanField('置顶', default=False)

	def __str__(self):
		return str(self.name) + '(' + str(self.myCourse.name) + ')'

	def get_absolute_url(self):
		return reverse('homework_detai', args=(self.id,))

	class Meta:
		verbose_name_plural = '作业'


class Suggestion(models.Model):
	"""Suggestion for this app"""
	name = models.CharField('姓名', max_length=name_len, editable=False)
	email = models.EmailField('邮箱', editable=False)
	suggestion = models.CharField('反馈意见', max_length=longText, editable=False)

	def __str__(self):
		return str(self.name+self.email+self.suggestion)

	class Meta:
		verbose_name_plural = '反馈意见'


class ZAN(models.Model):
	"""Collecting zan from the website viewers"""
	num = models.PositiveIntegerField('赞', default=0)
	name = models.CharField('为什么赞', max_length=name_len)
	
	def get_zan_num(name):
		return ZAN.objects.get(name=name).num

	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name_plural = '赞'

# 要规定它不能被编辑，或者对于后台是隐藏的
class IP(models.Model):
	"""Recording the zan IP"""
	ip = models.GenericIPAddressField()

	class Meta:
		verbose_name_plural = 'IP'

class ZanOnce(models.Model):
	"""Allow zan only at most once"""
	num = models.PositiveIntegerField('赞', default=0)
	name = models.CharField('为什么赞', max_length=name_len)
	IPs = models.ManyToManyField(IP, verbose_name='ip列表', editable=False)
	
	def get_zan_num(name, ip):
		return ZAN.objects.get(name=name).num

	def __str__(self):
		return str(self.name)

	class Meta:
		verbose_name_plural = '只赞一次'