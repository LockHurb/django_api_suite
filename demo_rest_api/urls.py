from django.urls import path
from . import views

urlpatterns = [
   path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_resources" ),
   path("item/", views.DemoRestApiItem.as_view(), name="demo_rest_api_item_body" ),  # Para métodos con ID en el cuerpo
   path("<str:item_id>/", views.DemoRestApiItem.as_view(), name="demo_rest_api_item" ),  # Para métodos con ID en URL
]