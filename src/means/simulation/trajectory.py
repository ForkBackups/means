import operator
import numbers

import numpy as np

from means.io.serialise import SerialisableObject
from means.simulation import SensitivityTerm
from means.simulation.descriptors import PerturbedTerm


class Trajectory(SerialisableObject):
    """
    A single simulated or observed trajectory for an ODE term.
    """
    _timepoints = None
    _values = None
    _description = None

    yaml_tag = u'!trajectory'

    def __init__(self, timepoints, values, description):
        """

        :param timepoints: timepoints the trajectory was simulated for
        :type timepoints: :class:`iterable`
        :param values: values of the curve at each of the timepoints
        :type values: :class:`iterable`
        :param description: description of the trajectory
        :type description: :class:`~means.approximation.ode_problem.Descriptor`
        """
        self._timepoints = np.array(timepoints)
        self._values = np.array(values)
        self._description = description

        assert(self._timepoints.shape == self._values.shape)

    @property
    def timepoints(self):
        """
        The timepoints trajectory was simulated for.

        :rtype: :class:`numpy.ndarray`
        """
        return self._timepoints

    @property
    def values(self):
        """
        The values for each of the timepoints in :attr:`~Trajectory.timepoints`.

        :rtype: :class:`numpy.ndarray`
        """
        return self._values

    @property
    def description(self):
        """
        Description of this trajectory. The same description as the description for particular ODE term.

        :rtype: :class:`~means.approximation.ode_problem.ODETermBase`
        """
        return self._description

    def plot(self, *args, **kwargs):
        """
        Plots the trajectory using :mod:`matplotlib.pyplot`.

        :param args: arguments to pass to :func:`~matplotlib.pyplot.plot`
        :param kwargs: keyword arguments to pass to :func:`~matplotlib.pyplot.plot`
        :return: the result of the :func:`matplotlib.pyplot.plot` function.
        """
        from means.plotting.util import mathtextify
        from matplotlib import pyplot as plt
        # Get label from the kwargs provided, or use self.description as default
        label = kwargs.pop('label', mathtextify(self.description))
        # This is needed for matplotlib version 1.1.1
        label = str(label)
        return plt.plot(self.timepoints, self.values, *args, label=label, **kwargs)

    def resample(self, new_timepoints, extrapolate=False):
        if not extrapolate:
            if min(self.timepoints) > min(new_timepoints):
                raise Exception("Some of the new time points are before any time points. If you really want to extrapolate, use `extrapolate=True`")
            if max(self.timepoints) < max(new_timepoints):
                raise Exception("Some of the new time points are after any time points. If you really want to extrapolate, use `extrapolate=True`")
        new_values = np.interp(new_timepoints, self.timepoints, self.values)
        return Trajectory(new_timepoints, new_values, self.description)

    def __repr__(self):

        n_edge_items = 4
        precision = 3

        if len(self.timepoints) <= 2*n_edge_items:
            timepoint_to_print = ", ".join([str(round(i,precision)) for i in self.timepoints])
            values_to_print = ", ".join([str(round(i,precision)) for i in self.values])
        else:
            left_time = ", ".join([str(round(i,precision)) for i in self.timepoints[0: n_edge_items]])
            right_time = ", ".join([str(round(i,precision)) for i in self.timepoints[-n_edge_items: len(self.timepoints)]])

            timepoint_to_print = "{0}, ...,{1}".format(left_time, right_time)
            left_values = ", ".join([str(round(i,precision)) for i in self.values[0: n_edge_items]])
            right_values = ", ".join([str(round(i,precision)) for i in self.values[-n_edge_items: len(self.values)]])
            values_to_print = "{0}, ...,{1}".format(left_values, right_values)

        return '{0} object\ndescription: {1}\ntime points: [{2}]\nvalues: [{3}]'.format(
            self.__class__.__name__,
            self.description,
            timepoint_to_print,
            values_to_print)


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return np.equal(self.timepoints, other.timepoints).all() and np.equal(self.values, other.values).all() \
            and self.description == other.description

    def __add__(self, other):
        return self._arithmetic_operation(other, operator.add)
    def __div__(self, other):
        return self._arithmetic_operation(other, operator.div)
    def __mul__(self, other):
        return self._arithmetic_operation(other, operator.mul)
    def __sub__(self, other):
        return self._arithmetic_operation(other, operator.sub)
    def __pow__(self, other):
        return self._arithmetic_operation(other, operator.pow)

    def __radd__(self, other):
        # for `sum()`    to work
        return self + other


    def _arithmetic_operation(self, other, operation):
        """
        Applies an operation between the values of a trajectories and a scalar or between
        the respective values of two trajectories. In the latter case, trajectories should have
        equal descriptions and time points
        """
        if isinstance(other, Trajectory):
            if self.description != other.description:
                raise Exception("Cannot add trajectories with different descriptions")
            if not np.array_equal(self.timepoints, other.timepoints):
                raise Exception("Cannot add trajectories with different time points")
            new_values = operation(self.values, other.values)
        elif isinstance(other, numbers.Real):
            new_values = operation(self.values, float(other))
        else:
            raise Exception("Arithmetic operations is between two `Trajectory` objects or a `Trajectory` and a scalar.")

        return Trajectory(self.timepoints, new_values, self.description)


    @classmethod
    def to_yaml(cls, dumper, data):
        mapping = [('timepoints', data.timepoints),
                   ('values', data.values),
                   ('description', data.description)]

        return dumper.represent_mapping(cls.yaml_tag, mapping)

