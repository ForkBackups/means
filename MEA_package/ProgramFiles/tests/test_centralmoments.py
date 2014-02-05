import unittest
import sympy
from centralmoments import eq_centralmoments
from ode_problem import Moment

class CentralMomentsTestCase(unittest.TestCase):
    def test_centralmoments_using_p53model(self):
        """
        Given the p53 model hard codded bellow,the result of central moment should match exactly the expected one
        :return:
        """
        counter_nvecs = [[0, 0, 0], [0, 0, 2], [0, 1, 1], [0, 2, 0], [1, 0, 1], [1, 1, 0], [2, 0, 0]]

        mcounter_nvecs = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [1, 0, 0], [0, 0, 2], [0, 1, 1], [0, 2, 0],
                    [1, 0, 1], [1, 1, 0], [2, 0, 0]]

        counter = [Moment(c,sympy.Symbol("YU{0}".format(i))) for i,c in enumerate(counter_nvecs)]
        mcounter = [Moment(c,sympy.Symbol("y_{0}".format(i))) for i,c in enumerate(mcounter_nvecs)]

        m = sympy.Matrix([
                              ['c_0 - c_1*y_0 - c_2*y_0*y_2/(c_6 + y_0)',
                               0,
                               0,
                               0,
                               'c_2*y_0/(c_6 + y_0)**2 - c_2/(c_6 + y_0)',
                               0,
                               '-c_2*y_0*y_2/(c_6 + y_0)**3 + c_2*y_2/(c_6 + y_0)**2'],
                         [
                              'c_3*y_0 - c_4*y_1',
                              0,
                              0,
                              0,
                              0,
                              0,
                              0],
                          [
                              'c_4*y_1 - c_5*y_2',
                              0,
                              0,
                              0,
                              0,
                              0,
                              0
                          ]])
        species = sympy.Matrix(['y_0', 'y_1', 'y_2'])
        propensities = sympy.Matrix(['c_0',
                                                        'c_1 * y_0',
                                                        'c_2*y_0*y_2/(c_6 + y_0)',
                                                        'c_3*y_0',
                                                        'c_4*y_1',
                                                        'c_5*y_2'])

        stoichiometry_matrix = sympy.Matrix([[1, -1, -1, 0, 0, 0],
                                             [0, 0, 0, 1, -1, 0],
                                             [0, 0, 0, 0, 1, -1]])


        answer = eq_centralmoments(counter, mcounter, m, species, propensities, stoichiometry_matrix)

        expected = sympy.Matrix([
            [" 2*c_4*y_1*y_2 + c_4*y_1 - 2*c_5*y_2**2 + c_5*y_2 - 2*y_1*(c_4*y_1 - c_5*y_2)","               -2*c_5","                2*c_4","      0","                                                                                                                                                 0","                                                             0","                                                                                                                                                                                                                    0"],
            ["c_3*y_0*y_2 + c_4*y_1**2 - c_4*y_1*y_2 - c_4*y_1 - c_5*y_1*y_2 - y_1*(c_3*y_0 - c_4*y_1) - y_2*(c_4*y_1 - c_5*y_2)","                    0","           -c_4 - c_5","    c_4","                                                                                                                                               c_3","                                                             0","                                                                                                                                                                                                                    0"],
            ["2*c_3*y_0*y_1 + c_3*y_0 - 2*c_4*y_1**2 + c_4*y_1 - 2*y_2*(c_3*y_0 - c_4*y_1)","                    0","                    0"," -2*c_4","                                                                                                                                                 0","                                                         2*c_3","0"],
            ["c_0*y_2 - c_1*y_0*y_2 - c_2*y_0*y_2**2/(c_6 + y_0) + c_4*y_0*y_1 - c_5*y_0*y_2 - y_1*(c_0 - c_1*y_0 - c_2*y_0*y_2/(c_6 + y_0)) - y_3*(c_4*y_1 - c_5*y_2)"," -c_2*y_0/(c_6 + y_0)","                    0","      0","                                -c_1 + 2*c_2*y_0*y_2/(c_6 + y_0)**2 - 2*c_2*y_2/(c_6 + y_0) - c_5 - y_1*(c_2*y_0/(c_6 + y_0)**2 - c_2/(c_6 + y_0))","c_4","                                                                                              -c_2*y_0*y_2**2/(c_6 + y_0)**3 + c_2*y_2**2/(c_6 + y_0)**2 - y_1*(-c_2*y_0*y_2/(c_6 + y_0)**3 + c_2*y_2/(c_6 + y_0)**2)"],
            ["c_0*y_1 - c_1*y_0*y_1 - c_2*y_0*y_1*y_2/(c_6 + y_0) + c_3*y_0**2 - c_4*y_0*y_1 - y_2*(c_0 - c_1*y_0 - c_2*y_0*y_2/(c_6 + y_0)) - y_3*(c_3*y_0 - c_4*y_1)","                    0"," -c_2*y_0/(c_6 + y_0)","      0","                                                 c_2*y_0*y_1/(c_6 + y_0)**2 - c_2*y_1/(c_6 + y_0) - y_2*(c_2*y_0/(c_6 + y_0)**2 - c_2/(c_6 + y_0))"," -c_1 + c_2*y_0*y_2/(c_6 + y_0)**2 - c_2*y_2/(c_6 + y_0) - c_4","                                                                                      -c_2*y_0*y_1*y_2/(c_6 + y_0)**3 + c_2*y_1*y_2/(c_6 + y_0)**2 + c_3 - y_2*(-c_2*y_0*y_2/(c_6 + y_0)**3 + c_2*y_2/(c_6 + y_0)**2)"],
            ["2*c_0*y_0 + c_0 - 2*c_1*y_0**2 + c_1*y_0 - 2*c_2*y_0**2*y_2/(c_6 + y_0) + c_2*y_0*y_2/(c_6 + y_0) - 2*y_3*(c_0 - c_1*y_0 - c_2*y_0*y_2/(c_6 + y_0))","                    0","                    0","      0"," 2*c_2*y_0**2/(c_6 + y_0)**2 - 4*c_2*y_0/(c_6 + y_0) - c_2*y_0/(c_6 + y_0)**2 + c_2/(c_6 + y_0) - 2*y_3*(c_2*y_0/(c_6 + y_0)**2 - c_2/(c_6 + y_0))","                                                             0"," -2*c_1 - 2*c_2*y_0**2*y_2/(c_6 + y_0)**3 + 4*c_2*y_0*y_2/(c_6 + y_0)**2 + c_2*y_0*y_2/(c_6 + y_0)**3 - 2*c_2*y_2/(c_6 + y_0) - c_2*y_2/(c_6 + y_0)**2 - 2*y_3*(-c_2*y_0*y_2/(c_6 + y_0)**3 + c_2*y_2/(c_6 + y_0)**2)"]
       ])

        self.assertEqual(answer, expected)

    def test_centralmoments_using_MM_model(self):
        """
        Given the MM model hard codded bellow,the result of central moment should match exactly the expected one
        :return:
        """
        counter_nvecs = [[0, 0], [0, 2], [1, 1], [2, 0]]
        mcounter_nvecs = [[0, 0], [0, 1], [1, 0], [0, 2], [1, 1], [2, 0]]

        counter = [Moment(c,sympy.Symbol("YU{0}".format(i))) for i,c in enumerate(counter_nvecs)]
        mcounter = [Moment(c,sympy.Symbol("y_{0}".format(i))) for i,c in enumerate(mcounter_nvecs)]

        m = sympy.Matrix([
                              ['-c_0*y_0*(y_0 + y_1 - 181) + c_1*(-y_0 - y_1 + 301)',
                               0,
                               '-c_0',
                               '-c_0'],
                          [
                              'c_2*(-y_0 - y_1 + 301)',
                              0,
                              0,
                              0]
        ])


        species = sympy.Matrix(map(sympy.var, ['y_0', 'y_1']))

        propensities = sympy.Matrix(['c_0*y_0*(y_0 + y_1 - 181)',
                                                        'c_1*(-y_0 - y_1 + 301)',
                                                        'c_2*(-y_0 - y_1 + 301)'])

        stoichiometry_matrix = sympy.Matrix([[-1, 1, 0],
                                             [0, 0, 1]])

        expected = sympy.Matrix([
        ["c_2*(-y_0 - y_1 + 301)"," -2*c_2"," -2*c_2"," 0"],
        ["-c_0*y_0*y_1*(y_0 + y_1 - 181) + c_1*y_1*(-y_0 - y_1 + 301) + c_2*y_0*(-y_0 - y_1 + 301) - c_2*y_2*(-y_0 - y_1 + 301) - y_1*(-c_0*y_0*(y_0 + y_1 - 181) + c_1*(-y_0 - y_1 + 301))"," -c_0*y_0 - c_1"," -c_0*y_0 - c_0*(y_0 + y_1 - 181) - c_1 - c_2"," -c_2"],
        ["-2*c_0*y_0**2*(y_0 + y_1 - 181) + c_0*y_0*(y_0 + y_1 - 181) + 2*c_1*y_0*(-y_0 - y_1 + 301) + c_1*(-y_0 - y_1 + 301) - 2*y_2*(-c_0*y_0*(y_0 + y_1 - 181) + c_1*(-y_0 - y_1 + 301))"," 0"," -4*c_0*y_0 + 2*c_0*y_2 + c_0 - 2*c_1"," -4*c_0*y_0 + 2*c_0*y_2 - 2*c_0*(y_0 + y_1 - 181) + c_0 - 2*c_1"]
        ])
        answer = eq_centralmoments(counter, mcounter, m, species, propensities, stoichiometry_matrix)
        self.assertEqual(answer, expected)