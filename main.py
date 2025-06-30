import os

def menu():
    print("Bem-vindo ao Campo Minado Multiplayer!")
    print("1 - Jogar Singleplayer")
    print("2 - Hostear Jogo Online")
    print("3 - Entrar em Jogo Online")
    escolha = input("Escolha uma opção: ")

    if escolha == "1":
        os.system("python minesweepergui.py")
    elif escolha == "2":
        os.system("python servidor.py")
    elif escolha == "3":
        os.system("python cliente_pygame.py")
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    menu()
