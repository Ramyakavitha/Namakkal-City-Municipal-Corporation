from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class Zone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Ward(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE, related_name='wards')
    name = models.CharField(max_length=100)
    number = models.IntegerField()

    class Meta:
        unique_together = ('zone', 'number')

    def __str__(self):
        return f"Ward {self.number} ({self.name})"

class Area(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='areas')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Officer(models.Model):
    DEPARTMENTS = [
        ('Sanitation', 'Sanitation & Health'),
        ('WaterSupply', 'Water Supply'),
        ('StreetLights', 'Street Lights'),
        ('Roads', 'Roads & Works'),
        ('Revenue', 'Revenue & Tax'),
        ('General', 'General Administration'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.get_department_display()}"

class ComplaintStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    CATEGORIES = [
        ('Sanitation', 'Sanitation & Garbage'),
        ('Water', 'Water Supply & Sewage'),
        ('Streetlight', 'Streetlight Maintenance'),
        ('Roads', 'Roads & Potholes'),
        ('Encroachment', 'Encroachments & Building Control'),
        ('Others', 'Others'),
    ]
    
    # Citizen Details
    complaint_number = models.CharField(max_length=30, unique=True, editable=False)
    mobile_number = models.CharField(max_length=15)
    citizen_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    street_address = models.TextField()
    pincode = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)

    # Complaint Location
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    street = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)

    # Complaint Details
    category = models.CharField(max_length=50, choices=CATEGORIES)
    complaint_type = models.CharField(max_length=100)
    social_media_link = models.URLField(blank=True, null=True)
    description = models.TextField()
    video_upload = models.FileField(upload_to='videos/', blank=True, null=True)
    
    # Status and Assignment
    status = models.ForeignKey(ComplaintStatus, on_delete=models.PROTECT, default=1)
    assigned_officer = models.ForeignKey(Officer, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Resolution Details
    resolution_remarks = models.TextField(blank=True, null=True)
    resolution_image = models.ImageField(upload_to='resolutions/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.complaint_number:
            year = datetime.datetime.now().year
            last = Complaint.objects.filter(complaint_number__startswith=f"NMCMC-{year}").order_by('-id').first()
            if last:
                try:
                    # last.complaint_number looks like "NMCMC-202600001"
                    last_seq_str = last.complaint_number.split('-')[1][4:]
                    num = int(last_seq_str) + 1
                except Exception:
                    num = Complaint.objects.filter(created_at__year=year).count() + 1
            else:
                num = 1
            self.complaint_number = f"NMCMC-{year}{num:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint_number} - {self.citizen_name}"

class ComplaintImage(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='complaints/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ComplaintTimeline(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='timeline')
    status = models.ForeignKey(ComplaintStatus, on_delete=models.PROTECT)
    changed_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['changed_at']

class OTP(models.Model):
    mobile_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        now = timezone.now()
        diff = now - self.created_at
        return diff.total_seconds() > 600

    def __str__(self):
        return f"{self.mobile_number} - {self.otp_code}"
