from django.db import models
from django.contrib.auth.models import User
from zmq import device

# Create your models here.
#FIXME Create model docs with eraser.io
#FIXME Use video for jwt settings
#FIXME Use databases that store info
#FIXME User might have to store credentials so that Refresh tokens dont expire when tasks take too long
#FIXME add dependencies
#FIXME frontend will be used for managing software, api calls arent really frontend when done by sw

#FIXME #fixme fill me in
# class Data_Storage(models.Model):
#     # Define fields as needed
#     field1 = models.CharField(max_length=100)
#     field2 = models.IntegerField()

#     class Meta:
#         # Specify the database alias
#         db_table = 'table_name_in_other_db'
#         app_label = 'your_app_name'
#         managed = False  # Important to prevent Django from managing this table
#         db_alias = 'other_db'


class Device(models.Model):
    
    validation_on_edge = models.BooleanField()
    # model_history is already stored
    can_be_used = models.BooleanField()

    #outputted to other edge if not Blank
    model_output_dest = models.ForeignKey("self", blank=True, on_delete=models.PROTECT) #No cascade on delete, just raises and error, blank = True lets us not give a value which means sends to server
    user = models.ForeignKey(User, on_delete=models.CASCADE) #If a user is removed it should be deleted
    ip = models.GenericIPAddressField()
    device_name = models.TextField(max_length=30, default="Unknown Device")
    #data_server = models.ForeignKey(Data_Storage, blank=True, on_delete=models.PROTECT) #FIXME ADDBACK
    data_path = models.FilePathField() #Used if data_server_ip or data_server blank, should be path on edge to get data from
    edge_working_directory = models.FilePathField() #the directory to create the folder in, use .env to get folder name and append
    #Most likely wont do key_files FIXME remove comment if necessary
    # If ssh is allowed, have the frontend be able to submit a username, ip, password then ssh and add it. 
    # Might have to give directions on how to enable start up or, delete and reinstall device or manually start up client software on IOT
    # Poll computers on output if chaining?
    edge_ram_gb = models.FloatField(blank=True)
    edge_storage_gb = models.FloatField(blank=True)
    # As soon as device is registered a device log should be sent to update 

    def __str__(self) -> str:
        return self.device_name
    
#FIXME make unchain method that gives a full path start to end using most recent by default or before run end_time
#FIXME when changing the chain do another post
class Device_Chain(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    current_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="current_device", verbose_name="Current Device")
    next_device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="next_device", verbose_name="Next Device")

    def __str__(self) -> str:
        return f"current device = {self.current_device}: next device = {self.next_device}"
    

class Model(models.Model): #Aggregated Models only
    # Should we store metrics here FIXME 
    model_name = models.TextField(max_length=20, default="Unknown Model") #FIXME might not be needed
    model_path = models.FileField("/aggregated_models/") #Should not be null or blank, this is stored on the server
    
    def __str__(self) -> str:
        return self.model_name

class Model_History(models.Model):
    model_id = models.ForeignKey(Model, on_delete=models.CASCADE) # No info if model already removed
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE) #delete if device removed

    def __str__(self) -> str:
        #FIXME might be slow
        return Device.objects.get(self.device_id).device_name + "uses model: " + Model.objects.get(self.model_id).model_name

class Run(models.Model):
    # The time is used such that the we can use the right chain
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True) #Update at end of RUN FIXME

    def __str__(self) -> str:
        return f"{self.start_time} to {self.end_time}"

class Run_History(models.Model):
    run_number = models.ForeignKey(Run, on_delete=models.CASCADE)
    device_id = models.ForeignKey(Device, on_delete=models.CASCADE)

class Log(models.Model):
    device_end = models.ForeignKey(Device, on_delete=models.CASCADE) #Device that sends to server info #FIXME
    error_file = models.FileField("/error_log_files/", blank=True) #FIXME file storing might need to change mediaurl or media_ROOT models.FileField("\path")
    device_log_file = models.FileField("/device_log_files/") 
    model_log_file = models.FileField("/model_log_files/") #FIXME
    initial_model_id = models.ForeignKey(Model, on_delete=models.PROTECT)
    run = models.ForeignKey(Run, on_delete=models.CASCADE)
    model_upload = models.FileField("/client_model_after_training_before_agg/") #FIXME

    def __str__(self) -> str:
        #FIXME might be slow
        return f"RUN: {self.run} {Device.objects.get(self.device_end).device_name} used model: {Model.objects.get(self.initial_model_id).model_name}"

# If we need config file add to Log class
# class Config(models.Model):
#     file_name = models.TextField(max_length=100) #RUN__DEVICE_ID__DEVICE_NAME__
