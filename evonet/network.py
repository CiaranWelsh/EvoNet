import pandas
import numpy
import os, glob
from scipy.integrate import ode
from pyodesys.core import ODESys
from pyodesys.symbolic import SymbolicSys
import sympy
from jitcode import jitcode, y
from functools import reduce
from numpy.random import uniform
from collections import OrderedDict


'''
What am i doing?
================
1) Create nodes from tsg
    - completly unconnected
2) Create new mutation
    - node mutation
        - Splits an existing connection
        - Old connection is set to disable
        - parameters derived from existing parameter or set to 1
    - edge mutation
        - 
    - parameter mutation
3) Simulate some data
4) Compute AIC
5) repeat the above with n models
6) mate models
7) pick mutation


Need ability to test whether networks are equal, this would be species. Parameter values not 

'''

class Network_old:

    def __init__(self, tsg, node_mutation=0.01, edge_mutation=0.09, parameter_mutation=0.9):
        self.tsg = tsg
        self.node_mutation = node_mutation
        self.edge_mutation = edge_mutation
        self.parameter_mutation = parameter_mutation

        self.nodes = OrderedDict()

        for i in range(len(self.tsg.features)):
            self.nodes[i] = self.tsg.features[i]

        self.edges = []
        self.parameters = []
        self.equations = OrderedDict()

    @property
    def maximum_edges(self):
        pass

    @staticmethod
    def zeroth_order(k):
        return sympy.symbols(k)

    @staticmethod
    def first_order(k, A):
        k, A = sympy.symbols([k, A])
        return k*A

    @staticmethod
    def second_order(k, A, B):
        k, A, B = sympy.symbols([k, A, B])
        return k*A*B

    @staticmethod
    def select_sign():
        return numpy.random.choice('+ -'.split(), 1)[0]

    def new_innovation(self):
        type = numpy.random.choice(['node', 'edge', 'parameter'], 1, p=[self.node_mutation,
                                                                       self.edge_mutation,
                                                                       self.parameter_mutation])[0]
        if type == 'node':
            self.node_factory()

        elif type == 'edge':
            pass

        elif type == 'parameter':
            pass

        else:
            raise ValueError('well this shouldnt have happened')


    def select_node(self, n):
        return numpy.random.choice([i for i in self.nodes.keys()], n, replace=False)

    def parameter_factory(self):
        return "k{}".format(len(self.parameters) + 1)

    def random_edge(self, seed=None):
        """
        Add a 0, first or second order reaction to a equation
        Make sure  two reactions of same type do not exist in a single equation
        Reuse parameters where you can
        :param seed:
        :return:
        """
        if seed is not None:
            if seed not in [0, 1, 2]:
                raise ValueError('seed parameter is either 0, 1 or 2')
            order = seed
        else:
            order = numpy.random.choice([0, 1, 2], 1)[0]


        ## select which node we apply this edge too
        subject_node = self.nodes[self.select_node(1)[0]]
        print(subject_node)

        # param = self.parameter_factory()
        # sign = self.select_sign()
        #
        # self.parameters.append(param)
        #
        # if order == 0:
        #     ## inspect equations for whether this alredy exists
        #     # print(self.edges)
        #     subject_node_equation = self.equations.get(subject_node)
        #     # print(subject_node)
        #     print(subject_node_equation, type(subject_node_equation))
        #     import re
        #     if subject_node_equation is not None:
        #         print(re.findall(r'k.* ', str(subject_node_equation)))
        #
        #     # print(self.equations)
        #     edge = self.zeroth_order(param)
        #     self.add_edge(edge, subject_node)
        #
        # elif order == 1:
        #     n = self.select_node(1)[0]
        #     # import re
        #     # if re.findall('k.*\*{}'.format(self.nodes[n]), )
        #     edge = self.first_order(param, self.nodes[n])
        #
        # elif order == 2:
        #     nodes = sorted(self.select_node(2))
        #     edge = self.second_order(param, self.nodes[nodes[0]], self.nodes[nodes[1]])
        #
        # else:
        #     raise ValueError("order is {}. Type is {}".format(order, type(order)))
        # if sign == '-':
        #     edge = edge * -1
        # # edge = sign+edge
        # # print(edge)
        # if edge in self.edges:
        #     self.random_edge()
        #
        # else:
        #     self.edges.append(edge)
        #
        # return edge

    def node_factory(self):
        new_node = "N{}".format(len(self.nodes) + 1)
        self.nodes[len(self.nodes) + 1] = new_node
        return new_node

    def add_edge(self, edge, node):
        """
        add edge to equation
        :param edge:
        :param node:
        :return:
        """
        if self.equations.get(node) is None:
            self.equations[node] = edge
        else:
            self.equations[node] = self.equations[node] + edge

    def augment_network(self):
        node = self.select_node(1)
        edge = self.random_edge()
        if self.equations.get(self.nodes[node[0]]) is None:
            self.equations[self.nodes[node[0]]] = edge
        else:
            self.equations[self.nodes[node[0]]] = self.equations[self.nodes[node[0]]] + edge

    def x(self):
        print('nodes', self.nodes)
        print('edges', self.edges)

        # sign = self.select_sign()
        edge = self.random_edge()
        node = self.select_node(1)
        # print(node, self.nodes[node[0]], edge)
        # self.equations[self.nodes[node[0]]] = edge

        for i in range(4):

            node = self.select_node(1)
            edge = self.random_edge()
            if self.equations.get(self.nodes[node[0]]) is None:
                self.equations[self.nodes[node[0]]] = edge
            else:
                self.equations[self.nodes[node[0]]] = self.equations[self.nodes[node[0]]] + edge

        print(self.equations)

    ## somehow need to test for coherance. I.e.
    ## cannot have +k1*x*y in ODE for x but not t-k8*x*y
    ## in ode for y. No wait. Yes you can, its called a modifier.



