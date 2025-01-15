"""
Projeto: Processamento de Dados de CEP
Autor: Juliano Chagas de Lima
Data: 14/01/2024
Versão: 1.0
Descrição: Este script processa dados de CEPs para gerar relatórios personalizados e enviar e-mails automatizados.
Uso: python main.py
Dependências: pandas, openpyxl, smtplib, jinja2
Licença: MIT

Este projeto tem como objetivo processar dados de CEPs para gerar relatórios personalizados e enviar e-mails automatizados com base em informações extraídas de arquivos CSV e Excel. Ele é especialmente útil para automatizar tarefas de comunicação em massa baseadas em localizações geográficas.

Status do Projeto: Em desenvolvimento

Funcionalidades:
- Processamento de listas de CEPs a partir de arquivos CSV.
- Geração de relatórios completos em formato PDF e Excel.
- Registro detalhado do processamento em arquivos de log.
- Envio automatizado de e-mails personalizados utilizando modelos HTML.

Configuração Inicial:
1. **Arquivo `pass.txt`:** Contém a senha de app do Gmail necessária para o envio de e-mails. Certifique-se de que este arquivo está no mesmo diretório que o `main.py`.
2. **Arquivo `email_modelo.html`:** Contém o modelo de e-mail utilizado para envio.
3. Certifique-se de que todos os arquivos necessários estão corretamente configurados.

Estrutura de Arquivos:
├── ceps_lista_30.csv            # Arquivo de entrada com a lista de CEPs a processar
├── dados_ceps_completos.xlsx    # Arquivo Excel com os dados completos dos CEPs
├── email_modelo.html            # Modelo HTML para envio de e-mails
├── main.py                      # Script principal do projeto
├── pass.txt                     # Arquivo contendo a senha de app do Gmail
├── processamento.log            # Arquivo de log gerado durante o processamento
├── relatorio.pdf                # Relatório final gerado pelo script

Contato: julianochagaslima@gmail.com
"""

import requests
import pandas as pd
import logging
from email.message import EmailMessage
import smtplib
import ssl
from pathlib import Path
import os
from fpdf import FPDF

# Configuração do Logger
def setup_logger(log_file):
    logging.basicConfig(filename=log_file, level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger()

class CEPService:
    def __init__(self, logger):
        self.logger = logger

    def consultar_cep_viacep(self, cep):
        """Consulta o CEP na API ViaCEP."""
        link = f'https://viacep.com.br/ws/{cep}/json/'
        return self._realizar_consulta(link, cep)

    def consultar_cep_opencep(self, cep):
        """Consulta o CEP na API OpenCEP."""
        link = f'https://api.opencep.com/v1/{cep}'
        return self._realizar_consulta(link, cep)

    def _realizar_consulta(self, link, cep):
        """Realiza a consulta em uma API específica."""
        try:
            requisicao = requests.get(link, timeout=10)
            requisicao.raise_for_status()
            resposta = requisicao.json()

            # Adiciona um controle específico para erros nas respostas das APIs
            if 'erro' in resposta or not resposta.get('cep'):
                raise ValueError(f"CEP {cep} não encontrado na API.")
            resposta['status'] = 'Sucesso'
            return resposta
        except Exception as e:
            self.logger.error(f"Erro ao consultar API para o CEP {cep}: {e}")
            return {'cep': cep, 'status': 'Erro'}

    def consultar_cep(self, cep):
        """Realiza a consulta no ViaCEP e, em caso de erro, no OpenCEP."""
        cep = cep.replace("-", "").strip()  # Remove traços e espaços extras
        self.logger.info(f"Tentando consulta no ViaCEP para o CEP {cep}")
        resposta = self.consultar_cep_viacep(cep)

        if resposta['status'] == 'Erro':
            self.logger.info(f"Falha no ViaCEP. Tentando consulta no OpenCEP para o CEP {cep}")
            resposta = self.consultar_cep_opencep(cep)

        return resposta

class CEPProcessor:
    def __init__(self, cep_service, logger):
        self.cep_service = cep_service
        self.logger = logger

    def process(self, input_file, output_file):
        try:
            df = pd.read_csv(input_file)
            if 'CEP' not in df.columns:
                raise ValueError("O arquivo CSV não contém uma coluna 'CEP'.")

            dados_completos = []

            for cep in df['CEP']:
                self.logger.info(f"Consultando CEP: {cep}")
                print(f"Consultando CEP: {cep}")
                dados = self.cep_service.consultar_cep(str(cep))
                dados_completos.append(dados)

            df_resultados = pd.DataFrame(dados_completos)
            df_resultados['EMAIL'] = ""  # Inicializa a coluna EMAIL
            df_resultados.to_excel(output_file, index=False)
            self.logger.info(f"Processamento concluído. Dados salvos em {output_file}")
            print(f"Processamento concluído. Dados salvos em {output_file}")
            return df_resultados

        except FileNotFoundError:
            self.logger.error(f"Erro: Arquivo {input_file} não encontrado.")
            print(f"Erro: Não foi possível encontrar o arquivo {input_file}. Verifique o caminho e tente novamente.")
        except ValueError as e:
            self.logger.error(f"Erro no arquivo de entrada: {e}")
            print(f"Erro: {e}")
        except Exception as e:
            self.logger.error(f"Erro inesperado: {e}")
            print(f"Erro inesperado: {e}")
        finally:
            self.logger.info("Processamento de CEPs finalizado.")
            print("Processamento de CEPs finalizado.")

class EmailSender:
    def __init__(self, logger):
        self.logger = logger

    def send_emails(self, dados_ceps, email_senha, corpo_template, email_de, output_file):
        safe = ssl.create_default_context()

        for index, cep in dados_ceps.iterrows():
            if cep['status'] == 'Sucesso':
                try:
                    # Personalizando o corpo do e-mail
                    corpo = (corpo_template
                             .replace('${cep}', str(cep['cep']))
                             .replace('${logradouro}', str(cep['logradouro']))
                             .replace('${bairro}', str(cep['bairro']))
                             .replace('${cidade}', str(cep['localidade']))  # Corrigido para 'localidade'
                             .replace('${estado}', str(cep['uf'])))  # Corrigido para 'uf'

                    # Configurando o e-mail
                    msg = EmailMessage()
                    msg['From'] = email_de
                    msg['To'] = 'seu_gmail_que_vai_receber_aqui@hotmail.com'
                    msg['Subject'] = f"Informações para o CEP {cep['cep']}"
                    msg.set_content(corpo, subtype='html')

                    # Enviando o e-mail
                    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
                        smtp.starttls(context=safe)
                        smtp.login(email_de, email_senha)
                        smtp.send_message(msg)  # Usando send_message ao invés de sendmail
                    
                    success_message = f"E-mail enviado com sucesso para {msg['To']} (CEP: {cep['cep']})"
                    print(success_message)
                    self.logger.info(success_message)
                    
                    # Atualiza a coluna EMAIL com Sucesso
                    dados_ceps.at[index, 'EMAIL'] = 'Sucesso'
                    
                except Exception as e:
                    error_message = f"Erro ao enviar e-mail para {msg['To']} (CEP: {cep['cep']}): {e}"
                    print(error_message)
                    self.logger.error(error_message)
                    # Atualiza a coluna EMAIL com Erro
                    dados_ceps.at[index, 'EMAIL'] = 'Erro'
                finally:
                    self.logger.info("Operação de envio de e-mail finalizada.")
            else:
                error_message = f"E-mail para o CEP {cep['cep']} não foi enviado pois ocorreu um erro nos dados."
                print(error_message)
                self.logger.info(error_message)
                # Atualiza a coluna EMAIL com Erro
                dados_ceps.at[index, 'EMAIL'] = 'Erro'
        
        # Salva o DataFrame atualizado com a coluna EMAIL no arquivo de saída
        dados_ceps.to_excel(output_file, index=False)

def gerar_relatorio_pdf(dados_ceps, output_pdf):
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 12)
            self.cell(0, 10, "Relatório de Processamento de CEPs", border=0, ln=1, align="C")

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, f"Página {self.page_no()}", align="C")

    # Criação do PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Dados do CSV
    for index, row in dados_ceps.iterrows():
        pdf.cell(0, 10, f"CEP: {row['cep']}, STATUS: {row['status']}, EMAIL: {row['EMAIL']}", ln=1)

    # Adiciona a soma dos sucessos e erros
    total_consultas_sucesso = (dados_ceps['status'] == 'Sucesso').sum()
    total_consultas_erro = (dados_ceps['status'] == 'Erro').sum()
    total_emails_sucesso = (dados_ceps['EMAIL'] == 'Sucesso').sum()
    total_emails_erro = (dados_ceps['EMAIL'] == 'Erro').sum()

    pdf.add_page()
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Resumo do Processamento", ln=1)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Consultas na API ViaCEP - Sucesso: {total_consultas_sucesso}, Erros: {total_consultas_erro}", ln=1)
    pdf.cell(0, 10, f"Envios de E-mails - Sucesso: {total_emails_sucesso}, Erros: {total_emails_erro}", ln=1)

    # Salva o PDF
    pdf.output(output_pdf)
    print(f"Relatório gerado e salvo em {output_pdf}")

