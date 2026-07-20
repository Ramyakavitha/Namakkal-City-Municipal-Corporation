from django.contrib import admin
from .models import Zone, Ward, Area, Officer, ComplaintStatus, Complaint, ComplaintImage, ComplaintTimeline, OTP

class ComplaintImageInline(admin.TabularInline):
    model = ComplaintImage
    extra = 1

class ComplaintTimelineInline(admin.TabularInline):
    model = ComplaintTimeline
    extra = 1

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('complaint_number', 'citizen_name', 'mobile_number', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'zone', 'ward')
    search_fields = ('complaint_number', 'citizen_name', 'mobile_number')
    inlines = [ComplaintImageInline, ComplaintTimelineInline]

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'zone')
    list_filter = ('zone',)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward')
    list_filter = ('ward__zone', 'ward')

@admin.register(Officer)
class OfficerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'department', 'zone')
    list_filter = ('department', 'zone')

@admin.register(ComplaintStatus)
class ComplaintStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('mobile_number', 'otp_code', 'created_at', 'is_verified')
    list_filter = ('is_verified',)
