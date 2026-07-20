from django import forms
from .models import Complaint, Zone, Ward, Area, Officer, ComplaintStatus
from django.core.exceptions import ValidationError

class ComplaintForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="Upload Image", widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}))
    declaration = forms.BooleanField(required=True, label="Declaration Checkbox")
    captcha = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Captcha Code'}))

    class Meta:
        model = Complaint
        fields = [
            'mobile_number', 'citizen_name', 'gender', 'street_address', 'pincode', 'email',
            'zone', 'ward', 'area', 'street', 'latitude', 'longitude',
            'category', 'complaint_type', 'social_media_link', 'description', 'video_upload'
        ]
        widgets = {
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'citizen_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'street_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter street address'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '639001'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'zone': forms.Select(attrs={'class': 'form-select'}),
            'ward': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street name/landmark'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'complaint_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Streetlight not working'}),
            'social_media_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/post/...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your complaint in detail'}),
            'video_upload': forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}),
        }

    def clean_video_upload(self):
        video = self.cleaned_data.get('video_upload')
        if video:
            if video.size > 5 * 1024 * 1024: # 5MB limit
                raise ValidationError("Video size cannot exceed 5MB.")
        return video

    def clean(self):
        cleaned_data = super().clean()
        # Custom file size validations for image too
        img = cleaned_data.get('image')
        if img and img.size > 5 * 1024 * 1024:
            self.add_error('image', "Image size cannot exceed 5MB.")
        return cleaned_data

class AdminComplaintUpdateForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status', 'assigned_officer', 'resolution_remarks', 'resolution_image']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'assigned_officer': forms.Select(attrs={'class': 'form-select'}),
            'resolution_remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter officer resolution remarks...'}),
            'resolution_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }
