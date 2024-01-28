import os
import platform
import json
import datetime
import time

arquivo_dados = "dados_financeiros.json"

def limpar_tela():
    # Verifica o sistema operacional
    if platform.system() == "Windows":
        os.system('cls')  # Para Windows
    else:
        os.system('clear')  # Para Linux e MacOS
def obter_timestamp_atual():
    """
    Retorna o timestamp atual.
    
    """
    return int(time.time())
def converter_data_para_timestamp(data_str):
    """
    Converte uma data no formato 'DD-MM-AAAA' para timestamp.
    
    """
    formato_data = '%d-%m-%Y'
    try:
        data_obj = datetime.datetime.strptime(data_str, formato_data)
        timestamp = int(data_obj.timestamp())
        return timestamp
    except ValueError:
        print("Formato de data inválido. Use 'DD-MM-AAAA'.")
        return None
def ler_dados():
    """Lê os dados do arquivo JSON e retorna a lista de registros."""
    try:
        with open(arquivo_dados, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

def escrever_dados(dados):
    """Escreve a lista de registros atualizada no arquivo JSON."""
    with open(arquivo_dados, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

def cadastrar():
    registros = ler_dados()
    ultimo_id = registros[-1]['id'] if registros else 0  # Obtém o último ID, se houver registros

    print("Cadastro de Transações")
    print("-" * 50)

    tipo = input("Tipo de transação (Receita/Despesa/Investimento): ").strip().capitalize()
    if tipo not in ['Receita', 'Despesa', 'Investimento']:
        print("Tipo inválido.")
        return

    valor = input("Valor da transação: ").strip()
    try:
        valor = float(valor)
    except ValueError:
        print("Valor inválido.")
        return

    if tipo == 'Investimento':
        data_investimento_str = input("Digite a data do investimento (DD-MM-AAAA): ")
        timestamp_investimento = converter_data_para_timestamp(data_investimento_str)
        if timestamp_investimento is None:  # Verifica se a conversão foi bem-sucedida
            return
    else:
        timestamp_investimento = None  # Não aplicável para outros tipos

    timestamp_registro = obter_timestamp_atual()
    timestamp_atualizacao = timestamp_registro  # Inicialmente, igual ao timestamp de registro

    # Constrói o registro
    registro = {
        "id": ultimo_id + 1,
        "tipo": tipo,
        "valor": valor,
        "data_investimento": data_investimento_str if tipo == 'Investimento' else None,
        "timestamp_registro": timestamp_registro,
        "timestamp_atualizacao": timestamp_atualizacao,
        "montante": None  # Opcional, depende da sua lógica para calcular montantes
    }

    registros.append(registro)
    escrever_dados(registros)
    print("Transação cadastrada com sucesso!")

def inicializar_arquivo():
    try:
        with open(arquivo_dados, 'r') as arquivo:
            # Verifica se o arquivo está vazio
            if arquivo.read().strip() == "":
                raise FileNotFoundError
    except FileNotFoundError:
        resposta = input(f"O arquivo {arquivo_dados} não foi encontrado ou está vazio. Deseja criar um novo arquivo? (s/n): ").strip().lower()
        if resposta == 's':
            with open(arquivo_dados, 'w') as arquivo:
                json.dump([], arquivo)
            print(f"Arquivo {arquivo_dados} criado com sucesso.")
        else:
            print("Operação cancelada. O arquivo não foi criado.")
def iniciar():
    while True:
        limpar_tela() 

        print("\033[1;34m" + "-" * 50)  
        print("\033[1;33mSistema de Controle Financeiro\033[0m")  
        print("\033[1;34m" + "-" * 50 + "\033[0m")  

        print("\nEscolha uma opção e pressione Enter:")
        print("\033[1;32m1 - Cadastrar")
        print("2 - Consultar")
        print("3 - Atualizar")
        print("4 - Deletar")
        print("5 - Sair\033[0m")

        escolha = input("\033[1;37mSua escolha: \033[0m")

        if escolha in ['1', '2', '3', '4', '5']:
            return escolha
        else:
            print("\033[1;31mOpção inválida. Tente novamente.\033[0m")
            input("\033[1;37mPressione Enter para continuar...\033[0m")
def consultar():
    pass
def atualizar():
    pass
def deletar():
    pass
def main():
    while True:
        inicializar_arquivo()
        escolha = iniciar()
        if escolha == '1':
            cadastrar()
        elif escolha == '2':
            consultar()
        elif escolha == '3':
            atualizar()
        elif escolha == '4':
            deletar()
        elif escolha == '5':
            print("Saindo do sistema...")
            break
if __name__ == '__main__':
    main()