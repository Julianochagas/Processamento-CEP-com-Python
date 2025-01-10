# Projeto: Processamento de Dados de CEP

![Capa do Projeto](https://via.placeholder.com/1200x400?text=Processamento+de+Dados+de+CEP)

![Status do projeto](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

## Índice

- [Descrição do Projeto](#descrição-do-projeto)
- [Status do Projeto](#status-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Demonstração da Aplicação](#demonstração-da-aplicação)
- [Como Acessar o Projeto](#como-acessar-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Configuração Inicial](#configuração-inicial)
- [Estrutura de Arquivos](#estrutura-de-arquivos)
- [Licença](#licença)

## Descrição do Projeto

Este projeto tem como objetivo processar dados de CEPs para gerar relatórios personalizados e enviar e-mails automatizados com base em informações extraídas de arquivos CSV e Excel. Ele é especialmente útil para automatizar tarefas de comunicação em massa baseadas em localizações geográficas.

## Status do Projeto

🚧 Em desenvolvimento 🚧

## Funcionalidades

- Processamento de listas de CEPs a partir de arquivos CSV.
- Geração de relatórios completos em formato PDF e Excel.
- Registro detalhado do processamento em arquivos de log.
- Envio automatizado de e-mails personalizados utilizando modelos HTML.

## Demonstração da Aplicação

Para executar o projeto, basta seguir os passos descritos na seção [Como Acessar o Projeto](#como-acessar-o-projeto). A aplicação gera relatórios e envia e-mails automaticamente conforme os dados fornecidos.

## Como Acessar o Projeto

1. Clone este repositório em sua máquina local.
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   ```
2. Instale as dependências necessárias utilizando `pip`.
   ```bash
   pip install -r requirements.txt
   ```
3. Configure a senha de app para o Gmail para habilitar o envio de e-mails automatizados. Consulte o guia oficial do Google para criar a senha: [Senha de App do Gmail](https://support.google.com/accounts/answer/185833?hl=pt-br).
4. Execute o arquivo `main.py` para iniciar o processamento.
   ```bash
   python main.py
   ```

## Tecnologias Utilizadas

- **Python 3.8+**
- **Pandas** para manipulação de dados.
- **OpenPyXL** para trabalhar com arquivos Excel.
- **Smtplib** para envio de e-mails.
- **Jinja2** para renderização de modelos HTML.

## Configuração Inicial

1. **Arquivo `pass.txt`:** Contém a senha de app do Gmail necessária para o envio de e-mails. Certifique-se de que este arquivo está no mesmo diretório que o `main.py`.
2. **Arquivo `email_modelo.html`:** Contém o modelo de e-mail utilizado para envio.
3. Certifique-se de que todos os arquivos necessários (listados na próxima seção) estão corretamente configurados.

## Estrutura de Arquivos

```plaintext
├── ceps_lista_30.csv            # Arquivo de entrada com a lista de CEPs a processar
├── dados_ceps_completos.xlsx    # Arquivo Excel com os dados completos dos CEPs
├── email_modelo.html            # Modelo HTML para envio de e-mails
├── main.py                      # Script principal do projeto
├── pass.txt                     # Arquivo contendo a senha de app do Gmail
├── processamento.log            # Arquivo de log gerado durante o processamento
├── relatorio.pdf                # Relatório final gerado pelo script
```

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

