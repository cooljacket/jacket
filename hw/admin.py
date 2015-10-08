from django.contrib import admin
from .models import College, School, Course, Homework, Teacher, Major, ZAN, Suggestion, IP, ZanOnce

# Register your models here. 
lst = [College, School, Course, Homework, Teacher, Major, ZAN, Suggestion, IP, ZanOnce]
for model in lst:
	admin.site.register(model)

# from django.contrib import admin
# from .models import College, School, Course, Teacher, Major

# # Register your models here. 
# lst = [College, School, Course, Teacher, Major]
# for model in lst:
# 	admin.site.register(model)
