from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET con IDs fijos para facilitar las pruebas
data_list.append({'id': '123e4567-e89b-12d3-a456-426614174001', 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': '123e4567-e89b-12d3-a456-426614174002', 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': '123e4567-e89b-12d3-a456-426614174003', 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', True)]
      return Response(active_items, status=status.HTTP_200_OK)
    
    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DebugView(APIView):
    """Vista para depurar y ver el estado actual de data_list"""
    
    def get(self, request):
        return Response({
            'total_items': len(data_list),
            'all_items': data_list,
            'active_items': [item for item in data_list if item.get('is_active', True)],
            'inactive_items': [item for item in data_list if not item.get('is_active', True)]
        }, status=status.HTTP_200_OK)


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"

    def put(self, request, id):
        """
        Reemplaza completamente los datos de un elemento del arreglo,
        excepto el identificador que se envía como campo obligatorio.
        """
        data = request.data

        # Debug: mostrar información para depuración
        print(f"PUT - ID recibido en URL: '{id}' (tipo: {type(id)})")
        print(f"PUT - IDs disponibles en data_list:")
        for i, item in enumerate(data_list):
            print(f"  [{i}] ID: '{item.get('id')}' (tipo: {type(item.get('id'))})")

        # Validación del ID en el cuerpo de la solicitud
        if 'id' not in data:
            return Response({'error': 'El campo id es obligatorio en el cuerpo de la solicitud.'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Validación de campos requeridos
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Los campos name y email son obligatorios.'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Buscar el elemento por ID
        for i, item in enumerate(data_list):
            if item.get('id') == id:
                # Reemplazar completamente los datos manteniendo el ID original
                new_item = {
                    'id': id,  # Mantener el ID original de la URL
                    'name': data['name'],
                    'email': data['email'],
                    'is_active': data.get('is_active', True)
                }
                data_list[i] = new_item
                return Response({'message': 'Elemento actualizado exitosamente.', 'data': new_item}, 
                              status=status.HTTP_200_OK)

        return Response({
            'error': 'Elemento no encontrado.',
            'debug_info': {
                'id_buscado': id,
                'ids_disponibles': [item.get('id') for item in data_list]
            }
        }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        """
        Actualiza parcialmente los campos del elemento identificado por su ID,
        manteniendo los valores no modificados.
        """
        data = request.data

        # Buscar el elemento por ID
        for i, item in enumerate(data_list):
            if item.get('id') == id:
                # Actualizar solo los campos proporcionados
                updated_item = item.copy()
                
                if 'name' in data:
                    updated_item['name'] = data['name']
                if 'email' in data:
                    updated_item['email'] = data['email']
                if 'is_active' in data:
                    updated_item['is_active'] = data['is_active']

                data_list[i] = updated_item
                return Response({'message': 'Elemento actualizado parcialmente.', 'data': updated_item}, 
                              status=status.HTTP_200_OK)

        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        """
        Elimina lógicamente un elemento del arreglo según el identificador proporcionado.
        """
        # Buscar el elemento por ID
        for i, item in enumerate(data_list):
            if item.get('id') == id:
                # Eliminación lógica: cambiar is_active a False
                data_list[i]['is_active'] = False
                return Response({'message': 'Elemento eliminado lógicamente.', 'data': data_list[i]}, 
                              status=status.HTTP_200_OK)

        return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)