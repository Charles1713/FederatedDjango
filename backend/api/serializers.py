# Maps code to database instance vice versa
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Device, Device_Chain, Model, Model_History, Run, Run_History, Log
#Data_Storage ?

# class {Table}Serializer(inherit)
# Meta class
# model = {Table} # User was preestablished
# fields to serialize from model so global()[Model].{field element}
# extra_kwargs # ????

#FIXME figure out which should be read or write fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username","password"]
        extra_kwargs = {"password": {"write_only": True}} # We dont want the unauthorized user to see password 

    #FIXME decide when to override create method for others
    def create(self, validated_data):
        print(validated_data)
        return User.objects.create_user(**validated_data)

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ["can_be_used", "model_output_dest", "user_id", "ip", "device_name", "data_server", "data_path"
                  , "edge_working_directory", "edge_ram_gb", "edge_storage_gb"]
        #The user shouldn't be able to change these except device_name
        extra_kwargs = {"user_id": {"read_only": True}, 
                        "ip": {"read_only": True}, 
                        "can_be_used": {"read_only": True}, 
                        "model_output_dest": {"read_only": True}, 
                        "user_id": {"read_only": True}, 
                        "ip": {"read_only": True}, 
                        "device_name": {"read_only": True}, 
                        "data_server": {"read_only": True}, 
                        "data_path": {"read_only": True},
                        "edge_working_directory": {"read_only": True}, 
                        "edge_ram_gb": {"read_only": True}, 
                        "edge_storage_gb": {"read_only": True}}

class Device_ChainSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["created_at", "current_model", "next_model"]
        extra_kwargs = {
            "current_device":{"read_only": True},
            "next_device":{"read_only": True},
        }

class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["model_name", "model_path"] #might remove model path, user should not be able to change that or this is just for admin level


class LogSerializer(serializers.ModelSerializer):
    class Meta: #FIXME what to do about file uploads
        fields = ["device_end", "error_file", "device_log_file", "model_log_file", "initial_model_id", "run", "model_upload"]
        extra_kwargs = {
            "device_end": {"read_only": True}, #Should always be the device that calls this so search by ip?
            }

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["start_time","end_time"] #Update at end of RUN FIXME

class Run_HistorySerializer(serializers.ModelSerializer): #Might remove this serializer, should be backend only 
    class Meta:
        fields = ["run_number","device_id"]

        

