from django.db import models
from django.contrib.auth.models import User #django has inbuild function amin which has users,auth ... see in documentation
# Create your models here.
class topic(models.Model):
    name =models.CharField(max_length=200)
    def __str__(self) -> str:
        return self.name

class room(models.Model): #python calss to model
    host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    top=models.ForeignKey(topic,on_delete=models.SET_NULL,null=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True,blank=True) #null=True which can make it blank .if instance not create.blank if save form it wiil be blank
    #participants=
    update= models.DateTimeField(auto_now=True) #take freq timestamp
    create=models.DateTimeField(auto_now_add=True)#first create timestamp

    class Meta:
        ordering=['-update','-create'] #descending - so newest first
    def __str__(self): #create Rome string
        return self.name
class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room=models.ForeignKey(room,on_delete=models.CASCADE) #models.SET_NULL-->mesg not del if room del. models.cascade msg del
    body=models.TextField()
    update=models.DateTimeField(auto_now=True) 
    create=models.DateTimeField(auto_now_add=True)

    def __str__(self): #create Rome string
        return self.body[0:50] #we want to only 50 char 