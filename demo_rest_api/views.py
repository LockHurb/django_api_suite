from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):
        active_items = [item for item in data_list if item["is_active"]==True]
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


class DemoRestApiItem(APIView):
    name = "Demo REST API Item"
    
    def _find_item_by_id(self, item_id):
        """Método auxiliar para encontrar un elemento por ID"""
        for item in data_list:
            if item['id'] == item_id:
                return item
        return None
    
    def put(self, request, item_id=None):
        """PUT: Reemplazar completamente los datos de un elemento (excepto el ID)"""
        data = request.data
        
        # Obtener ID de la URL o del cuerpo
        if item_id is None:
            if 'id' not in data:
                return Response({'error': 'El campo "id" es obligatorio cuando no se proporciona en la URL.'}, status=status.HTTP_400_BAD_REQUEST)
            item_id = data['id']
        
        # Buscar el elemento por ID
        item = self._find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Validación: campos requeridos
        if 'name' not in data or 'email' not in data:
            return Response({'error': 'Los campos "name" y "email" son obligatorios.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Reemplazar completamente (excepto el ID)
        original_id = item['id']
        item.clear()
        item.update(data)
        item['id'] = original_id  # Mantener el ID original
        
        # Si no se especifica is_active, se establece como True por defecto
        if 'is_active' not in item:
            item['is_active'] = True
            
        return Response({'message': 'Elemento reemplazado exitosamente.', 'data': item}, status=status.HTTP_200_OK)
    
    def patch(self, request, item_id=None):
        """PATCH: Actualizar parcialmente los campos del elemento"""
        data = request.data
        
        # Obtener ID de la URL o del cuerpo
        if item_id is None:
            if 'id' not in data:
                return Response({'error': 'El campo "id" es obligatorio cuando no se proporciona en la URL.'}, status=status.HTTP_400_BAD_REQUEST)
            item_id = data['id']
        
        # Buscar el elemento por ID
        item = self._find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        
        # Actualizar solo los campos proporcionados (excepto el ID)
        updated_fields = []
        for key, value in data.items():
            if key != 'id':  # No permitir modificar el ID
                item[key] = value
                updated_fields.append(key)
        
        if not updated_fields:
            return Response({'message': 'No se proporcionaron campos para actualizar.'}, status=status.HTTP_200_OK)
            
        return Response({
            'message': 'Elemento actualizado parcialmente.',
            'updated_fields': updated_fields,
            'data': item
        }, status=status.HTTP_200_OK)
    
    def delete(self, request, item_id=None):
        """DELETE: Eliminar lógicamente un elemento (marcar como inactivo)"""
        data = request.data
        
        # Obtener ID de la URL o del cuerpo
        if item_id is None:
            if 'id' not in data:
                return Response({'error': 'El campo "id" es obligatorio cuando no se proporciona en la URL.'}, status=status.HTTP_400_BAD_REQUEST)
            item_id = data['id']
        
        # Buscar el elemento por ID
        item = self._find_item_by_id(item_id)
        if not item:
            return Response({'error': 'Elemento no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Verificar si ya está eliminado lógicamente
        if item.get('is_active', True) == False:
            return Response({'error': 'El elemento ya está eliminado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Eliminación lógica: marcar como inactivo
        item['is_active'] = False
        
        return Response({
            'message': 'Elemento eliminado lógicamente.',
            'data': item
        }, status=status.HTTP_200_OK)
    