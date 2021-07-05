# calculation-tools

Działanie poszczególnych skryptów
* Otoczka_wypukła.py
Program generuje 20 losowych punktów na płaszczyźnie i tworzy wokół nich elipsy o dwóch losowych parametrach,
następnie używa algorytmu Jarvisa do stworzenia otocznki wypukłej wokół tych elips.
Punkty są generowane w granicach (5.0, 15.0), wyświetlany wykres obejmuje granice (0, 20)
![Covex_Hull]()

* Histogramy_i_kontury.py
Program wczytuje obraz z adresu URL i tworzy z niego histogramy RGB i skali szarości
oraz używa filtra Sobel'a i krzyża Roberts'a do znalezienia konturów.
Obraz nie nie jest rozmywany filtrem Gaussa aby zobaczyć efekt "surowych" filtrów konturów
![Image_Processing]()

* Labirynt.py
Program tworzy labirynt losowanym algorytmem Kruskala,
wykorzystanie tego algorytmu powoduje utworzenie innego typu labiryntu w którym możliwe są ściany nie połączone do
ściany głównej, labirynty mogą wydawać się mniej skomplikowane ale dają możliwość zapętleń, co trzeba uwzględnić
w algorytmie wyszukiwania.
Program znajduje też ścieżkę od lewgo dolnego rogu do prawego górnego
Niektóre wersje labiryntu powodują bardzo długi czas szukania ścieżki,
wtedy lepiej przeładować program żeby nie tracić czasu, ponieważ tego typu labirynty nie są częste,
a czas oczekiwania na wynik zazwyczaj jest krótki.
Wielkość labiryntu może być modyfikowana w wywołaniu funkcji create_maze(),
algorytm będzie zwracał dalej poprawne wyniki, bazowo labirynt jest wielkość 5 na 5 co oznacza pięć hexów zewnętrznych
na pięć hexów zewnętrznych
![Labirynth]()
