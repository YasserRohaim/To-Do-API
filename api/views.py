from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import TaskSerializer, CategorySerializer,UserSerializer
from .models import Tasks, Categories
from .permissions import IsObjCreator

@api_view(["POST"])
def sign_up(request):
    if request.method=="POST":
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(["POST"])
def sign_in(request):
    if request.method=="POST":
        username=request.data.get("username")
        password=request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            # Generate or get existing token
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def task_list(request):
    user = request.user
    tasks = Tasks.objects.filter(created_by=user).order_by('completed','-priority', 'deadline')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsObjCreator])
def task_details(request,task_id):
    try:
        task = Tasks.objects.get(id=task_id)
        if request.user.is_authenticated and IsObjCreator().has_object_permission(request, None, task):
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        else:
            return Response({'error': 'You do not have permission to access this task.'}, status=status.HTTP_403_FORBIDDEN)
  
    except Tasks.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_task(request):
    data = request.data
    # Set 'created_by' field to the authenticated user
    data['created_by'] = request.user.id
    
    # Serialize data
    serializer = TaskSerializer(data=data)
    
    # Validate and save the serializer
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["PUT","DELETE"])
@permission_classes([IsObjCreator])
def update_task(request,task_id):
    try:
        task = Tasks.objects.get(id=task_id)
        if not(request.user.is_authenticated and IsObjCreator().has_object_permission(request, None, task)):
            return Response({'error': 'You do not have permission to access this task.'}, status=status.HTTP_403_FORBIDDEN)
  
            
        if request.method=="PUT":
            serializer = TaskSerializer(task,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method=="DELETE":
            task.delete()
            return Response({"message":"Task has been deleted successfully"},status=status.HTTP_200_OK)
        
    except Tasks.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_finished(request):
    try:
        user_id=request.user.id
        completed_tasks=Tasks.objects.get(created_by=user_id,completed=True)
        deleted_count, _ = completed_tasks.delete()
        return Response({'message': f'{deleted_count} completed tasks deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as error:
        return Response({'error': str(error)},status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_tasks(request):
    try:
        user_id=request.user.id
        tasks=Tasks.objects.get(created_by=user_id)
        deleted_count, _ = tasks.delete()
        return Response({'message': f'{deleted_count} completed tasks deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as error:
        return Response({'error': str(error)},status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_list(request):
    user = request.user
    categories = Categories.objects.filter(created_by=user)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsObjCreator])
def category_details(request,category_id):
    try:
        category = Categories.objects.get(id=category_id)
        if not(request.user.is_authenticated and IsObjCreator().has_object_permission(request, None, category)):
            return Response({'error': 'You do not have permission to access this category.'}, status=status.HTTP_403_FORBIDDEN)
        category = Categories.objects.get(id=category_id)
        category_serializer = CategorySerializer(category)

        # Retrieve tasks associated with the category
        tasks = Tasks.objects.filter(category=category)
        task_serializer = TaskSerializer(tasks, many=True)

        # Combine category details and associated tasks in response data
        response_data = {
            'category': category_serializer.data,
            'tasks': task_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except Categories.DoesNotExist:
        return Response({'error': 'Category is not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category(request):
    data = request.data
    # Set 'created_by' field to the authenticated user
    data['created_by'] = request.user.id
    
    # Serialize data
    serializer = CategorySerializer(data=data)
    
    # Validate and save the serializer
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(["PUT","DELETE"])
@permission_classes([IsObjCreator])
def update_category(request,category_id):
    try:
        category = Categories.objects.get(id=category_id)
        if not(request.user.is_authenticated and IsObjCreator().has_object_permission(request, None, category)):
            return Response({'error': 'You do not have permission to access this category.'}, status=status.HTTP_403_FORBIDDEN)
  
            
        if request.method=="PUT":
            serializer = CategorySerializer(category,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method=="DELETE":
            category.delete()
            return Response({"message":"The category has been deleted successfully"},status=status.HTTP_200_OK)
        
    except Categories.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)







