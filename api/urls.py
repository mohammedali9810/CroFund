from django.urls import include, path
from rest_framework import routers

from . import views

# register your view set
# from .routers import *
"""> Official Doc:
The method handlers for a ViewSet are only bound to the corresponding actions at the point of finalizing the view, using the .as_view() method.

Typically, rather than explicitly registering the views in a viewset in the urlconf, you'll register the viewset with a router class, that automatically determines the urlconf for you.
"""
router = routers.DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'users', views.UserViewSet)
"""
The router above would generate the following URL patterns:

    - URL pattern: ^users/$ Name: 'user-list'
    - URL pattern: ^users/{pk}/$ Name: 'user-detail'
"""

# register your view set

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('view-all/', views.api_list, name="api overview"),
    path('project/list/', views.projectsList, name="projects list"),
    path('project/list/<str:pk>/', views.projectList, name="project list"),
    path('project/create/', views.projectCreate, name="Project-create"),

    path('user/<int:pk>', views.user_detail),
    path('myprofile/', views.user_profile),
    path('editprofile/', views.profile_edit)
]
