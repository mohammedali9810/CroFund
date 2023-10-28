from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'users', views.UserViewSet)

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
