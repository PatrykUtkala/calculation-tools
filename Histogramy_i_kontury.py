import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request as req
# Program wczytuje obraz z adresu URL i tworzy z niego histogramy RGB i skali szarości
# oraz używa filtra Sobel'a i krzyża Roberts'a do znalezienia konturów.
# Obraz nie nie jest rozmywany filtrem Gaussa aby zobaczyć efekt "surowych" filtrów konturów


def load_image():  # funkcja zwracająca obraz pod ustalonym adresem URL
    req.URLopener()
    req.urlretrieve('https://media.comicbook.com/2020/08/cyberpunk-2077-1--1233341-1280x0.jpeg', "im1.jpeg")
    im = Image.open('im1.jpeg')
    return im


def make_histogram(color):  # funkcja tworząca histogram z danej tablicy koloru
    histogram = np.array([])
    for x in range(0, 256):
        histogram = np.append(histogram, len(color[color == x]))
    return histogram


def plot_histograms(r, g, b, grey, image, image_s, image_r):  # funkcja wyświetlająca wyniki
    plt.figure(figsize=(15, 10))
    r_plot = plt.subplot(331)
    r_plot.plot(r, 'r')
    plt.title('histogram koloru czerwonego')
    g_plot = plt.subplot(332)
    g_plot.plot(g, 'g')
    plt.title('histogram koloru zielonego')
    b_plot = plt.subplot(333)
    b_plot.plot(b, 'b')
    plt.title('histogram koloru niebieskiego')
    a_plot = plt.subplot(334)
    a_plot.plot(r, 'r')
    a_plot.plot(g, 'g')
    a_plot.plot(b, 'b')
    plt.ylabel('nałożone histogramy')  # dalsze nazwy wykresów są napisane w poprzek żeby nie nakładały się
    grey_plot = plt.subplot(335)       # na inne wykresy
    grey_plot.plot(grey, 'black')
    plt.ylabel('histogram skali szarości')
    plt.subplot(337)
    plt.imshow(image)
    plt.ylabel('obraz oryginalny')
    plt.subplot(338)
    plt.imshow(image_s)
    plt.ylabel('kontury (filtr Sobel\'a)')
    plt.subplot(339)
    plt.imshow(image_r)
    plt.ylabel('kontury (krzyż Roberts\'a)')
    plt.suptitle('przetwarzanie obrazu')
    plt.show()


def sobel(im, level):  # funkcja realizująca filtr Sobel'a z granicą wyświetlania
    sx00 = np.roll(np.roll(im, -1, axis=1), -1, axis=0)
    sx01 = 2 * np.roll(im, -1, axis=0)
    sx02 = np.roll(np.roll(im, 1, axis=1), -1, axis=0)
    sx20 = -np.roll(np.roll(im, -1, axis=1), 1, axis=0)
    sx21 = -2 * np.roll(im, 1, axis=0)
    sx22 = -np.roll(np.roll(im, 1, axis=1), 1, axis=0)

    sy00 = np.roll(np.roll(im, -1, axis=1), -1, axis=0)
    sy02 = -np.roll(np.roll(im, 1, axis=1), -1, axis=0)
    sy10 = 2 * np.roll(im, -1, axis=1)
    sy12 = -2 * np.roll(im, 1, axis=1)
    sy20 = np.roll(np.roll(im, -1, axis=1), 1, axis=0)
    sy22 = -np.roll(np.roll(im, 1, axis=1), 1, axis=0)
    gx = sx00 + sx01 + sx02 + sx20 + sx21 + sx22
    gy = sy00 + sy10 + sy02 + sy20 + sy12 + sy22

    new_im = np.sqrt(gx**2 + gy**2)
    new_im[np.where(new_im < level)] = 0
    return new_im


def roberts_cross(im, level):  # funkcja realizująca filtr krzyż Roberts'a z granicą wyświetlania
    ra00 = np.roll(np.roll(im, -1, axis=1), -1, axis=0)
    ra11 = -np.roll(np.roll(im, 1, axis=1), -1, axis=0)
    rb01 = np.roll(np.roll(im, -1, axis=1), 1, axis=0)
    rb10 = -np.roll(np.roll(im, 1, axis=1), 1, axis=0)
    ra = ra00 + ra11
    rb = rb10 + rb01
    new_im = np.absolute(ra) + np.absolute(rb)
    new_im[np.where(new_im < level)] = 0

    return new_im


def process_image():  # funkcja realizująca operacje na obrazie
    image = np.array(load_image())
    r = image[:, :, 0]
    g = image[:, :, 1]
    b = image[:, :, 2]
    grey_scale = 0.299*r + 0.587*g + 0.114*b

    r_histogram = make_histogram(r)
    g_histogram = make_histogram(g)
    b_histogram = make_histogram(b)
    grey_scale_histogram = make_histogram(grey_scale)

    image_s = Image.fromarray(sobel(grey_scale, 150))
    image_r = Image.fromarray(roberts_cross(grey_scale, 45))

    plot_histograms(r_histogram, g_histogram, b_histogram, grey_scale_histogram, image, image_s, image_r)


process_image()
