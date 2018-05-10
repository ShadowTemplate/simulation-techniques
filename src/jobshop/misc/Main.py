##
# Executes the input analysis, then runs the simulations of exercise 13 and 14 and finally executes the output analysis.
import numpy
from simpy import Environment
from jobshop.entity.JobsGenerator import JobsGenerator
from jobshop.entity.JobShop import JobShop
from jobshop.entity.JobComparator import ByTypeComparator, FIFOComparator
from jobshop.misc.Colors import c_print
from jobshop.misc.Constants import Constants
from jobshop.statistics import InputAnalysis
from jobshop.statistics import OutputAnalysis
##
# @mainpage
# These web pages provide the documentation of the simulator implemented to study the performance of a job shop.
# The case study is drawn from the book "Discrete-Event System Simulation"
# (Banks, Carson, Nelson, Nicol  Pearson Prentice-Hall - 4th edition).
#
# The simulator solves exercise 13 and exercise 14 from Chapter 11.
#
# For further reading please read this documentation (in italian): http://goo.gl/KspH3W
#
# Authors: Alessandro Suglia, Gianvito Taneburgo
#
# Università degli Studi di Bari Aldo Moro - 2014
#
#

if __name__ == '__main__':
    numpy.random.seed(seed=Constants.SEED)

    c_print("<-----INPUT ANALYSIS----->", 'YELLOW')
    InputAnalysis.run([26, 51, 101])

    Constants.JOB_COMPARATOR = FIFOComparator()

    numpy.random.seed(seed=Constants.SEED)
    c_print("<-----SIMULATION EXERCISE 13----->", 'YELLOW')
    stats_data = []
    for i in range(Constants.NUMBER_OF_RUNS):
        if i > 0:
            Constants.DEBUG_MODE = False
        env = Environment()
        shop = JobShop(env)
        generator = JobsGenerator(env, shop)
        env.process(generator.run())
        env.run(until=Constants.MAX_SIMULATION_TIME)
        stats_data.append((generator.served_job_list[:], shop.stations.copy()))

    c_print("\n<-----OUTPUT ANALYSIS EXERCISE 13----->", 'YELLOW')
    OutputAnalysis.run(stats_data, '13')

    Constants.DEBUG_MODE = True
    Constants.JOB_COMPARATOR = ByTypeComparator()

    numpy.random.seed(seed=Constants.SEED)
    c_print("\n<-----SIMULATION EXERCISE 14a----->", 'YELLOW')
    stats_data2 = []
    for i in range(Constants.NUMBER_OF_RUNS):
        if i > 0:
            Constants.DEBUG_MODE = False
        env = Environment()
        shop = JobShop(env)
        generator = JobsGenerator(env, shop)
        env.process(generator.run())
        env.run(until=Constants.MAX_SIMULATION_TIME)
        stats_data2.append((generator.served_job_list[:], shop.stations.copy()))

    c_print("\n<-----OUTPUT ANALYSIS EXERCISE 14a----->", 'YELLOW')
    OutputAnalysis.run(stats_data2, '14a')

    c_print("\n<-----OUTPUT ANALYSIS EXERCISE 14b----->", 'YELLOW')
    OutputAnalysis.run(stats_data, '14b')
