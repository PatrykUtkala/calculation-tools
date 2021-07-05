import numpy as np
from numpy.random import randint as rand
import matplotlib.pyplot as plt
# Program tworzy labirynt losowanym algorytmem Kruskala,
# wykorzystanie tego algorytmu powoduje utworzenie innego typu labiryntu w którym możliwe są ściany nie połączone do
# ściany głównej, labirynty mogą wydawać się mniej skomplikowane ale dają możliwość zapętleń, co trzeba uwzględnić
# w algorytmie wyszukiwania.
# Program znajduje też ścieżkę od lewgo dolnego rogu do prawego górnego
# Niektóre wersje labiryntu powodują bardzo długi czas szukania ścieżki,
# wtedy lepiej przeładować program żeby nie tracić czasu, ponieważ tego typu labirynty nie są częste,
# a czas oczekiwania na wynik zazwyczaj jest krótki.
# Wielkość labiryntu może być modyfikowana w wywołaniu funkcji create_maze(),
# algorytm będzie zwracał dalej poprawne wyniki, bazowo labirynt jest wielkość 5 na 5 co oznacza pięć hexów zewnętrznych
# na pięć hexów zewnętrznych
p3 = 1.73205080757


def set_boarders(y1, y2, x, width, height):  # funkcja ustawiająca ściany wokół labiryntu
    y1[0, :], y2[0, :] = 1, 1
    y1[width, :], y2[width - 1, :] = 1, 1
    x[0, :] = 1
    x[width * 2 - 1, :] = 1
    x[:, 0] = 1
    x[:, height * 2 - 1] = 1
    return y1, y2, x


def find_route(route, cell, rooms, width, height):  # rekurencyjna funkcja odpowiadająca za znajdywanie ścieżki
    if route[-1] == width * height - 1:
        return route
    else:
        for i in range(6):
            if (rooms[cell, i] != -1) & (not (np.any(route == rooms[cell, i]))):
                route = find_route(np.hstack((route, rooms[cell, i])), rooms[cell, i], rooms, width, height)
                if route[-1] == width * height - 1:
                    return route

    return route[:-1]


