stock_status={
    1 : [[60, 4], [80, 3], [35, 1]],
    2 : [[12, 4], [45, 2], [25, 2]],
    3 : [[20, 2], [30, 1], [20, 3]],
    4 : [[30, 7], [10, 1]],
    5 : [[25, 2], [10, 10]]
}



# Trasy między półkami: {start point : {end point: [time, steps]}
neighbor_matrix={0 : {1 : [10, 0],
                      2 : [12, 0],
                      3 : [11, 0],
                      4 : [9, 0],
                      5 : [8, 0]},

                1 :  {0 : [10, 0],
                      2 : [11, 20],
                      3 : [15, 30],
                      4 : [22, 25],
                      5 : [12, 8]},

                2 :  {0 : [12, 0],
                      1 : [11, 20],
                      3 : [7, 11],
                      4 : [22, 35],
                      5 : [12, 8]},

                3 :  {0 : [11, 0],
                      1 : [15, 30],
                      2 : [7, 11],
                      4 : [13, 20],
                      5 : [35, 40]},

                4 :  {0 : [9, 0],
                      1 : [22, 35],
                      2 : [23, 32],
                      3 : [13, 20],
                      5 : [16, 25]},

                5 :  {0 : [8, 0],
                      1 : [12, 8],
                      2 : [15, 22],
                      3 : [35, 40],
                      4 : [16, 25]}}


import random
import time

punkty=[1,2,3,4,5]
def generate_path(): #tworzenie ścieżki z noszonymi wagami: [[pułka,waga],[pułka,waga],[pułka,waga]]
    new_path = [] #ścieżka
    weight=0 #przenoszona waga

    stock_status={
        1 : [[60, 4], [80, 3], [35, 1]],
        2 : [[12, 4], [45, 2], [25, 2]],
        3 : [[20, 2], [30, 1], [20, 3]],
        4 : [[30, 7], [10, 1]],
        5 : [[25, 2], [10, 10]]
    }


    punkty=[1,2,3,4,5]
    while True:
        new_point=random.choices(punkty,k=1)[0] #losowanie wierzchołka
        if stock_status[new_point]==[]: #jeśli pułka jest pusta
            punkty.pop(punkty.index(new_point)) #uzuwanie możliwości wybrania punktu
        else:
            weight=weight+stock_status[new_point][0][1] #dodawanie wagi noszonego przedmiotu
            if weight>=30: #jeśli przekraczamy maksymalne normy
                weight=0
                new_point=0
            if new_point!=0:
                stock_status[new_point][0][0]=stock_status[new_point][0][0]-1 #usuwanie przedmiotu z pułki
                new_path.append([new_point, weight]) #point and current weight
                if stock_status[new_point][0][0]<=0: #usuwanie przedmiotu z pułki
                    stock_status[new_point].pop(0)

            else:
                new_path.append([0,0])
        if stock_status=={1: [], 2: [], 3: [], 4: [], 5: []}: #jeśli wszystkie pułki są puste
            break

    return(new_path)

# new_path=generate_path()
# print(new_path)
def steps_time(path): #ilość kroków w ścieżce, czasu przejścia ścieżki (czas nie dotyczy przerw)
    n_steps=0
    s_time=0
    for id, point in enumerate(path[:-1]):
        if path[id][0]!=path[id+1][0]:
            n_steps=n_steps+neighbor_matrix[path[id][0]][path[id+1][0]][1]
            s_time=s_time+neighbor_matrix[path[id][0]][path[id+1][0]][0]
    return {"Liczba kroków:" : n_steps, "Całkowity czas:" : s_time}
# a=steps_time(new_path)

def funkcja_celu(droga, czas):
    max_step=500
    break_time=600
    return czas+(droga//max_step)*break_time


import math

def simulated_annealing( temperatura_poczatkowa, temperatura_koncowa, liczba_iteracji):
    trasa_aktualna = generate_path()
    aktualna=steps_time(trasa_aktualna)['Liczba kroków:']
    temperatura = temperatura_poczatkowa
    best_score=999999
    # print(aktualna)

    
    for iteracja in range(liczba_iteracji):
        trasa_sasiada = generate_path()
        new=steps_time(trasa_sasiada)#['Liczba kroków:']

        delta_dlugosc = funkcja_celu(new['Liczba kroków:'],new['Całkowity czas:']) - funkcja_celu(steps_time(trasa_aktualna)['Liczba kroków:'],steps_time(trasa_aktualna)['Całkowity czas:'])

        if delta_dlugosc < 0 or random.uniform(0, 1) < math.exp(-delta_dlugosc / temperatura):
            trasa_aktualna = trasa_sasiada
            best_score=new
            print(best_score)
        temperatura = temperatura_poczatkowa * (1 - iteracja / liczba_iteracji)
        
    return trasa_aktualna, best_score


temperatura_poczatkowa = 100.0
temperatura_koncowa = 0.1
liczba_iteracji = 5000

najlepsza_trasa, minimalna_dlugosc = simulated_annealing( temperatura_poczatkowa, temperatura_koncowa, liczba_iteracji)

print("Najlepsza trasa:", najlepsza_trasa)
print("Minimalna długość trasy:", minimalna_dlugosc)





# w większej pętli zmieniamy tempeterure
# w mniejszej tworzymy małę zmiany z ścieżce (przykladowo zamieniamy punktu które są odwiedzane) (Jeszcze nwm co zmienia w tym temeratura)
# przyjmujemy zawsze lepsze rozwiązanie chyba że random uzna że inaczej
# zprawdzić dla większej liczby punktów
# 