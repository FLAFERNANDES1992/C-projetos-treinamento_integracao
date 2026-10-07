# 🌐 Guia Passo a Passo: Publicar o BRVAL Hub de Treinamentos na Nuvem (Gratuito)

Este guia orienta como disponibilizar o **BRVAL Hub de Treinamentos** em um link oficial na web (ex: `https://brval-hub.streamlit.app`), permitindo que gestores, diretores e analistas de DP acessem o sistema de qualquer computador ou celular.

---

## 📌 Como funciona o Streamlit Community Cloud
* **O que é:** O serviço oficial de hospedagem em nuvem mantido pela Snowflake/Streamlit.
* **Custo:** 100% Gratuito.
* **Segurança:** O repositório no GitHub pode ser **Privado** ou **Público**. O processamento continua estritamente em memória volátil (RAM), respeitando a LGPD.
* **Atualizações:** Sempre que você alterar um arquivo no repositório, o site se atualiza automaticamente em tempo real.

---

## 🚀 Passo 1: Criar o Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login (ou crie uma conta gratuita).
2. No canto superior direito, clique no botão **`+`** e selecione **`New repository`** (Novo repositório).
3. Preencha os campos:
   * **Repository name:** `treinamento-integracao-brval`
   * **Visibility:** Escolha **Public** (Público) ou **Private** (Privado).
   * Desmarque a opção de adicionar README (o projeto já tem o seu).
4. Clique em **`Create repository`**.

---

## 📂 Passo 2: Subir os Arquivos do Projeto

### Opção A: Pela própria página web do GitHub (Mais Fácil - Sem Instalações)
1. Na página do repositório recém-criado, clique no link **"uploading an existing file"** (carregar arquivos existentes).
2. Abra a pasta `c:\projetos\treinamento_integracao` no seu Windows Explorer.
3. Arraste os seguintes arquivos e pastas para o GitHub:
   * `app.py` *(Obrigatório)*
   * `audit_engine.py` *(Obrigatório)*
   * `requirements.txt` *(Obrigatório)*
   * `BRVAL logo.png` *(Obrigatório para a identidade visual)*
   * `Controle de Treinamento 03 anos.xlsx` *(Obrigatório para o arquivo demonstrativo)*
   * `.streamlit/config.toml` *(Para manter o Dark Theme corporativo)*
   * `README.md`
   * `.gitignore`
4. Na parte inferior da página do GitHub, clique no botão verde **`Commit changes`**.

---

## ⚡ Passo 3: Ativar o Deploy no Streamlit Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io).
2. Clique em **"Sign in with GitHub"** (Entrar com sua conta GitHub).
3. Clique no botão azul **"Create app"** (ou **"New app"**).
4. Selecione a opção **"I already have an app"**.
5. Preencha os 3 campos:
   * **Repository:** Selecione o repositório criado (ex: `seu-usuario/treinamento-integracao-brval`).
   * **Branch:** `main`
   * **Main file path:** `app.py`
   * *(Opcional)* **App URL:** Você pode personalizar o link para algo como `brval-treinamentos.streamlit.app`.
6. Clique no botão **"Deploy!"**.

---

## 🎉 Pronto!
Em cerca de 1 a 2 minutos, o Streamlit instalará os pacotes e exibirá seu site ao vivo.
* O link gerado (ex: `https://brval-treinamentos.streamlit.app`) pode ser enviado por WhatsApp, Teams, e-mail ou Slack para qualquer pessoa da BRVAL.
* A página funcionará de forma responsiva tanto em computadores quanto em tablets e smartphones.
