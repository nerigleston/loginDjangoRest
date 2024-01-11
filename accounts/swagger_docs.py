from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

signup_swagger = swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password', 'email']
    ),
    responses={
        201: 'Descrição da resposta bem-sucedida do cadastro',
        400: 'Descrição da resposta de requisição inválida',
    },
    operation_description='Descrição detalhada da operação de cadastro'
)

login_swagger = swagger_auto_schema(
    methods=['POST'],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password']
    ),
    responses={
        200: 'Descrição da resposta bem-sucedida do login',
        401: 'Descrição da resposta não autorizada',
    },
    operation_description='Descrição detalhada da operação de login'
)

test_token_swagger = swagger_auto_schema(
    methods=['GET'],
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Token de autenticação',
            format='Token <token_value>',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: 'Descrição da resposta bem-sucedida do teste de token',
    },
    operation_description='Descrição detalhada da operação de teste de token',
)

get_all_users_swagger = swagger_auto_schema(
    methods=['GET'],
    responses={
        200: 'Descrição da resposta bem-sucedida de obtenção de todos os usuários',
    },
    operation_description='Descrição detalhada da operação de obtenção de todos os usuários'
)

delete_user_swagger = swagger_auto_schema(
    methods=['DELETE'],
    manual_parameters=[
        openapi.Parameter(
            'Authorization',
            openapi.IN_HEADER,
            description='Token de autenticação',
            format='Token <token_value>',
            type=openapi.TYPE_STRING,
            required=True,
        ),
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description='ID do usuário a ser excluído',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        204: 'Descrição da resposta bem-sucedida da exclusão de usuário',
        403: 'Descrição da resposta proibida',
    },
    operation_description='Descrição detalhada da operação de exclusão de usuário',
)
