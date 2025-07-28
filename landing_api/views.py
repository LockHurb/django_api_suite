from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import db
import datetime

# Create your views here.

class LandingAPI(APIView):
    name = "Landing API"
    collection_name = "contactos"

    def get(self, request):
        
        ref = db.reference(self.collection_name)

        data = ref.get()

        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, request):
        ref = db.reference(self.collection_name)

        data = request.data
        
        current_time = datetime.datetime.now()
        custom_format = current_time.strftime("%d/%m/%Y, %I:%M:%S %p").lower().replace('am', 'a. m.').replace('pm', 'p. m.')
        data.update({"timestamp": custom_format })

        new_resource = ref.push(data)

        return Response({"id": new_resource.key}, status=status.HTTP_201_CREATED)
