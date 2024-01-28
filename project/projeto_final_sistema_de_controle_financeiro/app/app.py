import os
import platform
import json
import datetime


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
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
    """

    Lê os dados do arquivo JSON e retorna a lista de registros.
    
    """
    try:
        with open(arquivo_dados, 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

def escrever_dados(dados):
    """
    Escreve a lista de registros atualizada no arquivo JSON.
    
    """
    with open(arquivo_dados, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)
def atualizar_montantes_investimento():
    registros = ler_dados()
    data_atual = datetime.datetime.now()
    houve_atualizacao = False

    for registro in registros:
        if registro['tipo'] == 'Investimento':
            data_investimento = datetime.datetime.strptime(registro['data_investimento'], '%d-%m-%Y')
            diferenca_dias = (data_atual - data_investimento).days

            # Converte a taxa de juros anual para diária
            taxa_juros_anual = registro['taxa_juros_anual']
            taxa_juros_diaria = (1 + taxa_juros_anual) ** (1 / 365) - 1

            # Recalcula o montante
            montante_atualizado = round(registro['valor'] * ((1 + taxa_juros_diaria) ** diferenca_dias),2)
            registro['montante'] = montante_atualizado

            # Atualiza o timestamp de atualização
            registro['timestamp_atualizacao'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            houve_atualizacao = True

    if houve_atualizacao:
        escrever_dados(registros)
        print("Montantes de investimento atualizados com sucesso para a data atual.")
    else:
        print("Não há registros de investimento para atualizar.")

def cadastrar():
    registros = ler_dados()
    ultimo_id = registros[-1]['id'] if registros else 0  # Obtém o último ID, se houver registros

    print("Cadastro de Transações")
    print("-" * 50)

    tipos_transacao = ["Receita", "Despesa", "Investimento"]
    print("Selecione o tipo de transação:")
    for i, tipo in enumerate(tipos_transacao, start=1):
        print(f"{i} - {tipo}")

    while True:
        escolha_tipo = input("Digite o número correspondente ao tipo ou '0' para voltar: ").strip()

        if escolha_tipo == '0':
            return

        if escolha_tipo.isdigit() and 1 <= int(escolha_tipo) <= len(tipos_transacao):
            tipo = tipos_transacao[int(escolha_tipo) - 1]
            break
        else:
            print("Opção inválida. Tente novamente.")

    valor = float(input("Digite o valor da transação: "))
    data_investimento_str = None
    montante = None

    if tipo == 'Investimento':

        data_investimento_str = input("Digite a data do investimento (DD-MM-AAAA): ")
        data_investimento = datetime.datetime.strptime(data_investimento_str, '%d-%m-%Y')
        data_atual = datetime.datetime.now()

        if data_investimento > data_atual:
            print("Data do investimento não pode ser futura.")
            return 
        

        print("Frequência de capitalização:")
        print("1 - Anual")
        print("2 - Mensal")
        print("3 - Diária")
        freq_capitalizacao = input("Escolha a frequência de capitalização: ").strip()

        taxa_juros = float(input("Digite a taxa de juros (%): ")) / 100

        # Conversão da taxa de juros para base diária
        if freq_capitalizacao == '1':  # Anual
            taxa_juros_anual = taxa_juros
        elif freq_capitalizacao == '2':  # Mensal
            taxa_juros_anual = ((1 + taxa_juros / 100 / 12) ** 12 - 1) * 100
        elif freq_capitalizacao == '3':  # Diária
            taxa_juros_anual = ((1 + taxa_juros / 100 / 365) ** 365 - 1) * 100
        else:
            print("Opção de frequência da taxa de juros inválida.")
            return

        # Calcula o montante usando a fórmula de juros compostos com base no número de dias
        montante = round(valor,2)
    elif tipo == 'Despesa':
        valor = -abs(valor)  # Garante que o valor da despesa seja armazenado como negativo

    # Constrói o registro
    registro = {
        "id": ultimo_id + 1,
        "tipo": tipo,
        "valor": round(valor,2),
        "data_investimento": data_investimento_str,
        "timestamp_registro": obter_timestamp_atual(),
        "timestamp_atualizacao": obter_timestamp_atual(),
        "taxa_juros_anual": taxa_juros_anual if tipo == 'Investimento' else None,
        "montante": montante
    }

    registros.append(registro)
    escrever_dados(registros)

    if tipo == 'Investimento':
        # Cadastra o investimento
        atualizar_montantes_investimento()

    limpar_tela()
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
    registros = ler_dados()
    print("Consulta de Registros")
    print("-" * 50)
    print("Escolha o critério de consulta:")
    print("1 - Por Data")
    print("2 - Por Tipo")
    print("3 - Por Valor")
    escolha = input("Digite o número correspondente ao critério: ").strip()

    resultados = []
    if escolha == '1':
        data_consulta = input("Digite a data (DD-MM-AAAA): ")
        for registro in registros:
            if 'data_investimento' in registro and registro['data_investimento'] == data_consulta:
                resultados.append(registro)
    elif escolha == '2':
        tipo_consulta = input("Digite o tipo (Receita, Despesa, Investimento): ").capitalize()
        resultados = [registro for registro in registros if registro['tipo'] == tipo_consulta]
    elif escolha == '3':
        valor_consulta = float(input("Digite o valor: "))
        resultados = [registro for registro in registros if registro['valor'] == valor_consulta]

    if resultados:
        for resultado in resultados:
            print(resultado)
            input("Pressione Enter para sair")
    else:
        print("Nenhum registro encontrado.")

def atualizar():

    registros = ler_dados()
    print("Atualização de Registro")
    print("-" * 50)
    id_registro = int(input("Digite o ID do registro que deseja atualizar: "))

    registro_encontrado = next((registro for registro in registros if registro['id'] == id_registro), None)
    if registro_encontrado:
        print(f"Tipo atual: {registro_encontrado['tipo']}")
        novo_tipo = input("Digite o novo tipo (Receita, Despesa, Investimento) ou pressione Enter para manter: ").capitalize()
        
        # Se o registro for de investimento e estiver sendo alterado para outro tipo, considere o montante como o valor
        if registro_encontrado['tipo'] == 'Investimento' and novo_tipo and novo_tipo != 'Investimento':
            print(f"Convertendo o montante de investimento ({registro_encontrado['montante']}) para o valor de {novo_tipo}.")
            registro_encontrado['valor'] = registro_encontrado['montante']
            registro_encontrado['montante'] = None  # Limpa o montante, pois não se aplica mais
            registro_encontrado['taxa_juros_anual'] = None  # Limpa a taxa de juros anual
            registro_encontrado['data_investimento'] = None  # Limpa a data do investimento

        # Atualiza o tipo, se fornecido
        if novo_tipo:
            registro_encontrado['tipo'] = novo_tipo

        # Atualiza o valor, se fornecido
        novo_valor = input(f"Valor atual: {registro_encontrado['valor']}. Digite o novo valor ou pressione Enter para manter: ")
        if novo_valor:
            registro_encontrado['valor'] = float(novo_valor)

        # Atualiza outros campos específicos de investimento, se aplicável
        if novo_tipo == 'Investimento':
            # Atualize a taxa de juros anual, data do investimento, etc., conforme necessário
            atualizar_montantes_investimento()

        # Atualiza o timestamp de atualização
        registro_encontrado['timestamp_atualizacao'] = obter_timestamp_atual()
        escrever_dados(registros)
        print("Registro atualizado com sucesso.")
    else:
        print("Registro não encontrado.")
def deletar():
    registros = ler_dados()
    print("Deletar Registro")
    print("-" * 50)
    id_registro = int(input("Digite o ID do registro que deseja deletar: "))

    registro_encontrado = next((registro for registro in registros if registro['id'] == id_registro), None)
    if registro_encontrado:
        registros.remove(registro_encontrado)
        escrever_dados(registros)
        print("Registro deletado com sucesso.")
    else:
        print("Registro não encontrado.")
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