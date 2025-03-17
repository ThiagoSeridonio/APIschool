# APIschool

Um sistema básico de gerenciamento de dados para professores, turmas e alunos, utilizando manipulação de arquivos JSON como banco de dados.

## Índice

- [APIschool](#apischool)
  - [Índice](#índice)
  - [Sobre o projeto](#sobre-o-projeto)
  - [Instalação](#instalação)
  - [Como usar](#como-usar)
  - [Estrutura de banco de dados](#estrutura-de-banco-de-dados)
- [Endpoints do APIschool](#endpoints-do-apischool)
  - [Endpoints](#endpoints)
    - [Professores](#professores)
    - [Turmas](#turmas)
    - [Alunos](#alunos)
    - [Utilitário](#utilitário)
  - [Funcionalidades](#funcionalidades)
  - [Contribuições](#contribuições)
  - [Licença](#licença)

## Sobre o projeto

O **APIschool** é um projeto de gerenciamento escolar, onde os dados de professores, turmas e alunos são armazenados modificados e também deletados sendo eles manipulados em um arquivo JSON.

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/ThiagoSeridonio/APIschool

## Como usar 
1. Execute o programa principal:
    python app.py

O sistema carregará ou criará o arquivo database.json para gerenciar os dados de professores, turmas e alunos.

## Estrutura de banco de dados 
O arquivo database.json é organizado da seguinte forma:
1.   {
  "professores": [],
  "turmas": [],
  "alunos": []
}

# Endpoints do APIschool

API para gerenciamento de professores, turmas e alunos com diversas funcionalidades documentadas abaixo.

## Endpoints

### Professores

- **`GET /professores`**
  - Descrição: Retorna a lista de todos os professores.
  - Resposta: 
    ```json
    [
      {
        "id": "string",
        "nome": "string",
        "data_nascimento": "string",
        "idade": "int",
        "disciplina": "string",
        "salario": "float"
      }
    ]
    ```

- **`GET /professores/<id>`**
  - Descrição: Retorna os dados de um professor específico pelo ID.
  - Resposta: 
    ```json
    {
      "id": "string",
      "nome": "string",
      "data_nascimento": "string",
      "idade": "int",
      "disciplina": "string",
      "salario": "float"
    }
    ```

- **`POST /professores`**
  - Descrição: Adiciona um novo professor.
  - Corpo da requisição:
    ```json
    {
      "nome": "string",
      "data_nascimento": "string",
      "disciplina": "string",
      "salario": "float"
    }
    ```
  - Resposta: Retorna o professor criado.

- **`PUT /professores/<id>`**
  - Descrição: Atualiza as informações de um professor pelo ID.
  - Corpo da requisição: Contém os campos a serem atualizados.
  - Resposta: Retorna os dados atualizados do professor.

- **`DELETE /professores/<id>`**
  - Descrição: Remove um professor pelo ID.
  - Resposta: 
    ```json
    {
      "mensagem": "Professor removido com sucesso"
    }
    ```

---

### Turmas

- **`GET /turmas`**
  - Descrição: Retorna a lista de todas as turmas.

- **`GET /turmas/<id>`**
  - Descrição: Retorna os dados de uma turma específica pelo ID.

- **`POST /turmas`**
  - Descrição: Adiciona uma nova turma.
  - Corpo da requisição:
    ```json
    {
      "nome": "string",
      "turno": "string",
      "capacidade": "int"
    }
    ```
  - Resposta: Retorna a turma criada.

- **`PUT /turmas/<id>`**
  - Descrição: Atualiza as informações de uma turma pelo ID.

- **`DELETE /turmas/<id>`**
  - Descrição: Remove uma turma pelo ID.

---

### Alunos

- **`GET /alunos`**
  - Descrição: Retorna a lista de todos os alunos.

- **`GET /alunos/<id>`**
  - Descrição: Retorna os dados de um aluno específico pelo ID.

- **`POST /alunos`**
  - Descrição: Adiciona um novo aluno.
  - Corpo da requisição:
    ```json
    {
      "nome": "string",
      "data_nascimento": "string",
      "nota_primeiro_semestre": "float",
      "nota_segundo_semestre": "float"
    }
    ```

- **`PUT /alunos/<id>`**
  - Descrição: Atualiza as informações de um aluno pelo ID.

- **`DELETE /alunos/<id>`**
  - Descrição: Remove um aluno pelo ID.

---

### Utilitário

- **`DELETE /delete_all`**
  - Descrição: Remove todos os dados (professores, turmas e alunos) do sistema.
  - Resposta:
    ```json
    {
      "mensagem": "Todos os dados foram removidos"
    }
    ```

---

## Funcionalidades
Carregamento de Dados: Carrega automaticamente os dados do arquivo database.json na inicialização.

Armazenamento de Dados: Salva os dados no arquivo database.json após cada alteração.

Geração de UUID: Cada registro recebe um identificador único (UUID).

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma pull request ou relatar issues.

## Licença
Este projeto está licenciado sob a MIT License.
