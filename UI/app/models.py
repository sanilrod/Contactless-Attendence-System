from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):
    name = models.CharField(max_length=255)
    face_image1 = models.ImageField(max_length=255,upload_to="media/uploaded_images/")
    face_image2 = models.ImageField(max_length=255,blank=True,upload_to="media/uploaded_images/")
    face_image3 = models.ImageField(max_length=255,blank=True,upload_to="media/uploaded_images/")
    details = models.TextField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)

    username = models.CharField(max_length=255,null=True)
    password = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, null=True)


    def __str__(self):
        return str(self.name)


class AttendanceSetting(models.Model):
    college_time = models.CharField(max_length=255,null=True,help_text="In Am")
    attendance_time = models.CharField(max_length=255,null=True,help_text="In Am")
    no_late_marks = models.IntegerField(null=True,help_text="After which Absentee will be marked")
    no_early_marks = models.IntegerField(null=True,help_text="After which Absentee will be marked")
    half_day_time = models.CharField(max_length=255,null=True,help_text="In Am")
    checkout_time = models.CharField(max_length=255,null=True,help_text="In Pm")


class Attendance(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    teacher = models.CharField(max_length=255)
    attendance_marked = models.BooleanField(default=False)
    late_mark = models.BooleanField(default=False)
    half_day = models.BooleanField(default=False)
    image_path = models.CharField(max_length=255,null=True)

    def __str__(self):
        return str(self.teacher)+"==>"+str(self.date)


class Checkout(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    teacher = models.CharField(max_length=255)
    attendance_marked = models.BooleanField(default=False)
    early_mark = models.BooleanField(default=False)
    half_day = models.BooleanField(default=False)
    image_path = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.teacher) + "==>" + str(self.date)

