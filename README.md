# [💟 Anime Daisuki! API](https://documenter.getpostman.com/view/17890889/UV5ZAbTe)

### API de animes com cadastro de usuários. O usuário autenticado pode avaliar e favoritar animes, comentar episódios e verificar o histórico de episódios assistidos

#### Projeto concluído ✔️

[Sobre](#sobre) • [Tecnologias](#tecnologias) • [Instalação](#instalação) • [Demonstração](#demonstração) • [Autores](#autores) • [Licença](#licença)

## Sobre

Projeto desenvolvido no terceiro trimestre da Kenzie Academy Brasil com o objetivo de criar uma API, aplicando os conceitos de CRUD, SQL, migrations, autenticação (JSON Web Tokens) e segurança (geração de hash para senha). Anime Daisuki! API é uma aplicação de cadastro de usuários, animes, episódios e comentários. Você pode utilizar o deploy no [Heroku](https://animedaisuki.herokuapp.com/api) e fazer requisições de qualquer client seguindo os endpoints /users, /animes e /episodes na [documentação](https://documenter.getpostman.com/view/17890889/UV5ZAbTe).
Caso queira rodar a aplicação na sua própria máquina, siga as instruções na seção [Instalação](#instalação).

## Tecnologias

As seguintes ferramentas foram utilizadas na construção do projeto:

- [Python](https://docs.python.org/3/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [JWT](https://jwt.io/)

## Instalação

Renomeie o arquivo .env.example para .env e preencha com as informações do banco que deseja utilizar. Ative o ambiente virtual seguindo os comandos:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

Agora, dentro do ambiente virtual, insira o comando para instalar as dependências:

```bash
pip install -r requirements.txt
```

Para que as tabelas sejam inseridas no seu banco de dados, rode o comando:

```bash
flask db upgrade
```

Insira dados nas tabelas com os seguintes comandos (nessa ordem):

```bash
flask cli_genres create
flask cli_animes create
flask cli_episodes create
```

Inicie o flask:

```bash
flask run
```

Pronto! Agora você já pode fazer requisições seguindo os endpoints na seção [Demonstração](#demonstração), substituindo a url do heroku pelo localhost. Mas caso queira cadastrar um usuário com permissão de admin, insira o seguinte comando substituindo por seu e-mail, usuário e senha:

```bash
flask cli_admin create teste@gmail.com teste 1234
```

É possível também promover um usuário já cadastrado com o comando:

```bash
flask cli_admin upgrade --email=teste@gmail.com

# ou

flask cli_admin upgrade --username=teste
```

E para remover o cargo de admin, tornando-o um usuário comum, rode o comando:

```bash
flask cli_admin downgrade teste@gmail.com

# ou utilize o parâmetro --permission para torná-lo um moderador

flask cli_admin downgrade teste@gmail.com --permission=mod
```

## Demonstração

Todos os endpoints da aplicação estão descritos na [documentação](https://documenter.getpostman.com/view/17890889/UV5ZAbTe). A rota de criação de users no [Heroku](https://animedaisuki.herokuapp.com/api) permite somente a criação de usuários comuns, então para criar um admin ou mod siga os últimos comandos da seção acima e faça as requisições utilizando um client como o Postman e substituindo a url com o localhost:

![Postman](https://i.imgur.com/BW8KNef.png)

## Autores

Feito com ❤️ por:

- **Laiane Suzart**:
  <br>
  [![Linkedin Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&link=https://www.linkedin.com/in/laianesuzart/)](https://www.linkedin.com/in/laianesuzart/)
  [![Github Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&link=https://github.com/laianesuzart)](https://github.com/laianesuzart)

- **Paulo Thor**:
  <br>
  [![Linkedin Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&link=https://www.linkedin.com/in/paulothorsilva/)](https://www.linkedin.com/in/paulothorsilva/) [![Github Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&link=https://github.com/PauloThor)](https://github.com/PauloThor)

- **Thaina Ferreira**:
  <br>
  [![Linkedin Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&link=https://www.linkedin.com/in/thainaferreira/)](https://www.linkedin.com/in/thainaferreira/) [![Github Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&link=https://github.com/thainaferreira)](https://github.com/thainaferreira)

- **Matheus Paiva**:
  <br>
  [![Linkedin Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&link=https://www.linkedin.com/in/matheus-paiva-vieira/)](https://www.linkedin.com/in/matheus-paiva-vieira/) [![Github Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&link=https://github.com/matheuspaivah2)](https://github.com/matheuspaivah2)

- **Emanuela Quizini**:
  <br>
  [![Linkedin Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white&link=https://www.linkedin.com/in/emanuela-biondo-quizini-245ab0195/)](https://www.linkedin.com/in/emanuela-biondo-quizini-245ab0195/) [![Github Badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white&link=https://github.com/emanuelakenzie)](https://github.com/emanuelakenzie)

## Licença

Este projeto está sob a licença [MIT](https://choosealicense.com/licenses/mit/).
