CREATE TABLE Usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    /*tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('Aluno', 'Docente', 'Comissão'))*/
);

CREATE TABLE Aluno (
    usuario_id INTEGER NOT NULL,
    matricula VARCHAR(50) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    rg VARCHAR(50),
    local_nascimento VARCHAR(255),
    nacionalidade VARCHAR(255),
    curso TEXT NOT NULL CHECK (curso IN ('Mestrado', 'Doutorado')),
    link_lattes VARCHAR(255),
    data_matricula DATE,
    data_aprov_exame_qualif DATE,
    data_aprov_exame_proficiencia DATE,
    data_limite_trabalho_final DATE,
    disciplinas_cursadas_aprovadas TEXT, -- restrição de integridade
    disciplinas_cursadas_reprovadas TEXT,-- restrição de integridade
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE,
    PRIMARY KEY (usuario_id)   
);

CREATE TABLE Docente (
    usuario_id INTEGER NOT NULL,
    numero_alunos_orientados INTEGER DEFAULT 0, -- restrição de integridade
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE,
    PRIMARY KEY (usuario_id) 
);

CREATE TABLE Comissao (
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuario(id) ON DELETE CASCADE,
    PRIMARY KEY (usuario_id)
);

CREATE TABLE Disciplina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_disciplina VARCHAR(255) NOT NULL,
    descricao TEXT,
);

CREATE TABLE Oferecimento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    docente_id INTEGER NOT NULL,
    disciplina_id INTEGER NOT NULL,
    vagas_total INTEGER NOT NULL,
    vagas_remanescentes INTEGER NOT NULL, -- restrição de integridade
    periodo TEXT NOT NULL CHECK (periodo IN ('Matutino', 'Vespertino', 'Noturno')),
    semestre VARCHAR(20) NOT NULL,
    sala VARCHAR(50),
    FOREIGN KEY (docente_id) REFERENCES Docente(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (disciplina_id) REFERENCES Disciplina(id) ON DELETE CASCADE
);

CREATE TABLE Matricula (
    oferecimento_id INTEGER NOT NULL,
    aluno_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Aprovado', 'Reprovado')),
    FOREIGN KEY (oferecimento_id) REFERENCES Oferecimento(id) ON DELETE CASCADE,
    FOREIGN KEY (aluno_id) REFERENCES Aluno(usuario_id) ON DELETE CASCADE,
    PRIMARY KEY (oferecimento_id, aluno_id)
);

CREATE TABLE Orientacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER UNIQUE NOT NULL, -- unique -> um aluno só tem um orientador
    docente_id INTEGER NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES Aluno(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (docente_id) REFERENCES Docente(usuario_id) ON DELETE CASCADE
);


CREATE TABLE Relatorio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orientacao_id INTEGER NOT NULL,
    data_submissao DATE NOT NULL,
    arquivo_relatorio VARCHAR(255) NOT NULL,
    semestre VARCHAR(20) NOT NULL,
    reavaliacao BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (orientacao_id) REFERENCES Orientacao(id) ON DELETE CASCADE
    
);

CREATE TABLE Avaliacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relatorio_id INTEGER NOT NULL,
    avaliador_id INTEGER NOT NULL, -- restrição de integridade
    parecer TEXT NOT NULL,
    conceito TEXT NOT NULL CHECK (conceito IN ('Adequado', 'Adequado com Ressalvas', 'Insatisfatório')),
    data_avaliacao DATE NOT NULL,
    tipo_avaliador TEXT NOT NULL CHECK (tipo_avaliador IN ('Orientador', 'Comissão')), -- restrição de integridade
    FOREIGN KEY (relatorio_id) REFERENCES Relatorio(id) ON DELETE CASCADE,
    FOREIGN KEY (avaliador_id) REFERENCES Usuario(id) ON DELETE CASCADE,
);

/*
ainda nao sei pq isso existe

CREATE TABLE Chamado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relatorio_id INTEGER NOT NULL,
    data_abertura DATE NOT NULL,
    data_limite DATE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('Aberto', 'Avaliando', 'Fechado')),
    notificacao_enviada BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (relatorio_id) REFERENCES Relatorio(id)
);
*/
