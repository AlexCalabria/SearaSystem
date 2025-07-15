🕊️ Sistema de Gerenciamento da Casa de Umbanda

Este projeto é um sistema de cadastro e controle de mensalidades para uma Casa de Umbanda, desenvolvido em **Python** com **interface gráfica (Tkinter)** e integração com **MySQL**. Ele permite o gerenciamento de médiuns, verificação de inadimplência e registro de dados relevantes da instituição.

---

## 📋 Funcionalidades

- Cadastro de médiuns com dados pessoais e profissionais  
- Cálculo automático do valor da mensalidade conforme situação profissional  
- Edição, listagem e exclusão de registros  
- Verificação de inadimplência com base em pagamentos mensais  
- Interface gráfica simples e funcional para facilitar o uso

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Tkinter** (interface gráfica)
- **MySQL** (armazenamento de dados)
- **mysql-connector-python** (conector para banco de dados)

---

## ⚙️ Pré-requisitos

- Python 3 instalado  
- MySQL Server em funcionamento  
- Biblioteca `mysql-connector-python` instalada:  
  ```bash
  pip install mysql-connector-python
  ```

---

## 🗄️ Estrutura Esperada do Banco de Dados

Banco: `casa_umbanda`  
Tabela: `mediuns`

```sql
CREATE DATABASE casa_umbanda;

USE casa_umbanda;

CREATE TABLE mediuns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    email VARCHAR(100),
    data_nascimento DATE,
    sexo VARCHAR(20),
    estado_civil VARCHAR(30),
    cargo VARCHAR(30),
    situacao_profissional VARCHAR(30),
    valor_mensalidade DECIMAL(10,2),
    data_entrada DATE,
    pagamento_1 BOOLEAN DEFAULT FALSE,
    pagamento_2 BOOLEAN DEFAULT FALSE,
    pagamento_3 BOOLEAN DEFAULT FALSE,
    pagamento_4 BOOLEAN DEFAULT FALSE,
    pagamento_5 BOOLEAN DEFAULT FALSE,
    pagamento_6 BOOLEAN DEFAULT FALSE,
    pagamento_7 BOOLEAN DEFAULT FALSE,
    pagamento_8 BOOLEAN DEFAULT FALSE,
    pagamento_9 BOOLEAN DEFAULT FALSE,
    pagamento_10 BOOLEAN DEFAULT FALSE,
    pagamento_11 BOOLEAN DEFAULT FALSE,
    pagamento_12 BOOLEAN DEFAULT FALSE
);
```

> **Importante:** Atualize o campo `password` na função `conectar()` com a sua senha do MySQL.

---

## 🚀 Como Executar o Projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/SeuUsuario/SearaSystem.git
   cd SearaSystem
   ```

2. Configure o banco de dados conforme a estrutura acima.

3. Execute o arquivo principal:
   ```bash
   python sistema_umbanda.py
   ```

---

## 📌 Melhorias Futuras

- Adição de relatórios em PDF
- Sistema de login e permissões
- Envio automático de notificações por e-mail
- Interface gráfica mais moderna (ex: com `customtkinter` ou `PySide`)

---

## 🤝 Contribuição

Sinta-se à vontade para sugerir melhorias ou abrir issues. Toda contribuição é bem-vinda!
