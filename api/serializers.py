from django.contrib.auth.models import User
from rest_framework import serializers
from .serializers import *
from Users.models import *
from projects.models import *
from .serializers import *

# import from models in the same folder "app"

# serializer for user profile details

"""
- view his own:
    * profile
    * projects
    * donations
    * edit all except email
    * delete after confirm
"""


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reportno
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email", read_only=True)

    password = serializers.CharField(source="user.password", style={'input_type': 'password'}, required=True)

    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = '__all__'


# Projects

class CategoriesSer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category', 'id']


class TagsSer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['tags', 'id']


class ProjectSer(serializers.ModelSerializer):
    category = CategoriesSer(many=False)
    tags = TagsSer(many=True)

    # comments = CommentSer(many=True)

    class Meta:
        model = Projects
        fields = ['id', 'title', 'details', 'total_target', 'start_time', 'end_time', 'category', 'tags']


class ImageSer(serializers.ModelSerializer):
    class Meta:
        model = Images
        exclude = ['project_id']


class RatingSer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
