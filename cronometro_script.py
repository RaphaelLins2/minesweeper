import time

class Cronometro:
    def __init__(self):
        self.inicio = None

    def iniciar(self):
        self.inicio = time.time()

    def tempo_decorrido(self):
        if self.inicio is None:
            return 0.0
        return round(time.time() - self.inicio, 2)

    def mostrar_tempo(self):
        print(f"Tempo decorrido: {self.tempo_decorrido():.2f} segundos")
        
