CREATE DATABASE IF NOT EXISTS mxodontologia;
USE mxodontologia;

CREATE TABLE IF NOT EXISTS paciente (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  data_nascimento DATE,
  telefone VARCHAR(50),
  email VARCHAR(255),
  especialidade VARCHAR(120),
  status VARCHAR(50) DEFAULT 'Ativo',
  data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consulta (
  id INT AUTO_INCREMENT PRIMARY KEY,
  paciente_id INT NOT NULL,
  data_consulta DATETIME NOT NULL,
  procedimento VARCHAR(255),
  dentista VARCHAR(120),
  status VARCHAR(50) DEFAULT 'Agendada',
  observacoes TEXT,
  FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS prontuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  paciente_id INT NOT NULL,
  data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
  procedimento VARCHAR(255),
  observacoes TEXT,
  FOREIGN KEY (paciente_id) REFERENCES paciente(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS estoque_item (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  quantidade INT NOT NULL DEFAULT 0,
  unidade VARCHAR(50),
  nivel_alerta VARCHAR(50) DEFAULT 'Normal',
  data_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transacao_financeira (
  id INT AUTO_INCREMENT PRIMARY KEY,
  data_operacao DATETIME NOT NULL,
  descricao VARCHAR(255),
  tipo ENUM('Receita', 'Despesa') NOT NULL,
  valor DECIMAL(12,2) NOT NULL,
  categoria VARCHAR(120),
  observacoes TEXT
);

CREATE TABLE IF NOT EXISTS relatorio (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  periodo VARCHAR(120),
  status VARCHAR(50) DEFAULT 'Disponível',
  data_geracao DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS usuario (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nome VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  funcao VARCHAR(100),
  senha_hash VARCHAR(255) NOT NULL,
  status VARCHAR(50) DEFAULT 'Ativo',
  ultimo_login DATETIME
);
