import os, glob, numpy
import pandas
import unittest

from evonet.network import ODE, SymOde


class ODETests(unittest.TestCase):

    def setUp(self):
        self.y0 = [1, 1]
        self.t0 = 0
        self.end = 10
        self.dt = 1

    def f(self, t, y, *args):
        return [- args[0] * y[0] + args[1] * y[1],
                +0.3 * y[0] - args * y[1]]

    # def f(self, t, y):
    #     return [1 * y[0] + y[1], - y[1] ** 2]


    def test(self):
        o = ODE(self.f, self.end)
        o.set_initial_value(self.y0, self.t0)
        ts = o.go()




class SymOdeTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_first_order_matrix(self):
        """
        dy(0)/dt = +k0*y(1)
        dy(1)/dt = +k1*y(0)
        a nodes tyable and an edge table
        :return:
        """

        nodes = 'n1 n2 n3'.split()
        from itertools import permutations
        edges = ''

        comb = permutations(nodes, 2)
        matr = numpy.matrix([i for i in comb])
        matr = pandas.DataFrame(matr)
        matr['i'] = 0
        matr = numpy.matrix(matr)
        print(matr)

        ## iterate over table of source to target nodes
        ## what about modifiers
        ## coul work with strings diectly for ode??

        # matrix = numpy.zeros((2, 2))
        # matrix[0, 1] = 1
        # matrix[1, 0] = 1
        #
        #
        # s = SymOde(matrix)
        # s.read_matrix()
        # f, params = s.read_matrix()
        # first = 'k0*y(1)'
        # second = 'k1*y(0)'
        # self.assertEqual("[{}, {}]".format(first, second), str(f))

    def test_another(self):
        """
        dy(0)/dt = k0*y(2)
        dy(1)/dt = k1
        dy(2)/dt = -k0*y(2)

        :return:
        """
        matrix = numpy.matrix(numpy.zeros([3, 3]))
        matrix[0, 0] = 1
        matrix[0, 2] = -1
        matrix[1, 1] = 1
        print(matrix)

        """
        maybe I am going about this the wrong way. Can I create a graph to interpret, rather than a matrix?
        """
        # s = SymOde(matrix)
        # f, params = s.read_matrix()
        # first = "k0*y(0)-"



if __name__ == '__main__':
    unittest.main()