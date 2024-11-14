from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Create your models here.

class LeaveApplication(models.Model):
    LEAVE_TYPES = [
        ('Sick Leave', 'Sick Leave'),
        ('Casual Leave', 'Casual Leave'),
        ('Annual Leave', 'Annual Leave'),
        ('Maternity Leave', 'Maternity Leave'),
        ('Paternity Leave', 'Paternity Leave'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    date_of_application = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(max_length=140)
    department = models.CharField(max_length=75)
    total_leave_days = models.PositiveIntegerField()
    officer_handing_over_duty_to = models.TextField(max_length=100)
    supervisor_name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reviewed_leaves')
    review_date = models.DateTimeField(null=True, blank=True)
    review_comment = models.TextField(blank=True)
    
    def save(self, *args, **kwargs):

        # Automatically calculate total leave days (excluding weekends)
        if self.start_date and self.end_date:
            total_days = 0
            current_date = self.start_date
            while current_date <= self.end_date:
                if current_date.weekday() not in (5, 6):  # 5: Saturday, 6: Sunday
                    total_days += 1
                current_date += timedelta(days=1)
            self.total_leave_days = total_days
            super().save(*args, **kwargs)
    

    def __str__(self):
        return f"{self.user}   {self.leave_type}"
    

