from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from .swagger_docs import (
    signup_swagger,
    login_swagger,
    test_token_swagger,
    get_all_users_swagger,
    delete_user_swagger,
    update_user_swagger
)


@signup_swagger
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_swagger
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.filter(username=username).first()

    if user and user.check_password(password):
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_200_OK)

    return Response({'detail': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


@test_token_swagger
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    user = request.user
    return Response("Token Válido para o usuário {}".format(user.username), status=status.HTTP_200_OK)


@get_all_users_swagger
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@delete_user_swagger
@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.user != user:
        return Response("Você não tem permissão para excluir este usuário", status=status.HTTP_403_FORBIDDEN)

    user.delete()
    return Response("Usuário deletado com sucesso", status=status.HTTP_204_NO_CONTENT)


@update_user_swagger
@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, id):
    user = get_object_or_404(User, id=id)

    if request.user != user:
        return Response("Você não tem permissão para atualizar este usuário", status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
