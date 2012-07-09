from unittest import TestCase as TC
import nk_model
from nk_model import *
from bitstring import Bitstring


class TestSimpleNKModel(TC):
    def test_init(self):
        dep = [[0, 1], [1, 0]]
        clt = [[1, 2, 3, 4], [5, 6, 7, 8]]
        model = NKModelSimple(dep, clt)
        self.assertEqual(dep, model.dependancy_lists)
        self.assertEqual(clt, model.contribution_lookup_tables)

    def test_calculate_fitness_hard(self):
        dep = [[0, 1], [1, 0], [2, 1]]
        clt = [[.1, .2, .3, .4], [.5, .6, .7, .8], [.9, 1.0, .15, .25]]
        model = NKModelSimple(dep, clt)
        bs = Bitstring("010")
        expected_fitness = (.3 + .7 + .15) / 3.0
        self.assertAlmostEqual(expected_fitness, model.calculate_fitness(bs))

    def test_calculate_fitness_easy(self):
        model = NKModelSimple([[0], [1]], [[.2, .3], [.6, .7]])
        bs = Bitstring("01")
        expected_fitness = (.3 + .6) / 2.0
        self.assertAlmostEqual(expected_fitness, model.calculate_fitness(bs))


class TestNKModelFactory(TC):
    def setUp(self):
        self.factory = NKModelFactory()

    def test_no_dependancies(self):
        smooth_nk = self.factory.no_dependancies(2)
        self.assertEqual(smooth_nk.dependancy_lists, [[0], [1]])
        self.assertEqual(len(smooth_nk.contribution_lookup_tables), 2)
        self.assertEqual(len(smooth_nk.contribution_lookup_tables[0]), 2)
        self.assertEqual(len(smooth_nk.contribution_lookup_tables[1]), 2)

    def test_model_with_uniform_contribution_lookup_table(self):
        dep_lists = [[0, 1], [1, 2, 3], [4]]
        model = self.factory._model_with_uniform_contribution_lookup_table(dep_lists)
        clt = model.contribution_lookup_tables
        self.assertEqual(len(clt), 3)
        self.assertEqual(len(clt[0]), 4)
        self.assertEqual(len(clt[1]), 8)
        self.assertEqual(len(clt[2]), 2)

    def test_max_depandancies(self):
        model = self.factory.max_dependancies(6)
        deps = model.dependancy_lists
        self.assertEqual(6, len(deps))
        self.assertEqual(deps[0], list(range(6)))
        self.assertEqual(deps[-1], [5, 0, 1, 2, 3, 4])

    def test_consecutive_dependancies(self):
        model = self.factory.consecutive_dependancies(6, 2)
        deps = model.dependancy_lists
        self.assertEqual(6, len(deps))
        self.assertEqual(deps[0], list(range(3)))
        self.assertEqual(deps[-1], [5, 0, 1])



class NotTestNKModel(object):
    def setUp(self):
        self.clt_smooth = [[.25, .75], [.4, .8]]
        self.smooth = NKModel(2, 0, self.clt_smooth)
        self.clt_rugged = [[.25, .75, .1, 0], [.4, .8, .6, .7]]
        self.rugged = NKModel(2, 1, self.clt_rugged)

    def test_init(self):
        nk = NKModel()
        self.assertEqual(nk.n, 2)
        self.assertEqual(nk.k, 0)
        nk2 = NKModel(4, 3)
        self.assertEqual(nk2.n, 4)
        self.assertEqual(nk2.k, 3)
        nk3 = NKModel(k=6, n=10)
        self.assertEqual(nk3.n, 10)
        self.assertEqual(nk3.k, 6)

    def test_init_table(self):
        self.assertEqual(
            self.smooth.contribution_lookup_table, self.clt_smooth)

    def test_determine_fitness(self):
        b = Bitstring("01")
        smooth_fit = self.smooth.determine_fitness(b)
        expected_smooth_fit = (.75 + .4) / 2
        self.assertEqual(smooth_fit, expected_smooth_fit)
        rugged_fit = self.rugged.determine_fitness(b)
        expected_rugged_fit = (.1 + .8) / 2
        self.assertEqual(rugged_fit, expected_rugged_fit)

    def test_determine_fitness_from_random(self):
        b = Bitstring("01")
        rug_fit = self.rugged.determine_fitness_from_random(b)
        expected_rugged_fit = (.1 + .8) / 2
        self.assertEqual(rug_fit, expected_rugged_fit)