def main():
    """Função principal de execução."""
    base_path = Path(os.getcwd())  # Obtendo o diretório de trabalho atual
    config = {
        'input_file': base_path / 'ceps_lista_30.csv',
        'output_file': base_path / 'dados_ceps_completos.xlsx',
        'log_file': base_path / 'processamento.log',
        'pass_file': base_path / 'pass.txt',
        'email_template': base_path / 'email_modelo.html',
        'output_pdf': base_path / 'relatorio.pdf'
    }

    try:
        # Inicializa o logger
        logger = setup_logger(config['log_file'])
        
        # Inicializa os serviços
        cep_service = CEPService(logger)
        processor = CEPProcessor(cep_service, logger)

        # Processa os CEPs
        result_df = processor.process(
            config['input_file'],
            config['output_file']
        )

        # Verifica se a planilha contém dados
        if result_df.empty:
            logger.info("A planilha está vazia. Nenhum e-mail será enviado.")
            print("A planilha está vazia. Nenhum e-mail será enviado. Encerrando o script.")
            return

        # Inicializa e executa o envio de e-mails
        email_sender = EmailSender(logger)

        # Leitura da senha do e-mail a partir de um arquivo
        with open(config['pass_file'], 'r') as file:
            email_senha = file.read().strip()

        # Configurações do e-mail de envio
        email_de = 'seu_GMAIL_aqui@gmail.com'

        # Leitura do corpo do e-mail a partir de um arquivo
        with open(config['email_template'], 'r', encoding='utf-8') as file:
            corpo_template = file.read()

        # Envia os e-mails com as informações dos CEPs
        email_sender.send_emails(result_df, email_senha, corpo_template, email_de, config['output_file'])
        
        # Gera o relatório em PDF
        gerar_relatorio_pdf(result_df, config['output_pdf'])
        
        logger.info("Processo concluído com sucesso")
        print("""
                As seguintes etapas foram realizadas:
                
                1 - Processamentos dos CEPs
                2 - Envios de E-mails
                3 - Relatórios em PDF gerado
                
                Encerrando o robô... bye... bye...
                """)


    except Exception as e:
        logger.error(f"Processo falhou: {str(e)}")
        raise

if __name__ == "__main__":
    main()






