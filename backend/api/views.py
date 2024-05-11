from django.shortcuts import render
from .models import User #,Data_Storage
from rest_framework import generics, viewsets
from .serializers import * #This is fine as all defined classes are used here
from rest_framework.permissions import  AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.

#Anyone can create a user for now, #FIXME this should be changed in certain situations
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

#FIXME might change super class
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class Device_ChainViewSet(viewsets.ModelViewSet):
    queryset = Device_Chain.objects.all()
    serializer_class = Device_ChainSerializer


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer


class Run_HistoryViewSet(viewsets.ModelViewSet):
    queryset = Run_History.objects.all()
    serializer_class = Run_HistorySerializer


# def external_data_database_view(request):
#     # Query data from the other database
#     data = OtherDatabaseModel.objects.using('other_db').all()

#     return render(request, 'template.html', {'data': data})