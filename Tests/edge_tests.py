import os, glob
import numpy
from evonet.network import Network, Edge, Node
import unittest
import site
site.addsitedir(r'/home/b3053674/Documents/timeseries')
from pytseries.core import TimeSeriesGroup, TimeSeries




class EdgeTests(unittest.TestCase):

    def setUp(self):
        self.a = Node('A')
        self.b = Node('B')
        self.c = Node('C')
        self.d = Node('D')


    def test_first_order_deg(self):
        ## i.e. x -> ; k
        E = Edge(source=self.a, target=None, id=1)
        self.assertTrue(E.form == 'first_order_deg')

    def test_second_order_deg(self):
        ##i.e. x + y -> ; k*x*y
        E = Edge(source=[self.a, self.b], target=None, id=7)
        self.assertTrue(E.form == 'second_order_deg')
    #
    def test_zero_order_prod(self):
        ## i.e. -> x; k
        E = Edge(source=None, target=self.b, id=2)
        self.assertTrue(E.form == 'zero_order_prod')

    def test_raises_error_With_two_targets_no_source(self):
        ## -> A + B
        E = Edge(target=[self.a, self.b], id=1)
        with self.assertRaises(ValueError):
            E.form

    def test_first_order_transition(self):
        E = Edge(source=self.a, target=self.b, id=3)
        self.assertTrue(E.form == 'first_order_transition')

    def test_complex_break(self):
        ## a -> x + y
        E = Edge(source=self.a, target=[self.b, self.c], id=4)
        self.assertTrue(E.form == 'complex_break')

    def test_complex_form(self):
        ## x + y -> z
        E = Edge(source=[self.a, self.b], target=self.c, id=5)
        self.assertTrue(E.form == 'complex_form')

    def test_second_order_transition(self):
        E = Edge(source=[self.a, self.b], target=[self.c, self.d], id=6)
        self.assertTrue(E.form == 'second_order_transition')

    # def test_tra(self):
    #     ## eq should have forn k*a
    #     E = Edge(source='a', id=1)
    #     print(E.equation())



if __name__ == '__main__':
    unittest.main()























