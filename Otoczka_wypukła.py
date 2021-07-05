import matplotlib.pyplot as plt
import numpy as np


# Program generuje 20 losowych punktów na płaszczyźnie i tworzy wokół nich elipsy o dwóch losowych parametrach,
# następnie używa algorytmu Jarvisa do stworzenia otocznki wypukłej wokół tych elips.
# Punkty są generowane w granicach (5.0, 15.0), wyświetlany wykres obejmuje granice (0, 20)


class Tiger:  # klasa tygrysa trzymająca informacje o punkcie na płaszczyźnie i parametrach elipsy wokół punktu
    def __init__(self, point):  # funckja inicjalizująca która ustala losowe parametry elipsy
        self.point = point
        self.params = (np.random.rand(2) * 1.5) + 0.5  # parametry elipsy mieszczą się w granicach (0.5, 2.0)

    def gen_points(self):  # funkcja zwracająca zestaw punktów tworzący elipsę
        t = np.arange(0, 2 * np.pi, 0.01)
        points = self.point[0] + self.params[0] * np.cos(t), self.point[1] + self.params[1] * np.sin(t)
        return points


def jarvis_algorithm(points_set):  # funkcja tworząca otoczkę wypukłą na podstawie zadanych punktów algorytmem Jarvisa
    # Ustalenie punktów leżących najwyżej i najniżej
    p1 = points_set[np.where(points_set[:, 1] == np.amin(points_set[:, 1]))].reshape(2)
    q1 = points_set[np.where(points_set[:, 1] == np.amax(points_set[:, 1]))].reshape(2)
    # iterowana część algorytmu Jarvisa
    pi = p1
    convex_hull = p1
    while all(pi != q1):  # wyznaczanie prawego łańcucha otoczki
        theta = np.arctan2(pi[1] - points_set[:, 1], pi[0] - points_set[:, 0])
        pn = points_set[np.where(theta == np.amin(theta))].reshape(2)
        convex_hull = np.append(convex_hull, pn).reshape(int((convex_hull.size / 2) + 1), 2)
        pi = pn

    qi = q1
    while all(qi != p1):  # wyznaczanie lewego łańcucha otoczki
        theta = np.arctan2(-qi[1] + points_set[:, 1], -qi[0] + points_set[:, 0])
        q2 = points_set[np.where(theta == np.amin(theta))].reshape(2)
        convex_hull = np.append(convex_hull, q2).reshape(int((convex_hull.size / 2) + 1), 2)
        qi = q2

    return convex_hull


def plot_convex_hull():
    plt.figure(figsize=(9, 9))
    # generowanie tygrysów
    random_points = np.random.rand(20, 2) * 10 + 5
    tigers = []
    ellipses = []
    all_points = random_points
    # tworzenie zbioru tygrysów i wszystkich punktów potrzebnych do generowania otoczki
    for x in range(0, 20):
        tigers.append(Tiger(random_points[x]))
        ellipses.append(np.array(tigers[x].gen_points()))
        ellipses[x] = ellipses[x].transpose()
        all_points = np.concatenate((all_points, ellipses[x]), axis=0)
    ellipses = np.array(ellipses)
    # inicjalizacja algorytmu Jarvisa
    convex_hull = jarvis_algorithm(all_points)
    # nanoszenie danych na płaszczyznę
    ax = plt.subplot()
    ax.plot(random_points[:, 0], random_points[:, 1], 'bo')
    for x in range(0, 20):
        ax.plot(ellipses[x, :, 0], ellipses[x, :, 1], 'b')
    ax.plot(convex_hull[:, 0], convex_hull[:, 1], 'r')
    # ustalenie parametrów wykresu
    plt.axis([0, 20, 0, 20])
    plt.title('Otoczka wypukła')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid(True)

    plt.show()

    return 0


plot_convex_hull()
