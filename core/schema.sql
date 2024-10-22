CREATE TABLE Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('Aluno', 'Orientador', 'Comissão'))
);

CREATE TABLE Aluno (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matricula VARCHAR(50) UNIQUE NOT NULL,
    usuario_id INTEGER NOT NULL,
    data_nascimento DATE NOT NULL,
    rg VARCHAR(50),
    local_nascimento VARCHAR(255),
    nacionalidade VARCHAR(255),
    curso TEXT NOT NULL CHECK (curso IN ('Mestrado', 'Doutorado')),
    orientador_id INTEGER NOT NULL,
    link_lattes VARCHAR(255),
    data_matricula DATE,
    data_aprov_exame_qualif DATE,
    data_aprov_exame_proficiencia DATE,
    data_limite_trabalho_final DATE,
    disciplinas_cursadas_aprovadas TEXT,
    disciplinas_cursadas_reprovadas TEXT,
    FOREIGN KEY (orientador_id) REFERENCES Orientador(id),
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);

CREATE TABLE Orientador (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    numero_alunos_orientados INTEGER DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);

CREATE TABLE Comissao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id)
);

CREATE TABLE Disciplina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_disciplina VARCHAR(255) NOT NULL,
    descricao TEXT,
    professor_id INTEGER NOT NULL,
    numero_alunos INTEGER NOT NULL,
    periodo TEXT NOT NULL CHECK (periodo IN ('Matutino', 'Vespertino', 'Noturno')),
    semestre VARCHAR(20) NOT NULL,
    sala VARCHAR(50),
    FOREIGN KEY (professor_id) REFERENCES Orientador(id)
);

CREATE TABLE HistoricoDisciplina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Aprovado', 'Reprovado')),
    semestre VARCHAR(20) NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES Aluno(id),
    FOREIGN KEY (disciplina_id) REFERENCES Disciplina(id)
);

CREATE TABLE Relatorio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    data_submissao DATE NOT NULL,
    arquivo_relatorio VARCHAR(255) NOT NULL,
    semestre VARCHAR(20) NOT NULL,
    reavaliacao BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (aluno_id) REFERENCES Aluno(id)
);

CREATE TABLE Avaliacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relatorio_id INTEGER NOT NULL,
    avaliador_id INTEGER NOT NULL,
    parecer TEXT NOT NULL,
    conceito TEXT NOT NULL CHECK (conceito IN ('Adequado', 'Adequado com Ressalvas', 'Insatisfatório')),
    data_avaliacao DATE NOT NULL,
    tipo_avaliador TEXT NOT NULL CHECK (tipo_avaliador IN ('Orientador', 'Comissão')),
    FOREIGN KEY (relatorio_id) REFERENCES Relatorio(id)
);

CREATE TABLE Chamado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relatorio_id INTEGER NOT NULL,
    data_abertura DATE NOT NULL,
    data_limite DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Aberto', 'Avaliando', 'Fechado')),
    notificacao_enviada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (relatorio_id) REFERENCES Relatorio(id)
);
