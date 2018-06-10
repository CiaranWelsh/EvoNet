import os, glob
import numpy
from evonet.network import Network
import unittest
import site
site.addsitedir(r'/home/b3053674/Documents/timeseries')
from pytseries.core import TimeSeriesGroup, TimeSeries




class NetworkTests(unittest.TestCase):

    def setUp(self):
        x = [0.5, 2, 4, 5.5, 6.5, 7, 7.25, 7.3]
        y = [i*2 for i in x]
        t = [i for i in range(len(x))]
        ts = TimeSeries(values=x, time=t, feature='x')
        ts2 = TimeSeries(values=y, time=t, feature='y')
        self.tsg = TimeSeriesGroup([ts, ts2])


    def test_select_sign(self):
        n = Network(self.tsg)
        sign = n.select_sign()
        self.assertTrue(sign in ['-', '+'])

    def test_zeroth_order(self):
        n = Network(self.tsg)
        out = n.zeroth_order('parameter1')
        self.assertTrue(str(out) == 'parameter1')

    def test_first_order(self):
        n = Network(self.tsg)
        out = n.first_order('parameter1', 'species1')
        self.assertTrue(str(out) == 'parameter1*species1')

    def test_second_order(self):
        n = Network(self.tsg)
        out = n.second_order('parameter1', 'species1', 'species2')
        self.assertTrue(str(out) == 'parameter1*species1*species2')

    def test_select_node(self):
        n = Network(self.tsg)
        nodes = sorted(n.select_node(2))

        self.assertTrue(nodes == [0, 1])

    def test_parameter_factory(self):
        n = Network(self.tsg)
        self.assertTrue(n.parameter_factory() == 'k1')

    def test_node_factory(self):
        n = Network(self.tsg)
        self.assertTrue(n.node_factory() == 'N3')

    # def test_edge(self):
    #     n = Network(self.tsg)
    #     self.assertTrue(str(n.random_edge(0)) in ['k1', '-k1'])
    #
    # def test_edge1(self):
    #     n = Network(self.tsg)
    #     edge = n.random_edge(1)
    #     self.assertTrue(str(edge) in ['k1*x', 'k1*y', '-k1*x', '-k1*y'])
    #
    # def test_edge2(self):
    #     n = Network(self.tsg)
    #     edge = n.random_edge(2)
    #     self.assertTrue(str(edge) in ['k1*x*y', '-k1*x*y'])


    def test_edge4(self):
        n = Network(self.tsg)
        # print(n.new_innovation())
        n.random_edge(0)
        # n.random_edge(0)
        # n.random_edge(0)
        # n.random_edge(0)
        # n.random_edge(0)
        # print(n.equations)


if __name__ == '__main__':
    unittest.main()























