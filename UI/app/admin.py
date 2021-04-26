from django.contrib.auth.models import Group

from django.contrib import admin
from import_export import resources

from .models import *
from django.utils.html import format_html
import numpy as np
from random import randint
from django.utils import timezone
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin, ExportMixin


#Teacher,user,name,face_image1,face_image2,face_image3,details,address
#AttendanceSetting,college_time,college_time,no_late_marks,half_day_time,checkout_time
#Attendance,date,teacher,attendance_marked,late_mark,half_day
#Checkout,date,teacher,checkout_marked,early_mark,half_day


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



# class BookAdmin():
#     resource_class = BookResource

class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
        fields = ("id","name","face_image1","face_image2","face_image3","details","address","username","password","email")
        export_order = ('id',"name","face_image1","face_image2","face_image3","details","address","username","password","email")


class TeacherAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ("name","details","address","username","password","email")
    list_display = ("name","total_absentee","face_image1","face_image2","face_image3","details","address","username","password","email")
    resource_class = TeacherResource
    readonly_fields = ("total_absentee",)

    def total_absentee(self,obj):
        total_absentee_no = int(len(Attendance.objects.filter(teacher=obj.name,late_mark=True))/AttendanceSetting.objects.all()[0].no_late_marks) +  int(len(Checkout.objects.filter(teacher=obj.name,early_mark=True))/AttendanceSetting.objects.all()[0].no_early_marks)
        return format_html("<b><i>" + str(total_absentee_no) + "</i></b>")



    def teacher_name(self, obj):
        return format_html("<b>" + obj.teacher + "</b>")

    def save_model(self, request, obj, form, change):

        if (change):
            owner_object = self.model.objects.get(id=obj.id)
            user = User.objects.get(username=owner_object.username)
            user.username = obj.username
            user.set_password(obj.password)
            user.save()
        else:
            unique_id = random_with_N_digits(5)
            username = obj.username + "_" + str(unique_id)
            user = User.objects.create_user(username=username,
                                            email=obj.email,
                                            password=obj.password)

            user.is_staff = True
            user.save()
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            user.save()
            obj.user = user
            obj.username = username

        super(TeacherAdmin, self).save_model(request, obj, form, change)

        import face_recognition
        np.savetxt("media/encoding/" + str(obj.id)+"_1" + '.txt',
                   face_recognition.face_encodings(face_recognition.load_image_file(obj.face_image1.path))[0] )

        if obj.face_image2:
            np.savetxt("media/encoding/" + str(obj.id) + "_2" + '.txt',
                       face_recognition.face_encodings(face_recognition.load_image_file(obj.face_image2.path))[0])

        if obj.face_image3:
            np.savetxt("media/encoding/" + str(obj.id) + "_3" + '.txt',
                       face_recognition.face_encodings(
                           face_recognition.load_image_file(obj.face_image3.path))[0])




class AttendanceSettingResource(resources.ModelResource):
    class Meta:
        model = AttendanceSetting
        fields = ("id","college_time","attendance_time","no_early_marks","no_late_marks","half_day_time","checkout_time")
        export_order = ('id',"college_time","attendance_time","no_early_marks","no_late_marks","half_day_time","checkout_time")



class AttendanceSettingAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AttendanceSettingResource
    search_fields = ("college_time","attendance_time","no_early_marks","no_late_marks","half_day_time","checkout_time")
    list_display = ("college_time","college_time","no_early_marks","no_late_marks","half_day_time","checkout_time")



class AttendanceResource(resources.ModelResource):
    class Meta:
        model = Attendance
        fields = ("id","date","teacher_name","attendance_marked","late_mark","half_day")
        export_order = ('id',"date","teacher_name","attendance_marked","late_mark","half_day")


class AttendanceAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ("date","teacher","attendance_marked","late_mark","half_day")
    list_display = ("date","teacher_name","attendance_marked","late_mark","half_day")
    readonly_fields = ("teacher_name","start",)
    resources_class__ = AttendanceResource

    def get_fields(self, request, obj=None):
        return ("teacher","image_path","start")

    def get_queryset(self, request):
        qs = super(AttendanceAdmin, self).get_queryset(request)
        if request.user.username == "admin":
            return qs
        else:
            teacher_obj = Teacher.objects.get(username=request.user.username)
            return qs.filter(teacher=teacher_obj.name)


    def teacher_name(self,obj):
        return format_html("<b>"+obj.teacher+"</b>")

    def start(self,obj):
        if obj.id:
            return format_html("<p>Your Attendance was marked successfully</p><br/><img src='/"+obj.image_path+"' style='width:200px;height:200px;' />")
        else:
            return format_html("<button onclick='getAttendance();return false;'>Mark Your Attendance</button><button id='submit_btn' style='display:none;'></button>")

    class Media:
        js = ['/media/JS/attendance.js']

    def save_model(self, request, obj, form, change):

        if request.user.username == "admin":
            return
        teacher_obj = Teacher.objects.get(username=request.user.username)
        print(request.POST)
        if teacher_obj.name != request.POST["teacher"]:
            return

        super(AttendanceAdmin, self).save_model(request, obj, form, change)
        print("==========================================>")
        time_data = str(timezone.localtime(timezone.now()).time()).split(":")
        print(time_data)
        time_int = int(time_data[0] + time_data[1])
        print(time_int)
        ats = AttendanceSetting.objects.all()[0]
        obj.attendance_marked = True
        obj.save()

        half_day_time = str(ats.half_day_time).split(":")
        if time_int > int(half_day_time[0] + half_day_time[1]):
            obj.half_day = True
            obj.save()
            return

        attendance_time = str(ats.attendance_time).split(":")
        if time_int > int(attendance_time[0] + attendance_time[1]):
            obj.late_mark = True
            obj.save()
            return




class CheckoutResource(resources.ModelResource):
    class Meta:
        model = Checkout
        fields = ("id","date", "teacher", "attendance_marked", "early_mark", "half_day")
        export_order = ('id',"date", "teacher", "attendance_marked", "early_mark", "half_day")


class CheckoutAdmin(ExportMixin, admin.ModelAdmin):
    search_fields = ("date", "teacher", "attendance_marked", "early_mark", "half_day")
    list_display = ("date", "teacher_name", "attendance_marked", "early_mark", "half_day")
    readonly_fields = ("teacher_name", "start",)
    resources_class = CheckoutResource


    def get_fields(self, request, obj=None):
        return ("teacher", "image_path", "start")

    def get_queryset(self, request):
        qs = super(CheckoutAdmin, self).get_queryset(request)
        if request.user.username == "admin":
            return qs
        else:
            teacher_obj = Teacher.objects.get(username=request.user.username)
            return qs.filter(teacher=teacher_obj.name)

    def teacher_name(self, obj):
        return format_html("<b>" + obj.teacher + "</b>")

    def start(self, obj):
        if obj.id:
            return format_html(
                "<p>Your Checkout was marked successfully</p><br/><img src='/" + obj.image_path + "' style='width:200px;height:200px;' />")
        else:
            return format_html(
                "<button onclick='getAttendance();return false;'>Mark Your Checkout</button><button id='submit_btn' style='display:none;'></button>")

    class Media:
        js = ['/media/JS/attendance.js']

    def save_model(self, request, obj, form, change):
        super(CheckoutAdmin, self).save_model(request, obj, form, change)
        print("==========================================>")
        time_data = str(timezone.localtime(timezone.now()).time()).split(":")
        print(time_data)
        time_int = int(time_data[0] + time_data[1])
        print(time_int)
        ats = AttendanceSetting.objects.all()[0]
        obj.attendance_marked = True
        obj.save()

        attendance_time = str(ats.half_day_time).split(":")
        if time_int < int(attendance_time[0] + attendance_time[1]):
            obj.early_mark = True
            obj.save()
            return

        half_day_time = str(ats.checkout_time).split(":")
        if time_int < int(half_day_time[0] + half_day_time[1]):
            obj.half_day = True
            obj.save()
            return



admin.site.site_header = 'College ATTENDANCE SYSTEM USING FACE DETECTION'

admin.site.register(Teacher,TeacherAdmin)
admin.site.register(AttendanceSetting,AttendanceSettingAdmin)
admin.site.register(Attendance,AttendanceAdmin)
admin.site.register(Checkout,CheckoutAdmin)

