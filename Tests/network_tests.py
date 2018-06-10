import os, glob
import numpy
from evonet.network import Network, Edge, Node
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

        a = Node('A')
        b = Node('B')
        c = Node('C')
        d = Node('D')

        self.first_order_deg = Edge(source=a, target=None, id=1)
        self.zero_order_prod = Edge(source=None, target=b, id=2)
        self.first_order_transition = Edge(source=a, target=b, id=3)
        self.complex_break = Edge(source=a, target=[b, c], id=4)
        self.complex_form = Edge(source=[a, b], target=c, id=5)
        self.second_order_transition = Edge(source=[a, b], target=[c, d], id=6)
        self.second_order_deg = Edge(source=[a, b], target=None, id=7)

    def test_infer_nodes(self):
        n = Network(edges=[self.first_order_deg,
                           self.zero_order_prod])
        nodes = ['A', 'B']
        self.assertListEqual(sorted([i for i in n.nodes.keys()]), nodes)

    def test_infer_nodes2(self):
        n = Network(edges=[self.first_order_deg,
                           self.zero_order_prod,
                           self.second_order_transition
                           ])
        nodes = ['A', 'B', 'C', 'D']
        self.assertListEqual(sorted([i for i in n.nodes.keys()]), nodes)

    def test_first_order_transition_eq(self):
        n = Network(edges=self.first_order_transition)
        self.assertEqual(n.nodes['A'].equation, '-k0*A')

    def test_zero_order_prod_eq(self):
        n = Network(edges=self.zero_order_prod)
        self.assertEqual(n.nodes['B'].equation, '+k0')

    def test_zero_order_deg_eq(self):
        n = Network(edges=self.first_order_deg)
        self.assertEqual(n.nodes['A'].equation, '-k0*A')

    def test_complex_break_eq1(self):
        n = Network(edges=self.complex_break)
        self.assertEqual(n.nodes['A'].equation, '-k0*A')

    def test_complex_break_eq2(self):
        n = Network(edges=self.complex_break)
        self.assertEqual(n.nodes['B'].equation, '+k0*A')

    def test_complex_break_eq3(self):
        n = Network(edges=self.complex_break)
        self.assertEqual(n.nodes['C'].equation, '+k0*A')

    def test_complex_form_eq1(self):
        n = Network(edges=self.complex_form)
        self.assertEqual(n.nodes['A'].equation, '-k0*A*B')

    def test_complex_form_eq2(self):
        n = Network(edges=self.complex_form)
        self.assertEqual(n.nodes['B'].equation, '-k0*A*B')

    def test_complex_form_eq3(self):
        n = Network(edges=self.complex_form)
        self.assertEqual(n.nodes['C'].equation, '+k0*A*B')

    def test_second_order_transition_eq1(self):
        n = Network(edges=self.second_order_transition)
        self.assertEqual(n.nodes['A'].equation, '-k0*A*B')

    def test_second_order_transition_eq2(self):
        n = Network(edges=self.second_order_transition)
        self.assertEqual(n.nodes['B'].equation, '-k0*A*B')

    def test_second_order_transition_eq3(self):
        n = Network(edges=self.second_order_transition)
        self.assertEqual(n.nodes['C'].equation, '+k0*A*B')

    def test_second_order_transition_eq4(self):
        n = Network(edges=self.second_order_transition)
        self.assertEqual(n.nodes['D'].equation, '+k0*A*B')

    def test_second_order_deg_eq1(self):
        n = Network(edges=self.second_order_deg)
        self.assertEqual(n.nodes['A'].equation, '-k0*A*B')

    def test_second_order_deg_eq2(self):
        n = Network(edges=self.second_order_deg)
        self.assertEqual(n.nodes['B'].equation, '-k0*A*B')

    def test_parameter_list(self):
        n = Network(edges=[self.second_order_deg, self.first_order_transition])
        self.assertEqual(n.parameter_list, 'k0 k1'.split())

    def test_sample_parameters(self):
        numpy.random.seed(1)
        n = Network(edges=[self.second_order_deg,
                           self.first_order_transition,
                           self.zero_order_prod])
        params = sorted([i for i in n.parameter_sampling().values()])
        vals = sorted([-0.331911981189704, 0.8812979737686324, -1.9995425007306205])
        self.assertListEqual(params, vals)

    def test_solve(self):
        n = Network(edges=[self.first_order_transition])
        print(n.ode)
        ic = {'A': 10, 'B': 0}
        params = {'k0': 0.1}
        n.solve(ic, params)







if __name__ == '__main__':
    unittest.main()




