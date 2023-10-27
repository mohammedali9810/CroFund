from rest_framework import serializers

from projects.models import *


class Addcommentinproject(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['user_id', 'project_id']
    #   widgets = {
    #         'comment': forms.TextInput(attrs={'cols': 80, 'rows': 20}),
    #   }


class Addproject(serializers.ModelSerializer):
    #    start_time = forms.DateField(label="Start Date",required=True,widget=forms.DateInput(attrs={"placeholder":"YYYY-MM-DD"}))
    #    end_time = forms.DateField(label="End Date",required=True,widget=forms.DateInput(attrs={"placeholder":"YYYY-MM-DD"}))

    class Meta:
        model = Projects
        fields = ['title', 'details', 'category', 'total_target', 'start_time', 'end_time']


class Addimage(serializers.ModelSerializer):
    class Meta:
        model = Images
        exclude = ['project_id']


class addDonation(serializers.ModelSerializer):
    class Meta:
        model = Donation
        exclude = ['user_id', 'project_id']


class addRating(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['project_id', 'user_id']
