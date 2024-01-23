import os
import platform

DATABASE_SISTEMA_FINANCEIRO = {
    'ID' : [],
    'TIPO' : [],
    'VALOR' : [],
    'DATA' : [],

}

def limpar_tela():
    # Verifica o sistema operacional
    if platform.system() == "Windows":
        os.system('cls')  # Para Windows
    else:
        os.system('clear')  # Para Linux e MacOS

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



def cadastrar():
        limpar_tela()
        print("\033[1;34m" + "-" * 50)  
        print("\033[1;33mSistema de Controle Financeiro\033[0m")  
        print("\033[1;34m" + "-" * 50 + "\033[0m")
        
        print("\nEscolha uma opção e pressione Enter:")
        print("\033[1;32m1 - Receita")
        print("2 - Despesa")
        print("3 - Investimento")
        print("4 - voltar ao menu\033[0m")
        tipo = input("\033[1;37mSua escolha: \033[0m")

        if tipo in ['1', '2', '3', '4']:
            return tipo
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