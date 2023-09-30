from django.forms import ModelForm #prebuild form data  #used for create and delete items in table
from .models import room
class RoomForm(ModelForm):
    class Meta:
        model = room
        fields='__all__' #take all variable in room class
        exclude=['host']