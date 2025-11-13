from django.db import models
from django.urls import reverse

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    course = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos/')
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('student_list')


class SupportDocument(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='support_docs/')
    
    def __str__(self):
        return f"Document for {self.student.name}"
