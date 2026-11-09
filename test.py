"""Cuatro casos base y cuatro casos adicionales de robustez."""

import unittest

from bubblesort import Ordenador


class TestOrdenador(unittest.TestCase):
    def setUp(self):
        """Prepara una instancia independiente para cada caso."""
        self.ordenador = Ordenador()

    def tearDown(self):
        """Libera la referencia de la fixture después de cada caso."""
        self.ordenador = None

    def test_cp1_un_elemento(self):
        """CP1: no se ejecuta el cuerpo del ciclo externo."""
        # Arrange
        datos = [7]
        esperado = [7]
        # Act
        resultado = self.ordenador.bubble_sort(datos)
        # Assert
        self.assertEqual(datos, esperado)
        self.assertIsNone(resultado)

    def test_cp2_dos_ordenados(self):
        """CP2: una comparación, sin intercambio."""
        # Arrange
        datos = [1, 2]
        esperado = [1, 2]
        # Act
        self.ordenador.bubble_sort(datos)
        # Assert
        self.assertEqual(datos, esperado)

    def test_cp3_dos_invertidos(self):
        """CP3: una comparación con intercambio."""
        # Arrange
        datos = [2, 1]
        esperado = [1, 2]
        # Act
        self.ordenador.bubble_sort(datos)
        # Assert
        self.assertEqual(datos, esperado)

    def test_cp4_tres_ordenados(self):
        """CP4: dos pasadas y tres comparaciones sin intercambio."""
        # Arrange
        datos = [1, 2, 3]
        esperado = [1, 2, 3]
        # Act
        self.ordenador.bubble_sort(datos)
        # Assert
        self.assertEqual(datos, esperado)

    def test_extra_lista_vacia(self):
        # Arrange
        datos = []
        # Act
        self.ordenador.bubble_sort(datos)
        # Assert
        self.assertEqual(datos, [])

    def test_extra_negativos_y_cero(self):
        # Arrange
        datos = [0, -3, 2, -1]
        # Act
        self.ordenador.bubble_sort(datos)
        # Assert
        self.assertEqual(datos, [-3, -1, 0, 2])

    def test_extra_repetidos(self):
        # Arrange
        datos = [3, 1, 3, 1]
        # Act
        self.ordenador.bubble_sort(datos)
        # Assert
        self.assertEqual(datos, [1, 1, 3, 3])

    def test_extra_orden_inverso(self):
        # Arrange
        datos = [5, 4, 3, 2, 1]
        # Act
        self.ordenador.bubble_sort(datos)
        # Assert
        self.assertEqual(datos, [1, 2, 3, 4, 5])


if __name__ == '__main__':
    unittest.main(verbosity=2)
