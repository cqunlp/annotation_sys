from django.urls import path,include

from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('job', views.JobViewSet)
router.register('label', views.LabelViewSet)
router.register('entity', views.EntityViewSet)
router.register('relation', views.RelationViewSet)
router.register('summary', views.SummaryViewSet)
router.register('job_user', views.Job_userViewSet)
router.register('dispatched', views.DispatchedViewSet)

#app_name = 'job'
urlpatterns = [
    path('', include(router.urls)),
    #path('dispatchjob',views.Dispatchjob)
]