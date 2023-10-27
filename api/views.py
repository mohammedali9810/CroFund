from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data

from .serializers import *
from .views import *
from projects.models import *
from Users.models import *
from django.db.models import Avg,Sum,Count
# Create your views here.


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


'''
Profile User CRUD
'''
# The Queryset required => end point to allow operations on the model

# user profile
"""
- view his own:
    * profile   [/]
    * projects  [/]
    * donations [/]
    * edit all except email
    * delete after confirm
"""


# Helper function to combine all the profile data => return data

def get_profile_data(current_user):
    # only one profile per user => get
    current_user_profile = Profile.objects.get(user=current_user)
    # many projects => filter
    current_user_projects = Projects.objects.filter(user_id=current_user)
    # many donations => filter
    current_user_donations = Donation.objects.filter(user_id=current_user)

    # overall user donation => Just in one line ^^
    d_sum = sum(
        map(
            lambda x: x['amount_of_money'],
            current_user_donations.values('amount_of_money')
        )
    )

    # Setting up serializers
    profile_serializer = UserProfileSerializer()
    project_serializer = ProjectSer(many=True)
    donation_serializer = DonationSerializer(many=True)
    data = profile_serializer.to_representation(current_user_profile)
    data['projects'] = project_serializer.to_representation(current_user_projects)
    data['total-donations'] = d_sum
    data['donations'] = donation_serializer.to_representation(current_user_donations)
    return data


"""
<QueryDict: {
    'csrfmiddlewaretoken': ['___'], 
    'name': ['___'],
    'password': ['___'],
    'phone': ['___'], 
    'birth': ['___'],
    'social_media': ['___'],
    'country': ['___'],
    'image': ['___']
}>

# Profile model:
  user
  phone
  birth
  social_media
  country
  image

"""

# TODO: create an instance of a new user and an instance of a profile based on that user

