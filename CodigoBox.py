import RPi.GPIO as GPIO
from datetime import datetime
import time
import csv

alavanca_esquerda = 11
alavanca_direita = 12

botao_alavanca_esquerda = 13
botao_alavanca_direita = 15

luz_geral = 16
luz_esquerda = 18
luz_direita = 22

recompensa = 29

GPIO.setmode(GPIO.BOARD)

GPIO.setup(botao_alavanca_esquerda, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(botao_alavanca_direita, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(alavanca_esquerda, GPIO.OUT)
GPIO.setup(alavanca_direita, GPIO.OUT)
GPIO.setup(recompensa, GPIO.OUT)
GPIO.setup(luz_geral, GPIO.OUT)
GPIO.setup(luz_esquerda, GPIO.OUT)
GPIO.setup(luz_direita, GPIO.OUT)
GPIO.setup(luz_esquerda, GPIO.OUT)
GPIO.setup(luz_direita, GPIO.OUT)

def ligando_luz_geral():
    GPIO.output(luz_geral, 1)

def desligando_luz_geral():
    GPIO.output(luz_geral, 0)

def ligando_luz_esquerda():
    GPIO.output(luz_esquerda, 1)

def desligando_luz_esquerda():
    GPIO.output(luz_esquerda, 0)

def ligando_luz_direita():
    GPIO.output(luz_direita, 1)

def desligando_luz_direita():
    GPIO.output(luz_direita, 0)

def ligando_alavancas():
    GPIO.output(alavanca_esquerda, 1)
    GPIO.output(alavanca_direita, 1)

def desligando_alavancas():
    GPIO.output(alavanca_esquerda, 0)
    GPIO.output(alavanca_direita, 0)

def liberando_recompensa():
    GPIO.output(recompensa, 1)

def horario_segundos():
    horario = datetime.now()
    hora = horario.hour
    minuto = horario.minute
    segundo = horario.second
    total_segundos = (hora * 60 * 60) + (minuto * 60) + (segundo)
    return total_segundos

def horario_limite_segundos(tempo_limite):
    tempo_stop = tempo_limite * 60
    hora_inicial = horario_segundos()
    hora_final = hora_inicial + tempo_stop
    return hora_final

def pre_configuracao():
    ligando_luz_geral()
    desligando_luz_esquerda()
    desligando_luz_direita()
    ligando_alavancas()

def pos_configuracao():
    desligando_luz_geral()
    desligando_luz_esquerda()
    desligando_luz_direita()
    desligando_alavancas()

def test(identificacao_soinho, alavanca_ativa, tempo_limite):
    ativa1_alavanca_esq = 0
    ativa1_alavanca_dir = 0
    ativa2_alavanca_esq = 0
    ativa1_alavanca_dir = 0
    toques_esquerda = 0
    toques_direita = 0
    acertos = 0
    erros = 0
    
    pre_configuracao()
    
    data_hora_inicial = time.asctime(time.localtime(time.time()))
    hora_final = horario_limite_segundos(tempo_limite)

    while True:

        if (GPIO.input(alavanca_esquerda) == 1) and (alavanca_ativa == 1):
            ativa1_alavanca_esq = ativa1_alavanca_esq + 1
            acertos = acertos + 1
            toques_esquerda = toques_esquerda + 1
        elif (GPIO.input(alavanca_direita) == 1) and (alavanca_ativa == 1):
            ativa1_alavanca_dir =  ativa1_alavanca_dir + 1 
            erros = erros + 1
            toques_direita = toques_direita + 1
        elif (GPIO.input(alavanca_esquerda) == 1) and (alavanca_ativa == 2):
            ativa2_alavanca_esq = ativa2_alavanca_esq + 1 
            erros = erros + 1
            toques_esquerda = toques_esquerda + 1
        elif (GPIO.input(alavanca_direita) == 1) and (alavanca_ativa == 2):
            ativa2_alavanca_dir = ativa2_alavanca_dir + 1 
            acertos = acertos + 1
            toques_direita = toques_direita + 1
        
        hora_atual = horario_segundos()
        if hora_atual == hora_final:
            data_hora_final = time.asctime(time.localtime(time.time()))
            print("\n------------------------------------------- FEEDBACK -----------------------------------------------------")
            print("IDENTIFICACAO SOINHO: ", identificacao_soinho, " ALAVANCA ATIVA: ", alavanca_ativa)
            print("TOQUES ESQUERDA: ", toques_esquerda, " TOQUES DIREITA: ", toques_direita, " TOTAL ACERTOS: ", acertos, " TOTAL ERROS: ", erros)
            print("DATA E HORA INICIAIS: ", data_hora_inicial, " DATA E HORA FINAIS: ", data_hora_final)
            print("----------------------------------------------------------------------------------------------------------\n")
            pos_configuracao()
            break

def omission(identificacao_soinho, alavanca_ativa, tempo_limite):
    ativa1_alavanca_esq = 0
    ativa1_alavanca_dir = 0
    ativa2_alavanca_esq = 0
    ativa2_alavanca_dir = 0
    toques_esquerda = 0
    toques_direita = 0
    acertos = 0
    erros = 0
    recompensas_ganhas = 0
    controle_tempo = 0

    pre_configuracao()
    data_hora_inicial = time.asctime(time.localtime(time.time()))
    hora_final = horario_limite_segundos(tempo_limite)

    while True:

        if (controle_tempo == 0):
            tempo_final = horario_limite_segundos(0.5)
            controle_tempo = 1
         
        if (GPIO.input(alavanca_esquerda) == 1) and (alavanca_ativa == 1):
            ativa1_alavanca_esq = ativa1_alavanca_esq + 1
            acertos = acertos + 1
            toques_esquerda = toques_esquerda + 1
            tempo_final = horario_limite_segundos(0.5)
 
        elif (GPIO.input(alavanca_direita) == 1) and (alavanca_ativa == 1):
            ativa1_alavanca_dir =  ativa1_alavanca_dir + 1 
            erros = erros + 1
            toques_direita = toques_direita + 1
            tempo_final = horario_limite_segundos(0.5)

        elif (GPIO.input(alavanca_esquerda) == 1) and (alavanca_ativa == 2):
            ativa2_alavanca_esq = ativa2_alavanca_esq + 1 
            erros = erros + 1
            toques_esquerda = toques_esquerda + 1
            tempo_final = horario_limite_segundos(0.5)

        elif (GPIO.input(alavanca_direita) == 1) and (alavanca_ativa == 2):
            ativa2_alavanca_dir = ativa2_alavanca_dir + 1 
            acertos = acertos + 1
            toques_direita = toques_direita + 1
            tempo_final = horario_limite_segundos(0.5)

        if horario_segundos() == tempo_final:
            liberando_recompensa()
            recompensas_ganhas = recompensas_ganhas + 1
            controle_tempo = 0

        hora_atual = horario_segundos()

        if hora_atual == hora_final:
            data_hora_final = time.asctime(time.localtime(time.time()))
            print("\n------------------------------------------- FEEDBACK -----------------------------------------------------")
            print("IDENTIFICACAO SOINHO: ", identificacao_soinho, " ALAVANCA ATIVA: ", alavanca_ativa)
            print("TOQUES ESQUERDA: ", toques_esquerda, " TOQUES DIREITA: ", toques_direita, " TOTAL ACERTOS: ", acertos, " TOTAL ERROS: ", erros, " RECOMPENSAS GANHAS: ", recompensas_ganhas)
            print("DATA E HORA INICIAIS: ", data_hora_inicial, " DATA E HORA FINAIS: ", data_hora_final)
            print("----------------------------------------------------------------------------------------------------------\n")
            pos_configuracao()
            break 

def main():
    print("\n----------------------------------------INFORMACOES PREVIAS-----------------------------------------------")
    identificacao_soinho = str(input("DIGITE O CODIGO DE IDENTIFICACAO DO SOINHO: "))

    while True:
        alavanca_ativa = int(input("DIGITE QUAL ALAVANCA ESTA ATIVA -> 1 - ESQUERDA | 2 - DIREITA: "))
        if alavanca_ativa == 1 or alavanca_ativa == 2:
            break

    while True:
        tempo_limite =  float(input("DIGITE O TEMPO LIMITE (EM MINUTOS): "))
        if tempo_limite > 0:
            break

    while True:
        print("\n----------------------------------------MENU DE OPCOES----------------------------------------------------")
        print("0 - SAIR")
        print("3 - TEST")
        print("4 - OMISSION")
        print("----------------------------------------------------------------------------------------------------------\n")
        opcao = int(input("DIGITE A SUA OPCAO: "))
        
        if opcao == 0:
            print("SAINDO...")
            break
        elif opcao == 3:
            test(identificacao_soinho, alavanca_ativa, tempo_limite)
        elif opcao == 4:
            omission(identificacao_soinho, alavanca_ativa, tempo_limite)

main()