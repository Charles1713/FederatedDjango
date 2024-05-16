from django.contrib import admin
from django.db import router
from django.urls import path, include
from flask import views
from api.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

#FIXME might prune what specific routes do rather than let everything happen? Depends on Query Set and nonrepudiation to remove patch
router = routers.DefaultRouter()
router.register('device',DeviceViewSet)
router.register('device_chain',Device_ChainViewSet)
router.register('model',ModelViewSet)
router.register('log',LogViewSet)
router.register('run',RunViewSet)
router.register('run_history',Run_HistoryViewSet)

urlpatterns = [
    path("",include(router.urls)),
]