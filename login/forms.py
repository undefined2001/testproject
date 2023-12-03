from django import forms
from .models import *

'''
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faculty_initial = models.CharField(max_length=10, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    joined_date = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return self.faculty_initial
'''

class FacultyCreationForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = "__all__"
        exclude = ['joined_date']
        widgets = {
            'user':forms.Select(attrs={'class':'form-control'}),
            'faculty_initial':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'department':forms.TextInput(attrs={'class':'form-control'}),
        }

class FacultyUpdateForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = [
            'first_name'
        ]