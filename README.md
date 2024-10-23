# Nix Shell Environment for Python Development

Este projeto configura um ambiente de desenvolvimento Python usando Nix. O arquivo `shell.nix`define um ambiente com as dependências necessárias para desenvolver aplicações Django.

## Requisitos

Nix instalado no seu sistema.

### Como instalar o Nix

#### Usando Git Bash

1. **Instale o Git Bash** se ainda não tiver instalado. Você pode baixá-lo [aqui](https://gitforwindows.org/).

2. **Abra o Git Bash**.

3. **Execute o comando de instalação**:
   ```sh
   curl -L https://nixos.org/nix/install | sh
   ```

4. **Siga as instruções** que aparecerem no terminal para completar a instalação.

5. **Reinicie o terminal** para que as mudanças tenham efeito.

6. **Verifique a instalação** executando:
   ```sh
   nix --version
   ```

#### Usando WSL (Windows Subsystem for Linux)

1. **Instale o WSL** (se ainda não tiver instalado):
   - Abra o PowerShell como administrador e execute:
     ```powershell
     wsl --install
     ```

2. **Reinicie o computador** após a instalação do WSL.

3. **Instale uma distribuição Linux** (por exemplo, Ubuntu) da Microsoft Store.

4. **Abra o terminal do WSL** (Ubuntu).

5. **Execute o comando de instalação do Nix**:
   ```sh
   curl -L https://nixos.org/nix/install | sh
   ```

6. **Siga as instruções** que aparecerem no terminal para completar a instalação.

7. **Reinicie o terminal do WSL** para que as mudanças tenham efeito.

8. **Verifique a instalação** executando:
   ```sh
   nix --version
   ```

## Configuração do Ambiente

1. **Clone o repositório**:
   ```sh
   git clone <URL-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. **Inicie o Nix Shell**:
   ```sh
   nix-shell
   ```

   Isso irá configurar o ambiente com as dependências especificadas e executar o `shellHook` para criar e ativar um ambiente virtual Python.

## Dependências

O arquivo 

shell.nix

 inclui as seguintes dependências:

- Python 3.12
- Django
- Django REST framework
- Requests
- Python-dotenv
- Faker

## Uso

Após iniciar o Nix Shell, você pode começar a desenvolver sua aplicação Django. O ambiente virtual Python será ativado automaticamente, e todas as dependências estarão disponíveis.

## Contribuição

Sinta-se à vontade para abrir issues ou pull requests para melhorias ou correções.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).