class Edge:

    TRANSITION_TYPES = ['zero_order_prod', 'second_order_deg', 'first_order_deg',
                        'first_order_transition', 'complex_form', 'complex_break',
                        'second_order_transition']

    def __init__(self, source=None, target=None, enabled=True, id=None,
                 parameter=0.1):
        self.source = source
        self.target = target
        self._enabled = enabled
        self.parameter = parameter

        if id is None:
            raise ValueError('id must be given')

        if not isinstance(id, int):
            raise TypeError('is should be int')
        self._id = id

        if self.parameter is None:
            raise ValueError

        if isinstance(self.source, (str, Node)):
            self.source = [self.source]

        if isinstance(self.target, (str, Node)):
            self.target = [self.target]

        if self.source is not None:
            for i in self.source:
                if not isinstance(i, Node):
                    raise TypeError('Input to source must be a Node object')

        if self.target is not None:
            for i in self.target:
                if not isinstance(i, Node):
                    raise TypeError('Input to target must be a Node object')

    def __str__(self):
        return "Edge(source={}, target={}, enabled={}, id={}, parameter={})".format(
            self.source, self.target, self.enabled, self.id, self.parameter
        )

    def __repr__(self):
        return self.__str__()

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def form(self):
        """
        determine what type of reaction this
        will be from source and target arguments
        :return:
        """
        form = None
        if self.source is None and self.target is None:
            raise ValueError('Both source and target cannot be None')

        elif self.source is None and self.target is not None:
            ## i.e. -> A + B ; k
            if len(self.target) == 2:

                raise ValueError('It does not make sense for multiple targets to be '
                                 'produced by a single zero order reaction. Please give only a '
                                 'string as argument to target')
            if len(self.target) == 1:
                ## i.e. -> A ; k
                # form = self.target
                form = 'zero_order_prod'

        elif self.source is not None and self.target is None:
            ## switch to using lengths
            if len(self.source) == 2:
                ## i.e. A + B -> ; -k*A*B. Need to add to both equations
                form = 'second_order_deg'

            elif len(self.source) == 1:
                ## i.e. A ->
                # form = 'k*{}'.format(self.source)
                form = 'first_order_deg'

        elif len(self.source) == 1 and len(self.target) == 1:
            ## i.e. A -> B ; k*A. First order transition
            form = 'first_order_transition'

        elif len(self.source) == 2 and len(self.target) == 1:
            ## i.e. A + B -> C
            ## what about A + B -> A?
            form = 'complex_form'

        elif len(self.source) == 1 and len(self.target)== 2:
            ## i.e. A -> B + C
            form = 'complex_break'

        elif len(self.source)  == 2 and len(self.target) == 2:
            ## i.e. A + B -> C + D
            form = 'second_order_transition'

        return form

    # def equation(self):
    #     """
    #     translate form into string equation
    #     Maybe this is better done outside edge class?
    #     :return:
    #     """
    #     if self.form == 'zero_order_prod':
    #         eq = 'k'
    #
    #     elif self.form == 'second_order_deg':
    #         eq = 'k*'
    #
    #     elif self.form == 'first_order_deg':
    #         pass
    #
    #     elif self.form == 'first_oder_transition':
    #         pass
    #
    #     elif self.form == 'complex_form':
    #         pass
    #
    #     elif self.form == 'complex_break':
    #         pass
    #
    #
    #     elif self.form == 'second_order_transition':
    #         pass


class Node:
    def __init__(self, id, equation=''):
        self.id = id
        self.equation = equation

    def __str__(self):
        return "Node(id={}, equation={})".format(self.id, self.equation)

    def __repr__(self):
        return self.__str__()


