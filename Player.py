# Player.py
import pygame, random, threading, os, time

class Tocador:
    def __init__(self, playlists=None, playlist_atual=None, musica_atual=None, verificador_mudo=False, indice_musica_atual=0):
        self._playlist = playlists
        self._musica_atual = musica_atual
        self._playlist_atual = playlist_atual
        self._verificador_mudo = verificador_mudo
        self._indice_musica_atual = indice_musica_atual

    def limpar_tela(self):
        os.system('clear' if os.name == 'posix' else 'CLS')

    def timer(self, segundos):
        time.sleep(segundos)

    def printar_playlists(self):
        self.limpar_tela()
        for i in range(len(self._playlist)):
            print(f" * Playlist [{i}]: {self._playlist[i]} \n")

    def selecionar_playlist(self):
        user_input_p = int(input("Selecione o número da playlist: "))
        self._playlist_atual = self._playlist[user_input_p]
        self.tocar_musica()

    def verificador_musica(self):
        while True:
            if not pygame.mixer.music.get_busy() and not self._verificador_mudo:
                if self._indice_musica_atual < len(self._playlist_atual) - 1:
                    self._indice_musica_atual += 1
                else:
                    self._indice_musica_atual = 0
                self.tocar_musica()
            self.timer(1)

    def tocar_musica(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(f"music/{self._playlist_atual[self._indice_musica_atual]}")
        self._musica_atual = self._playlist_atual[self._indice_musica_atual]
        pygame.mixer.music.play()

    def funcoes(self):
        while True:
            background_thread = threading.Thread(target=self.verificador_musica)                        # Uso de threading para avaliar se está tocando algo mesmo com o input pedindo valores
            background_thread.daemon = True
            background_thread.start()

            self.limpar_tela()
            print(f"""Current Playing: {self._musica_atual}\n\nFunções disponiveis:\n* [1] Play{" "*13}* [2] Pause\n* [3] Replay {" "*10}* [4] Loop\n* [5] Próxima{" "*10}* [6] Retornar\n* [7] Aleatório{" "*8}* [8] Escolher Outra Playlist\n* [9] Ver a próxima música\n\n* [0] Sair""")
            user_input = int(input("\nDigite uma das opções: "))

            if user_input == 0:
                self._verificador_mudo = True
                pygame.mixer.music.stop()
                return

            elif user_input == 1:
                self._verificador_mudo = False
                pygame.mixer.music.unpause()

            elif user_input == 2:
                self._verificador_mudo = True
                pygame.mixer.music.pause()

            elif user_input == 3:
                self._verificador_mudo = False
                pygame.mixer.music.play()

            elif user_input == 4:
                self._verificador_mudo = False
                pygame.mixer.music.play(-1)

            elif user_input == 5:
                self._verificador_mudo = False
                if self._indice_musica_atual < len(self._playlist_atual) - 1:
                    self._indice_musica_atual += 1
                    self.tocar_musica()
                else:
                    self._indice_musica_atual = 0
                    self.tocar_musica()

            elif user_input == 6:
                self._verificador_mudo = False
                if self._indice_musica_atual > 0:
                    self._indice_musica_atual -= 1
                else:
                    self._indice_musica_atual = len(self._playlist_atual) - 1
                self.tocar_musica()

            elif user_input == 7:
                self._verificador_mudo = False
                if len(self._playlist_atual) > 1:
                    while True:
                        numero =  random.randint(0, len(self._playlist_atual) - 1)
                        if numero != self._indice_musica_atual:
                            self._indice_musica_atual = numero
                            break
                self.tocar_musica()

            elif user_input == 8:
                self._verificador_mudo = True
                pygame.mixer.music.stop()
                self._indice_musica_atual = 0
                self.printar_playlists()
                self.selecionar_playlist()
                
            elif user_input == 9:
                self._verificador_mudo = False
                print(f"A próxima música da playlist será: {self._playlist_atual[self._indice_musica_atual+1 if len(self._playlist_atual) > 1 else self._indice_musica_atual]}")
                self.timer(2)

            else:
                print("Inválido!")
                self.timer(1)
            