class UserProfileViewSet(viewsets.ViewSet):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

    

    # CREATE
    # first create a user then assgin a profile to him
    def create(self, request):
        """
        creating a new user/profile is available for all 
        """
        user_serializer = UserSerializer(data=request.data)
        user_profile_serializer = UserProfileSerializer(data=request.data)

        #create a new user
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            print(user_serializer.errors)
        


        return Response(status=status.HTTP_400_BAD_REQUEST)

    """
    override the retrieve method to only get his profile 
    """
    # RETRIEVE
    def retrieve(self, request, pk=None):
        current_user = request.user
        """
        Accessing other profiles is not authorized
        """

        if int(pk) != current_user.id:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        data = get_profile_data(current_user)
        return Response(data)

    # UPDATE
    def update(self, request, pk=None):
        current_user = request.user
        """
        Update other profiles is not authorized
        """
        if int(pk) != current_user.id:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

    # DELETE
    def destroy(self, request, pk=None):
        current_user = request.user
        """
        Accessing other profiles is not authorized
        """
        if int(pk) != current_user.id:
            return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        self.perform_destroy(current_user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


# Create
# Retrieve
"""
This is another way to retrieve user profile
"""


@api_view(['GET'])
def user_profile(request):
    current_user = request.user

    data = get_profile_data(current_user)
    return Response(data)


# Update
@api_view(['PUT'])
def profile_edit(request):
    current_user = request.user
    current_user_profile = Profile.objects.get(user=current_user)
    serializer = UserProfileSerializer(instance=current_user_profile, data=request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def profile_delete(request):
    current_user = request.user
    current_user_profile = Profile.objects.get(user=current_user)
    current_user_profile.delete()


@api_view(['GET'])
def api_list(request):
    api_urls = {
        'User Profile': {
            'View': '/myprofile'
        },
        'Projects': {
            'List': '/project/list/',
            'Detail View': '/project/list/<str:pk>/',
            'Create': '/project/create/',
            'Update': '/project/update/<str:pk>/',
            'Delete': '/project/delete/<str:pk>/',
        }

    }
    return Response(api_urls)


@api_view(['GET'])
def projectsList(request):
    projects = Projects.objects.all()
    Project = ProjectSer(projects, many=True)

    api_return = {
       'Project Details': []
    }

    for proj in Project.data:

        fullProjectDetails = {
            'Project info': [],
            'Project Donations': [],
            'Project Images': [],
            'Project Comments': [],
            'Project Rating': []
        }
        DonationSum=0
        RatingSum=0
        count=0
        print(proj['id'])

        donations = Donation.objects.filter(project_id=proj['id'])
        donationsSer = DonationSerializer(donations, many=True)
        for donate in donationsSer.data:
            DonationSum+=donate['amount_of_money']

        images = Images.objects.filter(project_id=proj['id'])
        imagesSer = ImageSer(images, many=True)

        comments = Comment.objects.filter(project_id=proj['id'])
        commentSer = CommentSerializer(comments, many=True)

        rates = Rating.objects.filter(project_id=proj['id'])

        ratingSer = RatingSer(rates, many=True)
        for rate in ratingSer.data:
            RatingSum += rate['rating']
            count+=1


        fullProjectDetails['Project info'].append(proj)
        fullProjectDetails['Project Donations'].append(DonationSum)
        if not count:
            fullProjectDetails['Project Rating'].append(RatingSum)
        else:
            fullProjectDetails['Project Rating'].append(RatingSum/count)
        fullProjectDetails['Project Images'].append(imagesSer.data)
        fullProjectDetails['Project Comments'].append(commentSer.data)

        api_return['Project Details'].append(fullProjectDetails)

    return Response(api_return)

@api_view(['GET'])
def projectList(request, pk):
    projects = Projects.objects.get(id=pk)
    Project = ProjectSer(projects, many=False)

    api_return = {
       'Project Details': []
    }



    fullProjectDetails = {
        'Project info': [],
        'Project Donations': [],
        'Project Images': [],
        'Project Comments': [],
        'Project Rating': []
    }
    DonationSum=0
    RatingSum=0
    count=0
    donations = Donation.objects.filter(project_id=pk)
    donationsSer = DonationSerializer(donations, many=True)
    for donate in donationsSer.data:
        DonationSum+=donate['amount_of_money']

    images = Images.objects.filter(project_id=pk)
    imagesSer = ImageSer(images, many=True)

    comments = Comment.objects.filter(project_id=pk)
    commentSer = CommentSerializer(comments, many=True)

    rates = Rating.objects.filter(project_id=pk)

    ratingSer = RatingSer(rates, many=True)
    for rate in ratingSer.data:
        RatingSum += rate['rating']
        count+=1


    fullProjectDetails['Project info'].append(Project.data)
    fullProjectDetails['Project Donations'].append(DonationSum)
    if not count:
        fullProjectDetails['Project Rating'].append(RatingSum)
    else:
        fullProjectDetails['Project Rating'].append(RatingSum/count)
    fullProjectDetails['Project Images'].append(imagesSer.data)
    fullProjectDetails['Project Comments'].append(commentSer.data)

    api_return['Project Details'].append(fullProjectDetails)

    return Response(api_return)


@api_view(['POST'])
def projectCreate(request):

    # api_return = {
    #     'Project Details': []
    # }

    # fullProjectDetails = {
    #     'Project info': [],
    #     'Project Donations': [],
    #     'Project Images': [],
    #     'Project Comments': [],
    #     'Project Rating': []
    # }

    Project = ProjectSer(data=request.data)
    if Project.is_valid():
        Project.save()
    # donationsSer = DonationSerializer(data=request.data['Project Details'][0]['Project Donations'])
    # if donationsSer.is_valid():
    #     donationsSer.save()
    # imagesSer = ImageSer(data=request.data['Project Details'][0]['Project Images'])
    # if imagesSer.is_valid():
    #     imagesSer.save()
    # commentSer = CommentSerializer(data=request.data['Project Details'][0]['Project Comments'])
    # if commentSer.is_valid():
    #     commentSer.save()
    # ratingSer = RatingSer(data=request.data['Project Details'][0][ 'Project Rating'])
    # if ratingSer.is_valid():
    #     ratingSer.save()
    # fullProjectDetails['Project info'].append(Project.data)
    # fullProjectDetails['Project Rating'].append(donationsSer.data)
    # fullProjectDetails['Project Donations'].append(ratingSer.data)
    # fullProjectDetails['Project Images'].append(imagesSer.data)
    # fullProjectDetails['Project Comments'].append(commentSer.data)
    # api_return['Project Details'].append(fullProjectDetails)

    return Response(Project.data)