class Network:

    k = 0
    parameter_list = []

    def __init__(self, edges, nodes=None, param_min=0.01, param_max=100):
        self.nodes = nodes
        self.edges = edges
        self.param_min = param_min
        self.param_max = param_max

        ##cater for single node/edge situations
        if isinstance(self.edges, Edge):
            self.edges = [self.edges]

        if self.nodes is not None:
            if isinstance(self.nodes, Node):
                self.nodes = [self.nodes]

        if self.nodes is None:
            self.nodes = self._infer_nodes_from_edges()

        ## get id: node/edge representation
        self.nodes, self.edges = self._convert_to_ordered_dict()

        self._set_node_equations()

    def _infer_nodes_from_edges(self):
        targets = []

        for i in self.edges:
            if isinstance(i.target, Node):
                targets.append(i.target)

            elif isinstance(i.target, list):
                targets += i.target

            elif i.target is None:
                continue

            else:
                raise ValueError

        sources = []
        for i in self.edges:
            if isinstance(i.source, Node):
                sources.append(i.source)

            elif isinstance(i.source, list):
                sources += i.source

            elif i.source is None:
                continue

            else:
                raise ValueError

        targets = list(set(targets))
        sources = list(set(sources))
        return list(set(targets + sources))

    def _convert_to_ordered_dict(self):
        """
        Convert nodes and edges into ordered dict
        :return:
        """
        nodes = OrderedDict()
        edges = OrderedDict()

        for node in self.nodes:
            nodes[node.id] = node

        for edge in self.edges:
            edges[edge.id] = edge

        return nodes, edges

    def get_node_by_id(self, id):
        if id not in self.nodes.keys():
            raise ValueError('id "{}" not in nodes. These are your nodes: "{}"'.format(id, self.nodes))

        return [i for i in self.nodes.values() if i.id == id][0]

    def _set_node_equations(self):
        for edge_id, edge in self.edges.items():
            if edge.form == 'first_order_transition':
                ## A -> B;
                assert len(edge.source) == 1
                assert len(edge.target) == 1
                eq = 'k{}*{}'.format(self.k, edge.source[0].id)
                source_node = edge.source[0]
                target_node = edge.target[0]
                source_node.equation += '-' + eq
                target_node.equation += '+' + eq

            elif edge.form == 'zero_order_prod':
                ## -> A
                assert len(edge.target) == 1
                target = edge.target[0]
                eq = 'k{}'.format(self.k)
                target.equation += '+' + eq

            elif edge.form == 'second_order_deg':
                ## A + B ->
                assert isinstance(edge.source, list)
                eq = 'k{}*{}*{}'.format(self.k, edge.source[0].id, edge.source[1].id)
                for i in edge.source:
                    i.equation += '-' + eq

            elif edge.form == 'first_order_deg':
                ## A -> ;
                assert len(edge.source) == 1
                eq = 'k{}*{}'.format(self.k, edge.source[0].id)
                edge.source[0].equation += '-' + eq

            elif edge.form == 'complex_form':
                assert len(edge.source) == 2
                assert len(edge.target) == 1
                eq = "k{}*{}*{}".format(
                    self.k,
                    edge.source[0].id,
                    edge.source[1].id
                )
                for i in edge.source:
                    i.equation += '-' + eq

                for i in edge.target:
                    i.equation += '+' + eq

            elif edge.form == 'complex_break':
                assert len(edge.source) == 1
                assert len(edge.target) == 2
                eq = "k{}*{}".format(
                    self.k,
                    edge.source[0].id,
                    edge.target[0].id
                )
                edge.source[0].equation = '-' + eq
                for i in edge.target:
                    i.equation += '+' + eq

            elif edge.form == 'second_order_transition':
                assert len(edge.source) == 2
                assert len(edge.target) == 2

                eq = "k{}*{}*{}".format(
                    self.k,
                    edge.source[0].id,
                    edge.source[1].id
                )
                for i in edge.source:
                    i.equation += '-' + eq

                for i in edge.target:
                    i.equation += '+' + eq
            self.parameter_list += ['k{}'.format(self.k)]
            self.k += 1

    @property
    def ode(self):
        """
        get list of ODEs
        :return:
        """
        ode_dct = OrderedDict()
        for id, node in self.nodes.items():
            ode_dct[id] = node.equation

        return ode_dct

    def parameter_sampling(self):
        """
        parameter sampling in log linear space
        :return:
        """
        return {i: uniform(numpy.log10(self.param_min),
                           numpy.log10(self.param_max), 1)[0] for i in self.parameter_list}

    def initial_conditions(self):
        """
        Input nodes get time 0 as initial conditions
        The rest are sampled N(mu, sd) of the input initial conditions
        :return:
        """


    def solve(self, initial_conditions, parameters):
        """

        :param initial_conditions:
        :param parameters:
        :return:
        """
        if not isinstance(initial_conditions, dict):
            raise TypeError('Input must be dict. Got "{}"'.format(type(initial_conditions)))

        if not isinstance(parameters, dict):
            raise TypeError('Input must be dict. Got "{}"'.format(type(parameters)))

        node_names = [i for i in self.ode.keys()]
        ode_list = [i for i in self.ode.values()]
        print(ode_list)
        NotImplementedError('Now make our new ODEs compatible with jitcode')
        SymbolicSys(ode_list)


























