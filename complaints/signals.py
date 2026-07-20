from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Complaint, ComplaintTimeline

@receiver(pre_save, sender=Complaint)
def track_status_change_before_save(sender, instance, **kwargs):
    if instance.id:
        try:
            previous = Complaint.objects.get(id=instance.id)
            # Store the old status on the instance temporarily
            instance._old_status = previous.status
            instance._old_assigned_officer = previous.assigned_officer
        except Complaint.DoesNotExist:
            instance._old_status = None
            instance._old_assigned_officer = None
    else:
        instance._old_status = None
        instance._old_assigned_officer = None

@receiver(post_save, sender=Complaint)
def log_status_change(sender, instance, created, **kwargs):
    old_status = getattr(instance, '_old_status', None)
    old_officer = getattr(instance, '_old_assigned_officer', None)
    
    # If newly created
    if created:
        ComplaintTimeline.objects.create(
            complaint=instance,
            status=instance.status,
            remarks="Complaint registered successfully."
        )
    # If status changed or officer changed
    else:
        remarks = []
        if old_status != instance.status:
            remarks.append(f"Status updated from '{old_status.name if old_status else 'None'}' to '{instance.status.name}'.")
        if old_officer != instance.assigned_officer:
            remarks.append(f"Assigned officer updated to '{instance.assigned_officer.name if instance.assigned_officer else 'Unassigned'}'.")
        
        if remarks:
            # We can log this transition
            remarks_text = " ".join(remarks)
            if instance.resolution_remarks and instance.status.name in ['Resolved', 'Closed']:
                remarks_text += f" Remarks: {instance.resolution_remarks}"
            ComplaintTimeline.objects.create(
                complaint=instance,
                status=instance.status,
                remarks=remarks_text
            )
