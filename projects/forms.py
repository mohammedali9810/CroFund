from django import forms
from Users.models import Comment, Donation
from django.utils.translation import gettext_lazy as _
from .models import *
from django.core.exceptions import ValidationError


class Addcommentinproject(forms.ModelForm):  
   class Meta:
      model = Comment
      exclude= ['user_id','project_id']
      widgets = {
            'comment': forms.TextInput(attrs={'cols': 80, 'rows': 20}),
      }


class Addproject(forms.ModelForm):
    start_time = forms.DateField(label="Start Date", required=True, widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}))
    end_time = forms.DateField(label="End Date", required=True, widget=forms.DateInput(attrs={"placeholder": "YYYY-MM-DD"}))

    class Meta:
        model = Projects
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_time")
        end_date = cleaned_data.get("end_time")

        if start_date and end_date and start_date >= end_date:
            self.add_error('start_time', 'Start date must be earlier than the end date.')

        return cleaned_data

class Addimage(forms.ModelForm):
    class Meta:
        model = Images
        exclude = ['project_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set 'required' attribute only for the first image field
        self.fields['image'].required = True
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

class addDonation(forms.ModelForm):
      class Meta: 
         model = Donation
         exclude= ['user_id','project_id']

class addRating(forms.ModelForm):
      class Meta: 
         model = Rating
         exclude= ['project_id','user_id']        

     