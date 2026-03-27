# 🏥 CEMTRABI — Sistema Web Institucional

Site institucional desenvolvido para a **CEMTRABI-VR**, empresa especializada em **Medicina Ocupacional, Segurança do Trabalho e Treinamentos**.

O sistema tem como objetivo apresentar os serviços da empresa e captar leads através de um formulário inteligente com validações.

---

## 🚀 Funcionalidades

### 🌐 Site Institucional

* Página inicial com apresentação da empresa
* Seções:

  * Medicina Ocupacional
  * Segurança do Trabalho
  * Treinamentos
  * Sobre Nós
* Layout moderno e responsivo

---

### 📩 Formulário de Contato Inteligente

* Captura de leads
* Validação de campos obrigatórios
* **Bloqueio de CNPJ duplicado**
* Mensagens de feedback (toast):

  * ✅ Sucesso
  * ❌ Erro
* Integração com banco de dados

---

### 📍 Múltiplas Unidades

* Seleção dinâmica de unidades
* Troca automática de:

  * Endereço
  * Mapa (Google Maps)
* Suporte atual:

  * Volta Redonda - RJ
  * Itaguaí - RJ

---

### 🎯 Interface e Experiência

* Accordion interativo
* Slider de imagens
* Feedback visual no formulário
* Design limpo e corporativo

---

## 🛠️ Tecnologias Utilizadas

* **Backend**

  * Python
  * Django

* **Frontend**

  * HTML5
  * CSS3
  * JavaScript

* **Banco de Dados**

  * SQLite (padrão do Django)

---

## 📂 Estrutura do Projeto

```
cemtrabi/
│
├── app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── contato.html
│   ├── medicina.html
│   ├── seguranca.html
│   ├── treinamentos.html
│   ├── sobre.html
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   ├── images/
│
├── db.sqlite3
├── manage.py
```

---

## ⚙️ Como Executar o Projeto

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

---

### 2. Crie o ambiente virtual

```bash
python -m venv venv
```

Ative:

**Windows**

```bash
venv\Scripts\activate
```

---

### 3. Instale as dependências

```bash
pip install django django-jazzmin openpyxl
```

---

### 4. Execute as migrações

```bash
python manage.py migrate
```

---

### 5. Inicie o servidor

```bash
python manage.py runserver
```

---

### 6. Acesse no navegador

```
http://127.0.0.1:8000/
```

---

## 🔒 Regras de Negócio

* Um CNPJ só pode enviar **um lead por vez**
* Caso já exista:

  * O sistema bloqueia o envio
  * Exibe mensagem amigável ao usuário

---

## 📌 Melhorias Futuras

* Integração com WhatsApp
* Envio de e-mail automático
* Painel administrativo personalizado
* Deploy em servidor (Hostinger / VPS)
* SEO e Google Analytics

---

## 👨‍💻 Autor

Desenvolvido por **Lucas Alves**
📧 Contato: [contatolucasalvesdev@gmail.com]
📞 Telefone: (24) 99924-8676

---

## 📄 Licença

Este projeto é de uso privado e destinado à empresa CEMTRABI.
