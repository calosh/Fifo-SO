from django.shortcuts import render
import os
from time import sleep

# Create your views here.
#from __future__ import division
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ord_insercion(tiempo_llegada, rafaga_cpu, proceso):
    for indice in range(1, len(tiempo_llegada)):
        valor = tiempo_llegada[indice]
        i = indice - 1
        while i>=0:
            if valor < tiempo_llegada[i]:
                tiempo_llegada[i], tiempo_llegada[i+1] = tiempo_llegada[i+1], tiempo_llegada[i]
                rafaga_cpu[i], rafaga_cpu[i + 1] = rafaga_cpu[i + 1], rafaga_cpu[i]
                proceso[i], proceso[i + 1] = proceso[i + 1], proceso[i]
                i -=1
            elif valor == tiempo_llegada[i] and rafaga_cpu[indice]>rafaga_cpu[i]:
                tiempo_llegada[i], tiempo_llegada[i + 1] = tiempo_llegada[i + 1], tiempo_llegada[i]
                rafaga_cpu[i], rafaga_cpu[i + 1] = rafaga_cpu[i + 1], rafaga_cpu[i]
                proceso[i], proceso[i + 1] = proceso[i + 1], proceso[i]
            else:
                break

def index(request):
    if request.POST:
        procesos = request.POST['procesos']
        tiempo_llegada = request.POST['tll']
        rafaga_cpu = request.POST['rcpu']

        procesos = procesos.split(',')
        tiempo_llegada = tiempo_llegada.split(',')
        rafaga_cpu = rafaga_cpu.split(',')

        try:
            tiempo_llegada = map(float, tiempo_llegada)
            rafaga_cpu = map(float, rafaga_cpu)
        except Exception, e:
            return render(request, 'index.html')
  
        
        
        ord_insercion(tiempo_llegada, rafaga_cpu,procesos)

        tiempo_espera = []
        tiempo_retorno = []


        tiempo1 = tiempo_llegada[0]
        tiempo2 = tiempo_llegada[0]
        sum1 = 0
        sum2 = 0
        te = 0 # Tiempo de espera
        print("PRC\t\tTLL\t\tRCPU\tTE\t\tTR" )

        for i in range(0, len(tiempo_llegada)):
            tiempo1+=rafaga_cpu[i]
            sum1+=tiempo1

            te = tiempo2-tiempo_llegada[i]
            tiempo2 = tiempo2+rafaga_cpu[i]
            sum2+=te

            tiempo_espera.append(te)
            tiempo_retorno.append(tiempo1)

            print("%s\t\t%d\t\t%d\t\t%d\t\t%d" %(procesos[i], tiempo_llegada[i],rafaga_cpu[i],te,tiempo1))


        ttl = sum2/len(tiempo_llegada)
        tr = sum1/len(tiempo_llegada)
        print('Tiempo de espera: %f' %ttl)
        print('Tiempo de retorno: %f' %tr)



        print tiempo_espera
        print tiempo_retorno


        print "Lista para graficar"
        x = []
        y = []

        for i in range(len(tiempo_llegada)):
            x.append(tiempo_llegada[i]+tiempo_espera[i])
            y.append(rafaga_cpu[i])


        print x
        print y

        aux_x = []
        for i in range(len(x)):

            aux_x.append(str(x[i])+"\n"+str(procesos[i]))
        
        print aux_x
        # Barras
        plt.bar(x,y, label='Linea 1', color='b')
        plt.ylabel('Rafaga de CPU')
        plt.xlabel('Tiempo')
        plt.xticks(x,aux_x)
        plt.yticks(y)
        plt.savefig(os.path.join(BASE_DIR,'static/myfig'))
        plt.close()
   
        return render(request, 'resultados.html',{'procesos':procesos, 'rafaga_cpu':rafaga_cpu,'tiempo_llegada':tiempo_llegada,
            'tiempo_espera':tiempo_espera,'tiempo_retorno':tiempo_retorno,'ttl':ttl,'tr':tr})
    else:
        return render(request, 'index.html')


def resultados():
    return render(request, 'resultados.html')