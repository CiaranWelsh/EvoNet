import os, glob
import numpy
from evonet.network import Network, Edge, Node
import unittest
import site
site.addsitedir(r'/home/b3053674/Documents/timeseries')
from pytseries.core import TimeSeriesGroup, TimeSeries




class NodeTests(unittest.TestCase):

    def setUp(self):
        x = [0.5, 2, 4, 5.5, 6.5, 7, 7.25, 7.3]
        y = [i*2 for i in x]
        t = [i for i in range(len(x))]
        ts = TimeSeries(values=x, time=t, feature='x')
        ts2 = TimeSeries(values=y, time=t, feature='y')
        self.tsg = TimeSeriesGroup([ts, ts2])

    def test_id(self):
        n = Node('A', equation='-k')
        self.assertTrue(n.id == 'A')

    def test_eq(self):
        n = Node('A', equation='-k')
        self.assertTrue(n.equation == '-k')



if __name__ == '__main__':
    unittest.main()























