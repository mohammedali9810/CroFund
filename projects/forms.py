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
        title = cleaned_data.get("title")
        details = cleaned_data.get("details")
        category = cleaned_data.get("category")
        total_target = cleaned_data.get("total_target")

        if not start_date:
            self.add_error('start_time', 'Start date is required.')

        if not end_date:
            self.add_error('end_time', 'End date is required.')

        if not title:
            self.add_error('title', 'Title is required.')

        if not details:
            self.add_error('details', 'Details are required.')

        if not category:
            self.add_error('category', 'Category is required.')

        if not total_target:
            self.add_error('total_target', 'Total target is required.')

        if start_date and end_date and start_date >= end_date:
            self.add_error('start_time', 'Start date must be earlier than the end date.')

        return cleaned_data

class Addimage(forms.ModelForm):
    class Meta:
        model = Images
        exclude = ['project_id']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('The image field is required.')
        return image


class addDonation(forms.ModelForm):
      class Meta: 
         model = Donation
         exclude= ['user_id','project_id']

class addRating(forms.ModelForm):
      class Meta: 
         model = Rating
         exclude= ['project_id','user_id']        

     