from copy import deepcopy
from django.http import HttpRequest
from django.shortcuts import render
from .models import User #,Data_Storage
from rest_framework import generics, viewsets
from .serializers import * #This is fine as all defined classes are used here
from rest_framework.permissions import  AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required
from typing import List
from django.db.models import Q


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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Admin can view all devices
            queryset = Device.objects.all()
        else:
            # Regular user can view only their own devices
            queryset = Device.objects.filter(user_id=user.id) #FIXME rename from id_id
        return queryset



# # Should
# def get_chain(device: Device) -> List[Device]:
#     returnValue = [device]
#     chain = Device_Chain.objects.filter(current_device = device)[0] #Assumed that chains have only 2 ends
#     next_chain_as_list = Device_Chain.objects.filter(current_device = chain.next_device)#purposely not indexing
#     while(next_chain_as_list ){
#         #if not empty
#         returnValue.append(next_chain_as_list[0].next_device)
#         next_chain_as_list = Device_Chain.objects.filter(current_device = returnValue[-1])#purposely not indexing
#     }
#     returnValue.append(next_chain_as_list[0].next_device)
#     return returnValue


class Device_ChainViewSet(viewsets.ModelViewSet):
    queryset = Device_Chain.objects.all()
    serializer_class = Device_ChainSerializer

#FIXME bring back
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser:
    #         # Admin can view all devices
    #         queryset = Device_Chain.objects.filter
    #     else:
    #         # Regular user can view only their own devices
    #         devices = Device.objects.filter(user_id = user.id)
    #         queryset = Device_Chain.objects.filter(Q( current_device__in = devices| next_device__in = devices))
    #     return queryset


class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class LogViewSet(viewsets.ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Admin can view all devices
            queryset = Log.objects.all()
        else:
            # Regular user can view only their own Logs
            queryset = Log.objects.filter(user_id=user.id) #FIXME rename from id_id
        return queryset


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer
    permission_classes = [IsAdminUser]


class Run_HistoryViewSet(viewsets.ModelViewSet):
    queryset = Run_History.objects.all()
    serializer_class = Run_HistorySerializer
    permission_classes = [IsAdminUser]


# def external_data_database_view(request):
#     # Query data from the other database
#     data = OtherDatabaseModel.objects.using('other_db').all()

#     return render(request, 'template.html', {'data': data})