class NotTestModuleWitoutGenes(object):

    def test_get_substring_with_wrapping(self):
        b = Bitstring("00111")
        sub1 = get_substring_with_wrapping(b, k=3, i=1)
        self.assertEqual(Bitstring("1100"), sub1)
        sub2 = get_substring_with_wrapping(b, k=3, i=2)
        self.assertEqual(Bitstring("1001"), sub2)
        sub3 = get_substring_with_wrapping(b, k=3, i=3)
        self.assertEqual(Bitstring("0011"), sub3)

    def test_deconstruct_bitstring(self):
        B = Bitstring
        b = B("11001")
        subs = deconstruct_bitstring(b, 3)
        expected = [B("1100"), B("1001"),
                    B("0011"), B("0111"),
                    B("1110")]
        self.assertEqual(subs, expected)

    def test_deconstruct_random(self):
        B = Bitstring
        b = Bitstring("100")
        l = determine_inner_dependencies(3,2)
        sub = decontruct_random_bitstring(b, l)
        self.assertEqual(3, len(sub))
        self.assertEqual(sub[0], B("100"))

    def test_inner_dependencies(self):
        l = determine_inner_dependencies(4, 2)
        self.assertEqual(len(l), 4)
        self.assertEqual(len(l[0]), 3)
        self.assertEqual(l[0][0], 0)

class NotTestNKWithGenes(object):
    def setUp(self):
        self.list_of_strings = [Bitstring("010"), Bitstring("100"),
                           Bitstring("001")]

    def test_determine_fitness(self):
        contrib_table = [[0.25, 0.8, 0.15], [0.9, 0.4, 0.55], [0.05, 0.7, 0.3]]
        nk = NKWithGenes(1, 0, 2, 2)
        bit_org = Bitstring("0101")
        self.assertNotEqual(0, nk.determine_fitness(bit_org))

    def test_passed_contribution_table(self):
        contrib_table = generate_contribution_lookup_table(3, 2)
        nk = NKWithGenes(1, 1, 2, 2, contrib_table)
        self.assertEqual(contrib_table, nk.contribution_lookup_table)

    def test_gene_divider(self):
        gene = Bitstring("101010101010")
        nk = NKWithGenes(2, 2, 3, 4)
        divided = nk.divide_to_genes(gene)
        self.assertEqual(len(divided), 4)
        self.assertEqual(len(divided[0]), 3)
        self.assertEqual(Bitstring("010"), divided[-1])

class NotTestModuleWithGenes(object):
    def setUp(self):
        self.depend = generate_dependencies(2, 2, 3, 3)
        self.list_of_strings = [Bitstring("010"), Bitstring("100"),
                           Bitstring("001")]

    def test_dependencies(self):
        long_depend = generate_dependencies(2, 4, 3, 3)
        self.assertEqual(len(long_depend), 3)
        self.assertEqual(len(long_depend[0]), 3)
        self.assertEqual(len(long_depend[-1]), 3)

    def test_passed_depend(self):
        dependencies = [[[(2, 0), (1, 2)], [(1, 1), (2, 1)],[(1, 0), (2, 2)]],
                        [[(1, 2), (1, 1)], [(0, 0), (1, 1)], [(0, 1), (0, 1)]],
                        [[(2, 2), (2, 0)], [(2, 2), (2, 0)], [(1, 1), (0, 1)]]]
        subs = generate_sub_bitstring(self.list_of_strings,
                                                          dependencies, 2)
        self.assertEqual(subs[0][1], Bitstring("10000"))

    def test_sub_bitstring(self):

        full = generate_sub_bitstring(self.list_of_strings,
                                                           self.depend, 2)
        self.assertEqual(len(full), len(self.list_of_strings))
        self.assertEqual(len(full[0]), 3)
        self.assertEqual(len(full[0][0]), 5)

    def test_linear_jump(self):
        linear_model = generate_linear_bistring(
            self.list_of_strings, 2, 1)
        self.assertEqual(4, len(linear_model[0][0]))
        self.assertEqual(3, len(linear_model))
        self.assertEqual(3, len(linear_model[0]))
        self.assertEqual(Bitstring("0101"), linear_model[0][0])
