from django import forms
from Users.models import Comment
from .models import *

class Addcommentinproject(forms.ModelForm):  
   class Meta:
      model = Comment
      exclude= ['user_id','project_id']
      widgets = {
            'comment': forms.TextInput(attrs={'cols': 80, 'rows': 20}),
      }
 

class Addproject(forms.ModelForm):  
  
   start_time = forms.DateField(label="Start Date",required=True,widget=forms.DateInput(attrs={"placeholder":"YYYY-MM-DD"}))
   end_time = forms.DateField(label="End Date",required=True,widget=forms.DateInput(attrs={"placeholder":"YYYY-MM-DD"}))

   class Meta:
      model = Projects
      fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time']



class Addimage(forms.ModelForm):
   class Meta:
      model = Images
      exclude= ['project_id']      

class addDonation(forms.ModelForm):
      class Meta: 
         model = Donation
         exclude= ['user_id','project_id']

class addRating(forms.ModelForm):
      class Meta: 
         model = Rating
         exclude= ['project_id','user_id']        

     