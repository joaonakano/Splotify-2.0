# MenuPlayer.py
from ReadWrite import Leitura, Escrita
from abc import ABC, abstractmethod
from Player import Tocador

# ----------------------------- Auth Classes -----------------------------
class Autenticacao(ABC):
    @abstractmethod
    def autenticar(self, login, lista):
        pass

class AutenticacaoLogin(Autenticacao):                              # Uso de Abstração
    def autenticar(self, user_login, logins):       
        return user_login in logins
    
class AutenticacaoSenha(Autenticacao):                              # Uso de Abstração
    def autenticar(self, user_senha, senhas, indice):
        return str(senhas[indice]) == str(user_senha)
# ----------------------------- End Auth Classes -----------------------------

# ----------------------------- Login / Start -----------------------------
class MusicPlayer:
    def __init__(self, arquivo_de_musicas, playlist_atual=None):
        self._tocador = None
        self._arquivo = arquivo_de_musicas
        self._playlist_atual = playlist_atual
        self._playlists = OrganizadorPlaylist(self._arquivo).ler_arquivo()

    # ----------------------------- Login Screen -----------------------------
    def tela_login(self):
        Tocador().limpar_tela()
        leitura, escrita = Leitura(), Escrita()

        while True:
            print('----------LOGIN----------', '\n* [1] Cadastro', '\n* [2] Entrar\n')
            user_input = int(input("Digite o número da opção: "))
            user_login, user_senha = input("Insira seu login: "), input("Insira sua senha: ")
            
            logins, senhas = leitura.extrair_logins(), leitura.extrair_senhas()

            autentica_login = AutenticacaoLogin().autenticar(user_login, logins)                            # Uso de Polimorfismo

            if user_input == 1:
                if user_login not in logins:
                    escrita.adicionar_login(user_login), escrita.adicionar_senha(user_senha)
                    break
                else:
                    print("\033[1;31;40m\n Usuário já cadastrado!", end="\033[0;37m\n")
                    Tocador().timer(1)
                    Tocador().limpar_tela()

            elif user_input == 2:
                indice = logins.index(user_login)
                autentica_senha = AutenticacaoSenha().autenticar(user_senha, senhas, indice)                # Uso de Polimorfismo

                if autentica_login and autentica_senha:
                    print("\033[1;32m\n Acesso liberado!", end="\033[0;37m\n")
                    Tocador().timer(1)
                    break
                else:
                    print("\033[1;31;40m\n Error!", end="\033[0;37m\n")
                    Tocador().timer(1)
                    self.tela_login()
                    break

            else:
                print("\033[1;31;40m\n Opção errada!", end="\033[0;37m")
    # ----------------------------- End Login Screen -----------------------------
    
    # ----------------------------- Available Playlist Print -----------------------------
    def printar_playlist(self):
        Tocador().limpar_tela()
        for i in range(len(self._playlists)):
            print(f" * Playlist [{i}]: {self._playlists[i]} \n")
    # ----------------------------- End Available Playlist Print -----------------------------

    # ----------------------------- Playlist Selection -----------------------------
    def selecionar_playlist(self):
        self.printar_playlist()
        while True:
            user_input_p = int(input("Selecione o número da playlist: "))
            if 0 <= user_input_p < len(self._playlists):
                break
            else:
                print("Playlist errada!")

        self._playlist_atual = self._playlists[user_input_p]
        self._tocador = Tocador(self._playlists, self._playlist_atual)
        self._tocador.tocar_musica()
    # ----------------------------- End Playlist Selection -----------------------------

    # ----------------------------- Main Menu -----------------------------
    def lancar_menu_inicial(self):
        print("""\033[0;32m
    /$$$$$$            /$$             /$$     /$$  /$$$$$$          
    /$$__  $$          | $$            | $$    |__/ /$$__  $$         
    | $$  \__/  /$$$$$$ | $$  /$$$$$$  /$$$$$$   /$$| $$  \__//$$   /$$
    | $$$$$$  /$$__  $$| $$ /$$__  $$|_  $$_/  | $$| $$$$   | $$  | $$
    \____  $$| $$  \ $$| $$| $$  \ $$  | $$    | $$| $$_/   | $$  | $$
    /$$  \ $$| $$  | $$| $$| $$  | $$  | $$ /$$| $$| $$     | $$  | $$
    | $$$$$$/| $$$$$$$/| $$|  $$$$$$/  |  $$$$/| $$| $$     |  $$$$$$$
    \______/ | $$____/ |__/ \______/    \___/  |__/|__/      \____  $$
            | $$                                            /$$  | $$
            | $$                                           |  $$$$$$/ 
            |__/                                            \______/ 
                        * JEB Productions *""", end="\033[0;37m\n")
        Tocador().timer(1)
        self.tela_login()

        while True:
            Tocador().limpar_tela()
            print("\n╔════════════════════════╗", "\033[1;32m\n           MENU ", "\033[0;37m\n * [1] - Music", "\n * [2] - Lista de Músicas", "\n * [3] - Fechar", "\n╚════════════════════════╝\n")
            user_input = int(input("Escolha uma opção: "))

            if user_input == 1:
                self.selecionar_playlist()
                self._tocador.funcoes()

            elif user_input == 2:
                self.printar_playlist()
                input("Pressione qualquer ENTER para fechar...")

            elif user_input == 3:
                exit()

            else:
                print("Inválido!")
                Tocador().timer(1)
    # ----------------------------- End Main Menu -----------------------------
# ----------------------------- End Login / Start -----------------------------

# ----------------------------- Read Music List -----------------------------
class OrganizadorPlaylist:
    def __init__(self, nome_arquivo):
        self._nome_arquivo = nome_arquivo

    def ler_arquivo(self):
        with open(self._nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas_brutas = arquivo.readlines()
            linhas = [x.replace("\n", "") for x in linhas_brutas]
        self._playlists_compactadas = [linhas[x:x+3] for x in range(0, len(linhas), 3)]
        return self._playlists_compactadas
# ----------------------------- End Read Music List -----------------------------