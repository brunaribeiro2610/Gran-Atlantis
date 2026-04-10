# 🏢 Gran Atlantis - Portal de Gestão Condominial

O **Gran Atlantis** é uma plataforma web desenvolvida para modernizar a gestão de condomínios. O sistema centraliza a comunicação entre moradores, síndicos e portaria, oferecendo uma interface intuitiva e segura para o controle de acessos e informações do condomínio.

---

## 🚀 Funcionalidades Implementadas

### 🔐 Autenticação e Segurança
- **Login Personalizado:** Interface exclusiva com tema Dark & Gold.
- **Níveis de Acesso:** Separação de permissões para Administradores (Síndicos) e Moradores.

### 📊 Dashboard (Painel de Controle)
- **Visão Geral:** Métricas rápidas sobre o condomínio.
- **Cards Informativos:** Atalhos para as principais funções do sistema.

### 👥 Gestão de Moradores
- **Cadastro de Unidades:** Organização por Bloco e Casa.
- **Tabela de Residentes:** Listagem completa com filtros de busca.
- **Solicitação de Acesso:** Fluxo para novos moradores realizarem o pré-cadastro.

### 📢 Comunicação e Portaria
- **Mural de Avisos:** Espaço para comunicados importantes do síndico.
- **Controle de Visitantes:** (Em desenvolvimento) Gestão de entrada e saída.

---

## 🛠️ Tecnologias Utilizadas

O projeto foi construído utilizando as melhores práticas de desenvolvimento web:

- **Linguagem:** [Python 3.12+](https://www.python.org/)
- **Framework Web:** [Django 5.0+](https://www.djangoproject.com/) (Arquitetura MVT)
- **Banco de Dados:** SQLite (Desenvolvimento)
- **Interface (Frontend):** - HTML5 & CSS3 (Customizado)
  - [Bootstrap 5](https://getbootstrap.com/) (Componentes e Responsividade)
  - Google Fonts (Integração de tipografia personalizada)
- **Versionamento:** Git & GitHub

---

## 📦 Estrutura do Projeto

```text
gran_atlantis/
├── core/              # App principal: Dashboard, Avisos e Lógica Central
├── usuarios/          # App de Gestão: Login, Perfis e Permissões
├── static/            # Arquivos estáticos (CSS, Imagens, JS)
├── templates/         # Arquivos HTML (Base, Login, Dashboard, Tabelas)
├── manage.py          # Gerenciador do Django
└── requirements.txt   # Dependências do sistema
