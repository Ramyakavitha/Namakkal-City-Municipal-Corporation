import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_sms(mobile_number, otp_code):
    """
    Simulates sending OTP to mobile number via SMS
    """
    print(f"--- SMS SIMULATION ---")
    print(f"To: {mobile_number}")
    print(f"Message: Your OTP for Namakkal City Municipal Corporation PGR is {otp_code}. Valid for 10 minutes.")
    print(f"----------------------")
    return True

def send_complaint_email_notification(complaint):
    """
    Simulates sending an email notification to the citizen
    """
    if not complaint.email:
        return False
        
    subject = f"Complaint Registered - {complaint.complaint_number} - Namakkal Corporation"
    message = f"""Dear {complaint.citizen_name},

Thank you for contacting Namakkal City Municipal Corporation. Your grievance has been registered successfully.

Complaint Details:
- Complaint Number: {complaint.complaint_number}
- Category: {complaint.get_category_display()}
- Sub-category: {complaint.complaint_type}
- Status: {complaint.status.name}

You can check the real-time status of your complaint at our portal using your Complaint Number or Registered Mobile Number.

Regards,
Public Grievance Redressal Cell
Namakkal City Municipal Corporation
    """
    
    # We will wrap in try/except so that it does not crash if SMTP is not configured
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL or 'noreply@namakkalcorporation.org',
            [complaint.email],
            fail_silently=True,
        )
        print(f"Email sent successfully to {complaint.email} for {complaint.complaint_number}")
    except Exception as e:
        print(f"Email simulation warning: {e}")
    return True
