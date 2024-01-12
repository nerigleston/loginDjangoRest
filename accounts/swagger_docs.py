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
        201: 'Cadastro realizado com sucesso.',
        400: 'Requisição inválida. Verifique os dados fornecidos.',
    },
    operation_description='Realiza o cadastro de um novo usuário.'
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
        200: 'Login bem-sucedido.',
        401: 'Não autorizado. Verifique as credenciais fornecidas.',
    },
    operation_description='Realiza o login do usuário.'
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
        200: 'Token válido. A autenticação foi bem-sucedida.',
    },
    operation_description='Realiza o teste de validade do token de autenticação.'
)

get_all_users_swagger = swagger_auto_schema(
    methods=['GET'],
    responses={
        200: 'Lista de usuários obtida com sucesso.',
    },
    operation_description='Obtém a lista de todos os usuários cadastrados.'
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
        204: 'Usuário excluído com sucesso.',
        403: 'Acesso proibido. Verifique suas permissões.',
    },
    operation_description='Exclui um usuário com base no ID fornecido.'
)

update_user_swagger = swagger_auto_schema(
    methods=['PUT'],
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
            description='ID do usuário a ser atualizado',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
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
        200: 'Usuário atualizado com sucesso.',
        400: 'Requisição inválida. Verifique os dados fornecidos.',
        403: 'Acesso proibido. Verifique suas permissões.',
    },
    operation_description='Atualiza as informações do usuário com base no ID fornecido.'
)

get_user_by_id_swagger = swagger_auto_schema(
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
        openapi.Parameter(
            'id',
            openapi.IN_PATH,
            description='ID do usuário a ser obtido',
            type=openapi.TYPE_STRING,
            required=True,
        ),
    ],
    responses={
        200: 'Informações do usuário obtidas com sucesso.',
        403: 'Acesso proibido. Verifique suas permissões.',
        404: 'Usuário não encontrado.',
    },
    operation_description='Obtém as informações do usuário com base no ID fornecido.'
)


get_user_by_token_swagger = swagger_auto_schema(
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
        200: 'Informações do usuário obtidas com sucesso.',
        401: 'Não autorizado. Verifique as credenciais fornecidas.',
        403: 'Acesso proibido. Verifique suas permissões.',
    },
    operation_description='Obtém as informações do usuário com base no token de autenticação.'
)

logout_swagger = swagger_auto_schema(
    methods=['POST'],
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
        200: 'Logout realizado com sucesso.',
        401: 'Não autorizado. Verifique as credenciais fornecidas.',
    },
    operation_description='Realiza o logout do usuário.'
)
