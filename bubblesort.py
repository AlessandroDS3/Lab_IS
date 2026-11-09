"""Bubble Sort, equivalente al pseudocódigo de la Práctica 05."""


class Ordenador:
    """Ordena listas de enteros en forma ascendente."""

    def bubble_sort(self, vet: list[int]) -> None:
        """Modifica vet en el mismo lugar; no devuelve una lista nueva.

        El enunciado usa índices 1..n. Python utiliza 0..n-1:
        j va desde 0 hasta i-2 y se compara vet[j] con vet[j+1].
        Se conservan los dos ciclos y la condición del algoritmo original.
        """
        for i in range(len(vet), 1, -1):
            for j in range(0, i - 1):
                if vet[j] > vet[j + 1]:
                    aux = vet[j]
                    vet[j] = vet[j + 1]
                    vet[j + 1] = aux
