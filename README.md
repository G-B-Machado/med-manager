# 💊 MedManager

Sistema simples para **gerenciamento de medicamentos**, com foco em controle de horários, doses e estoque, usando Python e SQLite.

> Projeto pessoal para aprendizado de **Análise de Dados** e **organização de código em Python**, servindo também como entrada no GitHub para portfólio profissional.

---

## 📌 Funcionalidades atuais

- Cadastro de usuários
- Cadastro de medicamentos (nome, dosagem, forma)
- Programação de horários de uso
- Controle de quantidade atual e cálculo de estoque
- Criação automatizada do banco SQLite via script

---

## 🛠️ Tecnologias utilizadas

- Python 3.11+
- SQLite3
- SQL (DDL)
- Git/GitHub

---

## 📁 Estrutura do projeto

med_manager/
├── init_db.py # Criação do banco SQLite a partir do schema
├── schema.sql # Definição das tabelas (DDL)
├── database.db # Banco gerado (ignorado no Git)
├── README.md # Este arquivo
└── .gitignore # Arquivos e pastas ignoradas


---

## 🚀 Como rodar localmente

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/med-manager.git
cd med-manager
```
2. Execute o script de criação do banco:
```bash
python init_db.py
```
4. Um arquivo database.db será criado automaticamente.

--- 

📈 Futuras melhorias (roadmap)
Interface via terminal (CLI) para cadastrar/remover medicamentos

Notificações de horário (via terminal ou email)

Verificação de estoque baixo com alerta automático

Busca de preços online (web scraping ou API pública)

Exportação de dados para análise com pandas/Excel

--- 

🧠 Aprendizados com o projeto
Este projeto está sendo desenvolvido com o objetivo de:

Fixar conceitos de banco de dados relacional

Trabalhar boas práticas de organização em projetos Python

Ter um código versionado e visível no GitHub para portfólio

--- 

📄 Licença
Este projeto está sob a licença MIT.

*Desenvolvido por Guilherme Machado ✨*
