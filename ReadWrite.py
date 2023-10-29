# ReadWrite.py
class Leitura:
    def __init__(self) -> None:
        self._logins = []
        self._senhas = []

    @property
    def logins(self):
        return self._logins    
    
    @logins.setter
    def logins(self, login):
        self._logins = login

    @property
    def senhas(self):
        return self._senhas
    
    @senhas.setter
    def senhas(self, senha):
        self._senhas = senha

    def extrair_logins(self):
        with open("importantFiles/logins.txt", 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()                                    # Uso da Leitura de Arquivos
            self.logins = [x.replace('\n', '') for x in linhas]
            return self.logins

    def extrair_senhas(self):
        with open("importantFiles/senhas.txt", 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()                                    # Uso da Leitura de Arquivos
            self.senhas = [x.replace('\n', '') for x in linhas]
            return self.senhas


class Escrita(Leitura):                                                     # Uso de herança
    def __init__(self) -> None:
        super().__init__()

    def adicionar_login(self, login):
        with open("logins.txt", 'a', encoding='utf-8') as arquivo:
            arquivo.write('\n'+login)                                       # Uso da Escrita de Arquivos

    def adicionar_senha(self, senha):
        with open("senhas.txt", 'a', encoding='utf-8') as arquivo:
            arquivo.write('\n'+senha)                                       # Uso da Escrita de Arquivos
