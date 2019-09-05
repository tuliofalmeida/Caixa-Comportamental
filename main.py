from Box import Box
import RPi.GPIO as GPIO
import Modules
from datetime import datetime
from random import randint
import time
import csv

caixa = Box(1, 200)

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

def test(identificacao_soinho, alavanca_ativa, tempo_limite):
    toques_esquerda = 0
    toques_direita = 0
    acertos = 0
    erros = 0

    caixa.startSession()
    
    data_hora_inicial = time.asctime(time.localtime(time.time()))
    hora_final = horario_limite_segundos(tempo_limite)

    while True:

        if caixa.getLeftLeverResponse() and (alavanca_ativa == 1):
            toques_esquerda += 1
            acertos += 1
        elif caixa.getRightLeverResponse() and (alavanca_ativa == 1):
            erros += 1
            toques_direita += 1
        elif caixa.getLeftLeverResponse() and (alavanca_ativa == 2):
            erros += 1
            toques_esquerda += 1
        elif caixa.getRightLeverResponse() and (alavanca_ativa == 2):
            acertos += 1
            toques_direita += 1
        
        hora_atual = horario_segundos()

        if hora_atual == hora_final:
            data_hora_final = time.asctime(time.localtime(time.time()))
            caixa.sendReward()
            print("\n------------------------------------------- FEEDBACK -----------------------------------------------------")
            print("IDENTIFICACAO SOINHO: ", identificacao_soinho, " ALAVANCA ATIVA: ", alavanca_ativa)
            print("TOQUES ESQUERDA: ", caixa.getLeftLeverResponse() , " TOQUES DIREITA: ", caixa.getRightLeverResponse() , " TOTAL ACERTOS: ", acertos, " TOTAL ERROS: ", erros)
            print("DATA E HORA INICIAIS: ", data_hora_inicial, " DATA E HORA FINAIS: ", data_hora_final)
            print("----------------------------------------------------------------------------------------------------------\n")
            caixa.stopSession()
            caixa.rightPalet = 0
            caixa.leftPalet = 0
            break

def omission(identificacao_soinho, alavanca_ativa, tempo_limite, omission_or_yoked):
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
            if(omission_or_yoked == 1):
                tempo_final = horario_limite_segundos(0.5)
            elif(omission_or_yoked == 2):
                tempo_random = randint(0.25, 0.75)
                tempo_final = horario_limite_segundos(tempo_random)
            controle_tempo = 1
         
        if (GPIO.input(alavanca_esquerda) == 1) and (alavanca_ativa == 1):
            ativa1_alavanca_esq = ativa1_alavanca_esq + 1
            acertos = acertos + 1
            toques_esquerda = toques_esquerda + 1
            if(omission_or_yoked == 1):
                tempo_final = horario_limite_segundos(0.5)
 
        elif (GPIO.input(alavanca_direita) == 1) and (alavanca_ativa == 1):
            ativa1_alavanca_dir =  ativa1_alavanca_dir + 1 
            erros = erros + 1
            toques_direita = toques_direita + 1
            if(omission_or_yoked == 1):
                tempo_final = horario_limite_segundos(0.5)

        elif (GPIO.input(alavanca_esquerda) == 1) and (alavanca_ativa == 2):
            ativa2_alavanca_esq = ativa2_alavanca_esq + 1 
            erros = erros + 1
            toques_esquerda = toques_esquerda + 1
            if(omission_or_yoked == 1):
                tempo_final = horario_limite_segundos(0.5)

        elif (GPIO.input(alavanca_direita) == 1) and (alavanca_ativa == 2):
            ativa2_alavanca_dir = ativa2_alavanca_dir + 1 
            acertos = acertos + 1
            toques_direita = toques_direita + 1
            if(omission_or_yoked == 1):
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
        print("5 - YOKED")
        print("----------------------------------------------------------------------------------------------------------\n")
        opcao = int(input("DIGITE A SUA OPCAO: "))
        
        if opcao == 0:
            print("SAINDO...")
            break
        elif opcao == 3:
            test(identificacao_soinho, alavanca_ativa, tempo_limite)
        elif opcao == 4:
            omission(identificacao_soinho, alavanca_ativa, tempo_limite, 1)
        elif opcao == 5:
            omission(identificacao_soinho, alavanca_ativa, tempo_limite, 2)

def rightInterrupt(arg):
    caixa.setRightLeverResponse()

def leftInterrupt(arg):
    caixa.setLeftLeverResponse()

GPIO.add_event_detect(Modules.Box[caixa.bx, 0], GPIO.FALLING, callback=rightInterrupt)
GPIO.add_event_detect(Modules.Box[caixa.bx, 1], GPIO.FALLING, callback=leftInterrupt)

main()