def solve(y1, y2, x, width, height):  # funkcja tworzy graf połączeń pokoi na podstawie ścian labiryntu
    rooms1 = np.zeros((width, height), dtype=bool)
    rooms1[0, 0] = 1
    route = np.array([0])
    cell = 0
    rooms1 = -1 * np.ones(((width * height + (width - 1) * (height - 1)), 6), dtype=int)
    # wypełnianie grafu połączeń dla hexów zewnętrznych
    for i in range(width * height):
        if y1[i % width, i // width] == 0:
            rooms1[i, 0] = i - 1
        if y1[i % width + 1, i // width] == 0:
            rooms1[i, 3] = i + 1
        if x[2 * (i % width) + 1, 2 * (i // width) + 1] == 0:
            rooms1[i, 1] = i + width * height - (i // width)
        if x[2 * (i % width), 2 * (i // width) + 1] == 0:
            rooms1[i, 2] = i + width * height - 1 - (i // width)
        if x[2 * (i % width) + 1, 2 * (i // width)] == 0:
            rooms1[i, 4] = i + width * height - width + 1 - (i // width)
        if x[2 * (i % width), 2 * (i // width)] == 0:
            rooms1[i, 5] = i + width * height - width - (i // width)

    # wypełnianie grafu połączeń dla hexów wewnętrznych
    for i in range(0, (width - 1) * (height - 1)):
        if y2[i % (width - 1), i // (width - 1)] == 0:
            rooms1[i + width * height, 0] = i - 1 + width * height
        if y2[i % (width - 1) + 1, (i // (width - 1))] == 0:
            rooms1[i + width * height, 3] = i + 1 + width * height
        if x[2 * (i % (width - 1)) + 2, 2 * (i // (width - 1)) + 2] == 0:
            rooms1[i + width * height, 1] = (i % (width - 1)) + ((i // (width - 1)) + 1) * width + 1
        if x[2 * (i % (width - 1)) + 1, 2 * (i // (width - 1)) + 2] == 0:
            rooms1[i + width * height, 2] = (i % (width - 1)) + ((i // (width - 1)) + 1) * width
        if x[2 * (i % (width - 1)) + 2, 2 * (i // (width - 1)) + 1] == 0:
            rooms1[i + width * height, 4] = (i % (width - 1)) + (i // (width - 1)) * width + 1
        if x[2 * (i % (width - 1)) + 1, 2 * (i // (width - 1)) + 1] == 0:
            rooms1[i + width * height, 5] = (i % (width - 1)) + (i // (width - 1)) * width

    # wywołanie funkcji przeszukującej wygenerowany graf
    route = find_route(route, cell, rooms1, width, height)

    return route


def maze_hex(width=5, height=5, complexity=0.75):  # funkcja generująca labirynt losowanym algorytmem Kruskala
    shape = (height, width)
    points = np.zeros((2 * width + 1, (3 * height)), dtype=bool)
    complexity = int(complexity * (125 * (shape[0] + shape[1])))
    # tutaj ustawiane są ściany na podstawie których tworzony jest labirynt
    # ściany są podzielone na dwa rodzaje wertykalnych i jeden horyzontalny
    connections_y1 = np.zeros((width + 1, height), dtype=int)
    connections_y2 = np.zeros((width, height - 1), dtype=int)
    connections_x = np.zeros((width * 2, height * 2), dtype=int)
    connections_y1, connections_y2, connections_x = set_boarders(connections_y1, connections_y2,
                                                                 connections_x, width, height)
    for d in range(complexity):  # losowanie ścian labiryntu
        # tylko do jednego punktu może przylegać ściana aby stworzyć nową ścianę między dwoma punktami
        a = rand(0, 8)  # losowanie typu ściany do wypełnienia
        if a == 0:
            x, y, direction = rand(0, width), rand(0, height), rand(0, 2)
            if (connections_x[x * 2, y * 2 + direction] == 0) & (connections_x[x * 2 - 1, y * 2 + direction] == 0):
                connections_y1[x, y] = 1
        elif a == 1:
            x, y, direction = rand(0, width), rand(0, height - 1), rand(0, 2)
            if (connections_x[x * 2, 1 + y * 2 + direction] == 0) & (connections_x[x * 2 + 1, y * 2 + direction] == 0):
                connections_y2[x, y] = 1
        if a > 1:
            x, y, direction = rand(0, width * 2), rand(0, height * 2), rand(0, 2)
            if ((x % 2 == 1) & (y % 2 == 1)) | ((x % 2 == 0) & (y % 2 == 0)):
                if (direction == 1) & (x < width * 2 - 1):
                    if (x % 2 == 1) & (connections_y1[int((x + 1) / 2), int((y - 1) / 2)] == 0) & (
                            connections_x[x + 1, y] == 0):
                        connections_x[x, y] = 1

                if (direction == 0) & (x > 1) & (y < height * 2 - 1):
                    if (x % 2 == 1) & (connections_y2[int((x - 1) / 2), int((y - 1) / 2)] == 0) \
                            & (connections_x[x - 1, y] == 0):
                        connections_x[x, y] = 1

            if ((x % 2 == 0) & (y % 2 == 1)) | ((x % 2 == 1) & (y % 2 == 0)):
                if (direction == 1) & (x < width * 2 - 1) & (y < height * 2 - 1):
                    if (x % 2 == 1) & (connections_y2[int((x - 1) / 2), int((y - 1) / 2)] == 0) & (
                            connections_x[x + 1, y] == 0):
                        connections_x[x, y] = 1
                if (direction == 0) & (x > 1) & (y < height * 2 - 1):
                    if (x % 2 == 1) & (connections_y1[int((x + 1) / 2), int((y - 1) / 2)] == 0) \
                            & (connections_x[x - 1, y] == 0):
                        connections_x[x, y] = 1
    # wywołanie funkcji rozwiązującej labirynt
    route = solve(connections_y1, connections_y2, connections_x, width, height)
    connections_y1[0, 0] = 0
    connections_y1[width, height-1] = 0
    return points, connections_y1, connections_y2, connections_x, route


# funkcja wyświetlająca labirynt
def create_maze(width=5, height=5):
    plt.figure(figsize=(9, 9))

    plt.subplot(111)
    points, cons_y1, cons_y2, cons_x, route = maze_hex(width, height)
    plt.axis([-10, len(points[0, :]) * 2 + 10, -10, len(points[0, :]) * 2 + 10])

    # wyświetlane wygenerowanego labiryntu
    for X in range(len(points[:, 0])):
        for Y in range(len(points[0, :])):
            if X % 2 == 0:
                if Y % 3 != 2:
                    plt.plot(p3 * X, (2 * Y) + 1, 'r.')
            elif Y % 3 != 1:
                plt.plot(p3 * X, 2 * Y, 'r.')

    for j in range(len(cons_y1[:, 0])):
        for i in range(len(cons_y1[0, :])):
            if cons_y1[j, i] == 1:
                plt.plot([2 * p3 * j, 2 * p3 * j], [6 * i + 1, 6 * i + 3], 'g')

    for j in range(len(cons_y2[:, 0])):
        for i in range(len(cons_y2[0, :])):
            if cons_y2[j, i] == 1:
                plt.plot([p3 + 2 * p3 * j, p3 + 2 * p3 * j], [3 + (6 * i + 1), 3 + (6 * i + 3)], 'b')

    for j in range(len(cons_x[:, 0])):
        for i in range(len(cons_x[0, :])):
            if cons_x[j, i] == 1:
                if ((j % 2 == 1) & (i % 2 == 1)) | ((j % 2 == 0) & (i % 2 == 0)):
                    plt.plot([p3 * j, p3 * (j + 1)], [p3 / 2 + (3 * i), (3 * i)], 'r')
                if ((j % 2 == 0) & (i % 2 == 1)) | ((j % 2 == 1) & (i % 2 == 0)):
                    plt.plot([p3 * j, p3 * (j + 1)], [(3 * i), (3 * i) + p3 / 2], 'm')

    # przeliczenie ścieżki do końca labiryntu na wartości do wyświetlenia
    route_plotx = -((route // (width * height)) - 1) * (p3 + 2 * p3 * (route % width)) + \
                  (route // (width * height)) * (2 * p3 + 2 * p3 * ((route - (width * height)) % (width - 1)))
    route_ploty = -((route // (width * height)) - 1) * (2 + 6 * (route // width)) + \
                  (route // (width * height)) * (5 + 6 * ((route - (width * height)) // (width - 1)))
    plt.plot(route_plotx, route_ploty, 'b--')

    plt.show()


create_maze(5, 5)
