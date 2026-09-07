# 🌐 Projeto Web — HTML, CSS e Python

Projeto desenvolvido para criação de um site utilizando **HTML, CSS e Python**, com uma estrutura organizada e preparada para evolução futura.

## 📋 Sobre o Projeto

Este projeto tem como objetivo desenvolver uma aplicação web utilizando:

* **HTML5** — estrutura das páginas
* **CSS3** — estilização e layout
* **Python** — lógica e processamento no servidor
* **Flask** — framework Python para desenvolvimento web

A proposta é criar uma aplicação simples, organizada e responsiva, servindo também como projeto de estudo e prática de desenvolvimento web.

---

## 🚀 Tecnologias Utilizadas

| Tecnologia | Utilização                     |
| ---------- | ------------------------------ |
| HTML5      | Estrutura das páginas          |
| CSS3       | Estilos, cores e layout        |
| Python     | Back-end e lógica da aplicação |
| Flask      | Framework web                  |
| Git        | Controle de versão             |
| GitHub     | Hospedagem do código           |

---

## 📁 Estrutura do Projeto

```text
projeto-web/
│
├── app.py
│
├── requirements.txt
│
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── script.js
    │
    └── img/
        └── logo.png
```

### 📄 Descrição dos arquivos

**`app.py`**

Arquivo principal da aplicação Python. É responsável por iniciar o servidor e controlar as rotas da aplicação.

**`templates/`**

Diretório utilizado para armazenar os arquivos HTML.

**`static/`**

Diretório destinado aos arquivos estáticos do projeto.

Dentro dele podem ser encontrados:

* CSS
* JavaScript
* imagens
* ícones
* fontes

**`requirements.txt`**

Lista das bibliotecas Python utilizadas no projeto.

**`README.md`**

Documentação do projeto.

---

# ⚙️ Instalação

## 1. Clonar o projeto

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
```

Entre na pasta:

```bash
cd seu-repositorio
```

---

## 2. Criar ambiente virtual

No Windows:

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

No Linux ou macOS:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Instalar o Flask

```bash
pip install flask
```

Ou, caso o projeto possua `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

# ▶️ Executando o Projeto

Depois de instalar as dependências, execute:

```bash
python app.py
```

O servidor será iniciado localmente.

Acesse no navegador:

```text
http://127.0.0.1:5000
```

ou:

```text
http://localhost:5000
```

---

# 🖥️ Front-end

O front-end do projeto é desenvolvido utilizando **HTML5 e CSS3**.

Exemplo de estrutura:

```html
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Meu Site</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>

<body>

    <header>
        <h1>Meu Site</h1>
    </header>

    <main>
        <h2>Bem-vindo!</h2>
        <p>Meu primeiro projeto utilizando HTML, CSS e Python.</p>
    </main>

</body>

</html>
```

---

# 🐍 Back-end com Python

O Python será responsável pelo processamento das informações e comunicação entre o navegador e o servidor.

Exemplo utilizando Flask:

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
```

---

# 🔄 Funcionamento

O funcionamento básico da aplicação será:

```text
Usuário
   │
   ▼
Navegador
   │
   ▼
HTML + CSS
   │
   ▼
Flask
   │
   ▼
Python
   │
   ▼
Processamento
   │
   ▼
Resposta para o navegador
```

---

# 📱 Responsividade

O site será desenvolvido para funcionar em diferentes tamanhos de tela:

* 💻 Computadores
* 💻 Notebooks
* 📱 Smartphones
* 📱 Tablets

Para isso, serão utilizadas técnicas de **CSS responsivo** e `media queries`.

---

# 🔐 Segurança

Durante a evolução do projeto, poderão ser implementados recursos como:

* Validação de formulários
* Autenticação de usuários
* Controle de acesso
* Proteção de senhas
* Sessões
* HTTPS
* Proteção contra ataques comuns
* Controle de permissões

> Senhas nunca devem ser armazenadas diretamente em texto puro.

---

# 🗄️ Banco de Dados

O projeto poderá futuramente utilizar um banco de dados para armazenar informações.

Algumas opções:

* SQLite
* MySQL
* PostgreSQL

Exemplo de evolução:

```text
HTML
  │
  ▼
CSS
  │
  ▼
Flask
  │
  ▼
Python
  │
  ▼
Banco de Dados
```

---

# 📌 Funcionalidades Futuras

* [ ] Página inicial
* [ ] Menu de navegação
* [ ] Página de contato
* [ ] Formulários
* [ ] Cadastro de usuários
* [ ] Login
* [ ] Sistema de autenticação
* [ ] Banco de dados
* [ ] Área administrativa
* [ ] Dashboard
* [ ] Responsividade
* [ ] Validação de dados
* [ ] API
* [ ] Deploy em servidor

---

# 📚 Objetivo de Aprendizado

Este projeto também tem como finalidade praticar conceitos de:

* Desenvolvimento Front-end
* Desenvolvimento Back-end
* HTML
* CSS
* Python
* Flask
* Git
* GitHub
* APIs
* Banco de dados
* Estrutura de projetos web

---

# 🔧 Melhorias Futuras

Com a evolução do projeto, novas tecnologias poderão ser adicionadas, como:

```text
HTML
CSS
JavaScript
   │
   ▼
Python + Flask
   │
   ▼
API REST
   │
   ▼
Banco de Dados
   │
   ▼
Deploy
```

---

# 📄 Licença

Este projeto pode ser utilizado para fins de estudo, aprendizado e desenvolvimento.

---

# 👨‍💻 Autor

**Cezar Silva**

Projeto desenvolvido para estudos e prática de desenvolvimento web.

---

⭐ Se este projeto foi útil para você, considere deixar uma estrela no repositório!
