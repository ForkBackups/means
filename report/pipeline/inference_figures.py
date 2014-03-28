from means import TrajectoryCollection, SolverException
from means.pipes import *
import numpy as np


from means.util.logs import get_logger
logger = get_logger(__name__)

class P53Model(means.Model):
    """
    A wrapper around means. Model that initialises it with P53 parameters and changes the __unicode__ function to
    print a shorter string
    """
    def __init__(self):
        from means.examples import MODEL_P53
        super(P53Model, self).__init__(MODEL_P53.species, MODEL_P53.parameters, MODEL_P53.propensities,
                                       MODEL_P53.stoichiometry_matrix)

    def __str__(self):
        # Override the str() methods so they do not print the whole blerch of things, but
        # only a nice and easily readable "p53"
        return 'p53'

class SampleObservedTrajectory(means.Trajectory):

    def __init__(self):
        values = [70.0, 69.033486295361868, 68.378006473997928, 68.081347037849596, 67.998126990007663, 68.001242363319562, 68.264974260383141, 68.512598398035323, 68.822132540463585, 68.975317248395555, 69.182423580483572, 69.183703342638367, 69.060135757979126, 68.912472802719194, 68.501199295306151, 67.984395247245061, 67.410836287406369, 66.709203292194616, 65.72569450803455, 64.643672659257717, 63.459591001199698, 62.091634276551005, 60.635433365799123, 59.027792759891462, 57.258295753217091, 55.538378980993691, 53.588832482636128, 51.625278035022788, 49.60962314775707, 47.527138731188074, 45.527566235011761, 43.53394331160785, 41.665276643737123, 39.826240478533201, 38.135486821978915, 36.480358187577394, 35.020053112878372, 33.656515366386024, 32.413359604841375, 31.387573561165301, 30.420295998780446, 29.753160900799056, 29.307353045947245, 28.869229708988573, 28.6980855385961, 28.664676455945649, 28.749462074560505, 29.06648325774395, 29.373783119914343, 29.9248013074019, 30.62867450337945, 31.506970218949661, 32.468608874920129, 33.515355129260406, 34.648753953497121, 35.974235750348591, 37.406252743572352, 38.828345981094614, 40.348139130869662, 41.969771378981626, 43.590460162811816, 45.1838188684792, 46.896743600932354, 48.530960671527815, 50.121625800548216, 51.741233120278729, 53.23374178607493, 54.77547451143117, 56.089534626886319, 57.50168606936807, 58.715866965798391, 59.734709284057658, 60.740849996880037, 61.501476236555817, 62.256616342888037, 62.83662723523431, 63.276078984656081, 63.681732634073462, 63.861423637890724, 63.904552865144588, 63.721509752105128, 63.522398888443121, 63.071135565147948, 62.483790887723188, 61.787720609592775, 61.025371147102511, 59.986523432525203, 58.969951633468469, 57.695667717408469, 56.455683052511581, 55.208755846736288, 53.932897544806337, 52.525162037137783, 51.044218892556053, 49.60384228329081, 48.018612702514623, 46.519943336206524, 45.0869921626795, 43.652354413341307, 42.33828036982684, 40.994132825462096, 39.739808578682101, 38.725381622871545, 37.771981128767301, 36.783078499354446, 36.085206523830252, 35.498263074347228, 34.927199205165685, 34.466104620823977, 34.235251436533467, 34.113569637046979, 34.057128588041301, 34.09688617629898, 34.324792997143589, 34.570086529259321, 35.048488857665951, 35.584251374289472, 36.199945092734382, 36.922050840084182, 37.681018450173489, 38.551700121330214, 39.394860281480362, 40.480280855155911, 41.474614088293393, 42.530122496026465, 43.76449029946297, 44.915908351732114, 46.061261370821079, 47.138375115668055, 48.166696246637812, 49.293044569805609, 50.331300192182049, 51.424019790742712, 52.364158412632477, 53.258886892912756, 54.24271412960335, 55.064538402502841, 55.875165986166252, 56.603765590642965, 57.294181910865987, 57.757382524579171, 58.143318531368443, 58.57380723338057, 58.820468146754685, 58.917990735895067, 58.97960541373952, 58.980823268061897, 58.738941290574076, 58.436155513298282, 57.996090548656348, 57.606716979488205, 57.177425112688312, 56.510972966508099, 55.861822296339994, 55.067783794779089, 54.316360234548853, 53.447026965715686, 52.523832004539983, 51.634568240172023, 50.816504020162405, 49.912047745727484, 48.847101350883229, 47.920514156781451, 46.895753787835964, 45.949269146893194, 45.049950427931691, 44.231723744300041, 43.337399651407104, 42.495887166190535, 41.85886268848116, 41.0900038182617, 40.492728475424485, 39.982292207987499, 39.517755983715141, 39.099395021817429, 38.795991491011208, 38.573169136966143, 38.488707823054604, 38.612966770483247, 38.569506715763019, 38.741794297554442, 38.769393173887764, 39.019453989747426, 39.381202545211828, 39.879761822212579, 40.373334874486815, 40.835399522858737, 41.546530328367567, 42.185365286940574, 42.963495143979578, 43.582989740038592, 44.284946580718511, 45.027448813843968, 45.755146117506506, 46.588347897987717, 47.402963940835711, 48.2220240675355, 48.968031574783275, 49.715359820778723, 50.375056594630763, 50.983683190108309, 51.628351630078399, 52.334037471178668, 52.934871105377361, 53.408930097927374, 53.806000642978915, 54.14321694567159, 54.475584872092973, 54.688658019162425, 54.89053600802346, 55.020184339030905, 55.143221910589034, 55.037443298506979, 54.979890732211715, 54.86080224349103, 54.828990564572322, 54.551101023791233, 54.276606224432378, 53.845602863744602, 53.457813982151563, 52.935772171907068, 52.478745832311795, 51.929637929943887, 51.382511657829404, 50.826085736166156, 50.160546443950224, 49.579385210948203, 48.890333112109765, 48.237697734683529, 47.677687816771943, 47.058566643122418, 46.427007282817009, 45.780837089338931, 45.167213641833918, 44.701099283212059, 44.045167413175456, 43.665346917777121, 43.288897532364622, 42.86172945216142, 42.573902513702265, 42.29785339076426, 42.074641491360943, 41.903505840831876, 41.902093900018343, 41.836557851553103, 41.818530649858111, 41.922788056483263, 42.064855477519075, 42.220496155528387, 42.358504266781281, 42.658280789191132, 42.917941732100765, 43.314432165345728, 43.660939917753794, 44.106270685568191, 44.505265919581269, 44.929038082410379, 45.393954909115806, 45.805295608921575, 46.355858414588951, 46.876693292074371, 47.474506729430573, 48.030226073338014, 48.445378385540508, 48.953885346948312, 49.426811952921796, 49.834164470330997, 50.100585672437688, 50.497960641939947, 50.795925615830193, 51.131559833530083, 51.520087307926701, 51.671411045842021, 51.865319807676677, 52.113937920460444, 52.249946684269219, 52.386741416834361, 52.360811842553453, 52.3734178597362, 52.40146332841973, 52.31074925147739, 52.114456963076201, 51.991812790244857, 51.813433082427323, 51.558302184022367, 51.233070605614621, 50.937118009657588, 50.621234633084192, 50.244635075071386, 49.88114907098889, 49.613817414717964, 49.122805737543572, 48.808764395920079, 48.402971714841406, 48.041728459996442, 47.739356358709827, 47.335176213415522, 47.003318688453319, 46.617570406475046, 46.279055378837242, 45.959895779801251, 45.645034275997986, 45.293986453439764, 44.984735615558854, 44.741774969618554, 44.447853678073201, 44.309298696906531, 44.089219579197277, 43.968654961780736, 43.888512893077838, 43.947446121959047, 44.079280119123354, 44.009325301110913, 44.085269572707581, 44.144812203299715, 44.274634517009432, 44.461543540339044, 44.574481008662353, 44.800396058707257, 45.016055558308601, 45.184927333236224, 45.39069903318925, 45.632643840353886, 45.856381217987767, 46.005271644618148, 46.397847658719435, 46.688028471084593, 46.97516900256322, 47.326965391914911, 47.692885579184193, 47.956118758895059, 48.292406632592311, 48.546629388524671, 48.880465859197834, 49.060563500544681, 49.266271095259548, 49.608143594369928, 49.954652018288115, 50.204847768780027, 50.473266885046506, 50.530591513279546, 50.718697915717804, 50.841606779573389, 50.93774928415877, 50.929975885943357, 50.938498663093554, 50.857796788023634, 50.786693972237124, 50.764542158176333, 50.65462725381883, 50.510627434940083, 50.367767911578873, 50.225697493882514, 50.103499147433006, 49.934943562879631, 49.850402702165972, 49.578243388896368, 49.257997586676218, 48.963298752467921, 48.635601727219587, 48.419692018589814, 48.193663433206865, 47.853596414061222, 47.557786138404992, 47.233333862757853, 47.009014553386464, 46.765767734992146, 46.48976527035051, 46.303552023752879, 46.086368881699038, 45.913408084694758, 45.831494973808532, 45.697724014136384, 45.580138124654646, 45.386078727791272, 45.202160926728816, 45.058620968097593, 45.004243651295731, 45.073681621136629, 45.142461653249491, 45.104911642403771, 45.059996433996474, 45.13211288755722, 45.239603296116265, 45.277210036109238, 45.382187637846187, 45.6000480604242, 45.809610981218199, 46.004410719504932, 46.240247605704688, 46.452762595118067, 46.704349355249057, 46.933199638430033, 47.148326840826662, 47.44889175534599, 47.71483062899383, 47.971500222400834, 48.132082888401555, 48.274273252353545, 48.481711602616819]
        description = means.Moment(np.array([1, 0, 0]), symbol='y_0')
        timepoints = [0.0, 0.10000000000000001, 0.20000000000000001, 0.30000000000000004, 0.40000000000000002, 0.5, 0.60000000000000009, 0.70000000000000007, 0.80000000000000004, 0.90000000000000002, 1.0, 1.1000000000000001, 1.2000000000000002, 1.3, 1.4000000000000001, 1.5, 1.6000000000000001, 1.7000000000000002, 1.8, 1.9000000000000001, 2.0, 2.1000000000000001, 2.2000000000000002, 2.3000000000000003, 2.4000000000000004, 2.5, 2.6000000000000001, 2.7000000000000002, 2.8000000000000003, 2.9000000000000004, 3.0, 3.1000000000000001, 3.2000000000000002, 3.3000000000000003, 3.4000000000000004, 3.5, 3.6000000000000001, 3.7000000000000002, 3.8000000000000003, 3.9000000000000004, 4.0, 4.1000000000000005, 4.2000000000000002, 4.2999999999999998, 4.4000000000000004, 4.5, 4.6000000000000005, 4.7000000000000002, 4.8000000000000007, 4.9000000000000004, 5.0, 5.1000000000000005, 5.2000000000000002, 5.3000000000000007, 5.4000000000000004, 5.5, 5.6000000000000005, 5.7000000000000002, 5.8000000000000007, 5.9000000000000004, 6.0, 6.1000000000000005, 6.2000000000000002, 6.3000000000000007, 6.4000000000000004, 6.5, 6.6000000000000005, 6.7000000000000002, 6.8000000000000007, 6.9000000000000004, 7.0, 7.1000000000000005, 7.2000000000000002, 7.3000000000000007, 7.4000000000000004, 7.5, 7.6000000000000005, 7.7000000000000002, 7.8000000000000007, 7.9000000000000004, 8.0, 8.0999999999999996, 8.2000000000000011, 8.3000000000000007, 8.4000000000000004, 8.5, 8.5999999999999996, 8.7000000000000011, 8.8000000000000007, 8.9000000000000004, 9.0, 9.0999999999999996, 9.2000000000000011, 9.3000000000000007, 9.4000000000000004, 9.5, 9.6000000000000014, 9.7000000000000011, 9.8000000000000007, 9.9000000000000004, 10.0, 10.100000000000001, 10.200000000000001, 10.300000000000001, 10.4, 10.5, 10.600000000000001, 10.700000000000001, 10.800000000000001, 10.9, 11.0, 11.100000000000001, 11.200000000000001, 11.300000000000001, 11.4, 11.5, 11.600000000000001, 11.700000000000001, 11.800000000000001, 11.9, 12.0, 12.100000000000001, 12.200000000000001, 12.300000000000001, 12.4, 12.5, 12.600000000000001, 12.700000000000001, 12.800000000000001, 12.9, 13.0, 13.100000000000001, 13.200000000000001, 13.300000000000001, 13.4, 13.5, 13.600000000000001, 13.700000000000001, 13.800000000000001, 13.9, 14.0, 14.100000000000001, 14.200000000000001, 14.300000000000001, 14.4, 14.5, 14.600000000000001, 14.700000000000001, 14.800000000000001, 14.9, 15.0, 15.100000000000001, 15.200000000000001, 15.300000000000001, 15.4, 15.5, 15.600000000000001, 15.700000000000001, 15.800000000000001, 15.9, 16.0, 16.100000000000001, 16.199999999999999, 16.300000000000001, 16.400000000000002, 16.5, 16.600000000000001, 16.699999999999999, 16.800000000000001, 16.900000000000002, 17.0, 17.100000000000001, 17.199999999999999, 17.300000000000001, 17.400000000000002, 17.5, 17.600000000000001, 17.699999999999999, 17.800000000000001, 17.900000000000002, 18.0, 18.100000000000001, 18.199999999999999, 18.300000000000001, 18.400000000000002, 18.5, 18.600000000000001, 18.699999999999999, 18.800000000000001, 18.900000000000002, 19.0, 19.100000000000001, 19.200000000000003, 19.300000000000001, 19.400000000000002, 19.5, 19.600000000000001, 19.700000000000003, 19.800000000000001, 19.900000000000002, 20.0, 20.100000000000001, 20.200000000000003, 20.300000000000001, 20.400000000000002, 20.5, 20.600000000000001, 20.700000000000003, 20.800000000000001, 20.900000000000002, 21.0, 21.100000000000001, 21.200000000000003, 21.300000000000001, 21.400000000000002, 21.5, 21.600000000000001, 21.700000000000003, 21.800000000000001, 21.900000000000002, 22.0, 22.100000000000001, 22.200000000000003, 22.300000000000001, 22.400000000000002, 22.5, 22.600000000000001, 22.700000000000003, 22.800000000000001, 22.900000000000002, 23.0, 23.100000000000001, 23.200000000000003, 23.300000000000001, 23.400000000000002, 23.5, 23.600000000000001, 23.700000000000003, 23.800000000000001, 23.900000000000002, 24.0, 24.100000000000001, 24.200000000000003, 24.300000000000001, 24.400000000000002, 24.5, 24.600000000000001, 24.700000000000003, 24.800000000000001, 24.900000000000002, 25.0, 25.100000000000001, 25.200000000000003, 25.300000000000001, 25.400000000000002, 25.5, 25.600000000000001, 25.700000000000003, 25.800000000000001, 25.900000000000002, 26.0, 26.100000000000001, 26.200000000000003, 26.300000000000001, 26.400000000000002, 26.5, 26.600000000000001, 26.700000000000003, 26.800000000000001, 26.900000000000002, 27.0, 27.100000000000001, 27.200000000000003, 27.300000000000001, 27.400000000000002, 27.5, 27.600000000000001, 27.700000000000003, 27.800000000000001, 27.900000000000002, 28.0, 28.100000000000001, 28.200000000000003, 28.300000000000001, 28.400000000000002, 28.5, 28.600000000000001, 28.700000000000003, 28.800000000000001, 28.900000000000002, 29.0, 29.100000000000001, 29.200000000000003, 29.300000000000001, 29.400000000000002, 29.5, 29.600000000000001, 29.700000000000003, 29.800000000000001, 29.900000000000002, 30.0, 30.100000000000001, 30.200000000000003, 30.300000000000001, 30.400000000000002, 30.5, 30.600000000000001, 30.700000000000003, 30.800000000000001, 30.900000000000002, 31.0, 31.100000000000001, 31.200000000000003, 31.300000000000001, 31.400000000000002, 31.5, 31.600000000000001, 31.700000000000003, 31.800000000000001, 31.900000000000002, 32.0, 32.100000000000001, 32.200000000000003, 32.300000000000004, 32.399999999999999, 32.5, 32.600000000000001, 32.700000000000003, 32.800000000000004, 32.899999999999999, 33.0, 33.100000000000001, 33.200000000000003, 33.300000000000004, 33.399999999999999, 33.5, 33.600000000000001, 33.700000000000003, 33.800000000000004, 33.899999999999999, 34.0, 34.100000000000001, 34.200000000000003, 34.300000000000004, 34.399999999999999, 34.5, 34.600000000000001, 34.700000000000003, 34.800000000000004, 34.899999999999999, 35.0, 35.100000000000001, 35.200000000000003, 35.300000000000004, 35.399999999999999, 35.5, 35.600000000000001, 35.700000000000003, 35.800000000000004, 35.899999999999999, 36.0, 36.100000000000001, 36.200000000000003, 36.300000000000004, 36.399999999999999, 36.5, 36.600000000000001, 36.700000000000003, 36.800000000000004, 36.899999999999999, 37.0, 37.100000000000001, 37.200000000000003, 37.300000000000004, 37.399999999999999, 37.5, 37.600000000000001, 37.700000000000003, 37.800000000000004, 37.899999999999999, 38.0, 38.100000000000001, 38.200000000000003, 38.300000000000004, 38.400000000000006, 38.5, 38.600000000000001, 38.700000000000003, 38.800000000000004, 38.900000000000006, 39.0, 39.100000000000001, 39.200000000000003, 39.300000000000004, 39.400000000000006, 39.5, 39.600000000000001, 39.700000000000003, 39.800000000000004, 39.900000000000006]
        super(SampleObservedTrajectory, self).__init__(timepoints, values, description)

    def __str__(self):
        return 'sample-observed-trajectory'

class SampleInferenceFigure(FigureTask):



    def requires(self):


        trajectory = SampleObservedTrajectory()
        task = InferenceTask(max_order=3, model=P53Model(),starting_initial_conditions=[70.0, 30.0, 60.0],
                             starting_parameters=[90.0, 0.002, 1.7, 1.1, 0.93, 0.96, 0.01],
                             variable_parameters=[('c_2', None),('c_4', None)],observed_trajectories=[trajectory])
        return task

    def _return_object(self):
        from matplotlib import pyplot as plt
        fig = plt.figure()
        result = self.input().load()
        result.plot()
        return fig

if __name__ == '__main__':
    #run(main_task_cls=FigureHitAndMissTex)
    run()