# Projeto de Gerenciamento de Estacionamento

Este projeto consiste em um sistema de gerenciamento de estacionamento utilizando FastAPI e MongoDB. O sistema é composto por vários serviços que se comunicam entre si para gerenciar usuários, créditos, vagas de estacionamento e controle de acesso.

## Estrutura do Projeto

- `api_gateway`: Gateway de API que roteia as requisições para os serviços apropriados.
- [user_service](file:///c%3A/Users/pbalc/sistema_estacionamento/user_service/main.py#1%2C3-1%2C3): Serviço responsável pelo gerenciamento de usuários.
- [credit_service](file:///c%3A/Users/pbalc/sistema_estacionamento/api_gateway/main.py#6%2C8-6%2C8): Serviço responsável pelo gerenciamento de créditos dos usuários.
- [spot_service](file:///c%3A/Users/pbalc/sistema_estacionamento/api_gateway/main.py#4%2C8-4%2C8): Serviço responsável pelo gerenciamento das vagas de estacionamento.
- [access_service](file:///c%3A/Users/pbalc/sistema_estacionamento/api_gateway/main.py#7%2C8-7%2C8): Serviço responsável pelo controle de acesso ao estacionamento.
- [gate_service](file:///c%3A/Users/pbalc/sistema_estacionamento/gate_service/main.py#1%2C3-1%2C3): Serviço responsável pelo controle da cancela do estacionamento.

## Instalação

1. Clone o repositório:
    ```sh
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_REPOSITORIO>
    ```

2. Crie e ative um ambiente virtual:
    ```sh
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```sh
    pip install -r requirements.txt
    ```

## Configuração

Certifique-se de que o MongoDB está configurado corretamente e que a URI de conexão está definida nos arquivos de serviço.

## Execução

Cada serviço pode ser iniciado individualmente. Por exemplo, para iniciar o `user_service`:

```sh
uvicorn user_service.main:app --host 0.0.0.0 --port 8001
```

Repita o comando acima para os outros serviços, alterando o caminho do módulo e a porta conforme necessário.

## Endpoints

### `api_gateway`

- **POST /users/**: Cria um novo usuário.
- **GET /users/{cpf}**: Obtém informações de um usuário pelo CPF.
- **POST /credits/**: Adiciona créditos a um usuário.
- **GET /credits/{cpf}**: Obtém créditos de um usuário pelo CPF.
- **POST /credits/{cpf}/decrement**: Decrementa créditos de um usuário.
- **GET /spots/{parking_lot}**: Obtém informações sobre vagas de um estacionamento.
- **POST /spots/**: Atualiza informações sobre vagas de um estacionamento.
- **POST /access/**: Controla o acesso ao estacionamento.
- **POST /gate/**: Controla a cancela do estacionamento.

### `user_service`

- **POST /users/**: Cria um novo usuário.
- **GET /users/{cpf}**: Obtém informações de um usuário pelo CPF.

### `credit_service`

- **POST /credits/**: Adiciona créditos a um usuário.
- **GET /credits/{cpf}**: Obtém créditos de um usuário pelo CPF.
- **POST /credits/{cpf}/decrement**: Decrementa créditos de um usuário.

### `spot_service`

- **POST /spots/**: Atualiza informações sobre vagas de um estacionamento.
- **GET /spots/{parking_lot}**: Obtém informações sobre vagas de um estacionamento.

### `access_service`

- **POST /access/**: Controla o acesso ao estacionamento.

### `gate_service`

- **POST /gate/**: Controla a cancela do estacionamento.

## Contribuição

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`).
4. Faça push para a branch (`git push origin feature/nova-feature`).
5. Crie um novo Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
