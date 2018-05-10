from jobshop.misc.Constants import Constants
import scipy
from scipy.stats import t


##
# Generates statistics about a specific exercise using
# the data collected during the simulation
#
# @param stats simulation data collected
# @param exercise_num a string representation of the exercise that will be analyzed
def run(stats, exercise_num):
    jobs_list_runs = [x[0] for x in stats]
    stations_list_runs = [x[1] for x in stats]
    print('Number of run(s): %s\n' % Constants.NUMBER_OF_RUNS)

    if Constants.NUMBER_OF_RUNS > 1:
        if exercise_num == '13':
            for i in range(1, Constants.STATIONS_NUM+1):
                print('Station {0} - Average worker utilization: {1}'.format(i, avg_worker_utilization(stations_list_runs, i)))

        acc = Constants.JOB_RESPONSE_TIME_INTERVAL_ACCURACY_EX13 if exercise_num == '13' else Constants.JOB_RESPONSE_TIME_INTERVAL_ACCURACY_EX14

        for i in range(1, Constants.JOB_TYPES_NUM + 1):
            print('Job type {0} - Mean total response time: {1}'.format(i, mean_total_response_time(jobs_list_runs, i, acc)))
    else:
        print('No stats available: an insufficient number of run has been executed.')


##
# Computes the average worker utilization for a specific station
# distributed among the different executions of the simulation.
# A confidence interval is generated at the end of the function using a specific
# significance value which is defined by the exercise.
#
# @param stations_list_runs a list of Station objects for each run
# @param curr_station_index the station for which will be computed the metric
#
# @return a string representation of the confidence interval for this metric
def avg_worker_utilization(stations_list_runs, curr_station_index):
    workers_utilizations = []

    for i in range(Constants.NUMBER_OF_RUNS):
        curr_station = stations_list_runs[i][curr_station_index]
        workers = curr_station.get_workers_list()
        workers_utilizations.append(0 if not workers else scipy.average([w.total_work_time / Constants.MAX_SIMULATION_TIME for w in workers]))

    return confidence_interval(workers_utilizations, Constants.AVG_WORKER_UTIL_INTERVAL_ACCURACY)


##
# Computes the mean total response time for a specific type of job that is
# satisfied by the jobshop's workers.
# A confidence interval is generated at the end of the function using a specific
# significance value which is defined by the exercise.
#
# @param jobs_list_runs list of jobs executed for each run
# @param job_type_index job type's index for which we want to compute the metric
# @param accuracy the significance level at which we want to compute the confidence interval
#
# @return a string representation of the confidence interval computed
def mean_total_response_time(jobs_list_runs, job_type_index, accuracy):
    response_times = []

    for i in range(Constants.NUMBER_OF_RUNS):
        jobs = [job for job in jobs_list_runs[i] if job.type == job_type_index]
        response_times.append(0 if not jobs else scipy.average([job.end_t - job.start_t for job in jobs]))

    return confidence_interval(response_times, accuracy)


##
# Generates the confidence interval starting from the data in input
# and using a specific degree of accuracy specified by the user.
# This kind of statistical test is used in order to compute output analysis
# on the results obtained from the simulation.
#
# @param values reference values for the test
# @param accuracy significance value for the current test
# @return a string representation of the confidence interval computed
def confidence_interval(values, accuracy):
    mean_average = scipy.average(values)
    size = len(values)
    standard_deviation = (1 / ((size - 1) * size) * sum([pow((x - mean_average), 2) for x in values]))

    error = abs(t.ppf((1 - accuracy) / 2, size - 1)) * scipy.sqrt(standard_deviation)
    return '{0} <= p <= {1}'.format(max(mean_average-error, 0), mean_average+error)