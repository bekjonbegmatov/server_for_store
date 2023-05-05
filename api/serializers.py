from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *

class InventorySerializer(ModelSerializer):
    class Meta:
        model = InventoryModel
        fields = '__all__'

class ActionSerializer(ModelSerializer):
    class Meta:
        model = ActionModel
        fields = '__all__'

class KreditSerializer(ModelSerializer):
    class Meta:
        model = KreditModel
        fields = '__all__'

class DutySerializer(ModelSerializer):
    class Meta:
        model = DutyModel
        fields = '__all__'
    
class BrilikSerializer(ModelSerializer):
    class Meta:
        model = BirlikModel
        fields = '__all__'

class NotesSerializer(ModelSerializer):
    class Meta:
        model = NotesModel
        fields = '__all__'

class ClientSetializer(ModelSerializer):
    class Meta:
        model = ClientModel
        fields = '__all__'
    
class ClientActionSerializer(ModelSerializer):
    class Meta:
        model = ClientActionModel
        fields = '__all__'