import subprocess
import time

# Configurações
tempo_limite_minutos = 120
segundos_totais = tempo_limite_minutos * 60
inicio_geral = time.time()

print(f"Iniciando loop de execução por {tempo_limite_minutos} minutos...")

while (time.time() - inicio_geral) < segundos_totais:
    print(f"\n--- Iniciando execução: {time.strftime('%H:%M:%S')} ---")
    
    # Executa o seu comando
    # O script espera o comando terminar para começar a próxima repetição
    subprocess.run(["python", "-m", "teste_treinamento"])
    
    tempo_restante = segundos_totais - (time.time() - inicio_geral)
    
    if tempo_restante > 0:
        minutos_faltando = int(tempo_restante / 60)
        print(f"Execução finalizada. Tempo restante: {minutos_faltando} min.")
    else:
        print("Tempo esgotado!")

print(f"Período de {tempo_limite_minutos} minutos concluído.")