class TrajectoryWithSensitivityData(Trajectory):
    """
    An extension to :class:`~means.simulation.Trajectory` that provides data about the sensitivity
    of said trajectory as well.

    """

    _sensitivity_data = None
    yaml_tag = '!trajectory-with-sensitivity'

    def __init__(self, timepoints, values, description, sensitivity_data):
        """

        :param timepoints: timepoints the trajectory was simulated for
        :type timepoints: :class:`numpy.ndarray`
        :param values: values of the curve at each of the timepoints
        :type values: :class:`numpy.ndarray`
        :param description: description of the trajectory
        :type description: :class:`~means.approximation.ode_problem.Descriptor`
        :param sensitivity_data: a list of :class:`~means.approximation.simulation.simulate.Trajectory` objects
                                 signifying the sensitivity change over time for each of the parameters.
        :type sensitivity_data: list[:class:`~means.approximation.simulation.simulate.Trajectory`]
        """
        super(TrajectoryWithSensitivityData, self).__init__(timepoints, values, description)
        self._sensitivity_data = sensitivity_data

    @classmethod
    def from_trajectory(cls, trajectory, sensitivity_data):
        return cls(trajectory.timepoints, trajectory.values, trajectory.description, sensitivity_data)

    @property
    def sensitivity_data(self):
        """
        THe sensitivity data for the trajectory

        :rtype: list[:class:`~means.approximation.simulation.simulate.Trajectory`]
        """
        return self._sensitivity_data

    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
               super(TrajectoryWithSensitivityData, self).__eq__(other) and \
               self.sensitivity_data == other.sensitivity_data

    def plot_perturbations(self, parameter, delta=1e-4, *args, **kwargs):
        from matplotlib import pyplot as plt
        alpha = kwargs.pop('alpha', 0.1)
        for sensitivity_trajectory in self.sensitivity_data:
            description_parameter = sensitivity_trajectory.description.parameter
            # Compare them as strings so it is easier to pass it in
            if str(sensitivity_trajectory.description.parameter) != str(parameter):
                continue

            perturbed_trajectory_positive = perturbed_trajectory(self, sensitivity_trajectory, delta=delta)
            perturbed_trajectory_negative = perturbed_trajectory(self, sensitivity_trajectory, delta=-delta)
            plt.fill_between(self.timepoints,
                             perturbed_trajectory_negative.values,
                             perturbed_trajectory_positive.values,
                             alpha=alpha,
                             *args,
                             **kwargs)

            label = kwargs.pop('label', "${0}$, "
                                        "when ${1}$ is perturbed by ${2}$".format(self.description.symbol,
                                                                                  sensitivity_trajectory.description.parameter,
                                                                                  delta))
            # This is needed for matplotlib version 1.1.1
            label = str(label)
            # Fill_between does not generate a legend entry, use this hack with Rectangle to do this
            plt.gca().add_patch(plt.Rectangle((0, 0), 0, 0, alpha=alpha,
                                              label=label,
                                                    *args, **kwargs))

    @classmethod
    def to_yaml(cls, dumper, data):
        mapping = [('timepoints', data.timepoints),
                   ('values', data.values),
                   ('description', data.description),
                   ('sensitivity_data', data.sensitivity_data)]
        return dumper.represent_mapping(cls.yaml_tag, mapping)


def perturbed_trajectory(trajectory, sensitivity_trajectory, delta=1e-4):
    """
    Slightly perturb trajectory wrt the parameter specified in sensitivity_trajectory.

    :param trajectory: the actual trajectory for an ODE term
    :type trajectory: :class:`Trajectory`
    :param sensitivity_trajectory: sensitivity trajectory (dy/dpi for all timepoints t)
    :type sensitivity_trajectory: :class:`Trajectory`
    :param delta: the perturbation size
    :type delta: float
    :return: :class:`Trajectory`
    """
    sensitivity_trajectory_description = sensitivity_trajectory.description
    assert(isinstance(sensitivity_trajectory_description, SensitivityTerm))
    assert(np.equal(trajectory.timepoints, sensitivity_trajectory.timepoints).all())

    return Trajectory(trajectory.timepoints,
                      trajectory.values + sensitivity_trajectory.values * delta,
                      PerturbedTerm(sensitivity_trajectory_description.ode_term,
                                    sensitivity_trajectory_description.parameter,
                                    delta))
