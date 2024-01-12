from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from django.conf import settings
from django.middleware import csrf
from .swagger_docs import (
    signup_swagger,
    login_swagger,
    test_token_swagger,
    get_all_users_swagger,
    delete_user_swagger,
    update_user_swagger,
    get_user_by_id_swagger,
    get_user_by_token_swagger,
    logout_swagger
)


@signup_swagger
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Mova a linha abaixo para garantir que 'refresh' seja definido antes de ser usado
        refresh = RefreshToken.for_user(user)

        token = Token.objects.get(user=user)

        response_data = {
            'token': token.key,
            'user': serializer.data
        }

        response = Response(response_data, status=status.HTTP_201_CREATED)

        # Configuração do cookie para o access_token
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=token.key,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        # Configuração do cookie para o refresh_token
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=str(refresh),
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response["X-CSRFToken"] = csrf.get_token(request)
        return response

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

        # Adição da definição de "refresh" aqui
        refresh = RefreshToken.for_user(user)

        response_data = {
            'token': token.key,
            'user': serializer.data
        }

        response = Response(response_data, status=status.HTTP_200_OK)

        # Configuração do cookie para o access_token
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=token.key,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            value=str(refresh),
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response["X-CSRFToken"] = csrf.get_token(request)
        return response

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

    # Verifica se o usuário que está fazendo a requisição é o próprio usuário que está sendo atualizado
    if request.user != user:
        return Response("Você não tem permissão para atualizar este usuário", status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        user = serializer.save()

        if 'password' in serializer.validated_data:
            user.set_password(serializer.validated_data['password'])
            user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@get_user_by_id_swagger
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, id):
    user = get_object_or_404(User, id=id)

    if request.user != user:
        return Response("Você não tem permissão para visualizar este usuário", status=status.HTTP_403_FORBIDDEN)

    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@get_user_by_token_swagger
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_by_token(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@logout_swagger
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response("Logout realizado com sucesso", status=status.HTTP_200_OK)
