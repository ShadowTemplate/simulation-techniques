from jobshop.entity.Job import Job
from jobshop.misc.Colors import c_print
from jobshop.misc.Constants import Constants
from jobshop.statistics.Distributions import UniformDistribution, ExponentialDistribution


##
# Process that creates new jobs and sends them to the
# proper first station.

# It is able to collect some kind of information about the clients that are
# correctly served by the system.
class JobsGenerator:
    counter = 1  # number of clients generated so far
    served_job_list = []  # list of jobs completed
    _job_type_distr = UniformDistribution(1, 100)  # distribution of the job types
    _interarrival_time_distr = ExponentialDistribution(Constants.ARRIVAL_RATE)  # distribution of the arrival_time

    ##
    # Initializes the current client generator
    # using the simulation environment and the shop.
    #
    # @param env the simulation environment
    # @param shop a reference to the specific shop
    def __init__(self, env, shop):
        self._env = env
        self._shop = shop
        JobsGenerator.counter = 1
        JobsGenerator.served_job_list = []

    ##
    # Starts to generate each client in a fashion defined
    # by the specific probability distribution associated
    # to the clients' arrival time.
    #
    def run(self):
        while True:
            new_type = JobsGenerator._get_job_type()
            new_job = Job(JobsGenerator.counter, new_type, self._env.now)
            if Constants.DEBUG_MODE:
                c_print('GEN: Job {0} (Type: {1}) at {2}'.format(new_job.id, new_job.type, new_job.start_t), 'BLUE')
            JobsGenerator.counter += 1
            first_station = self._shop.get_station(Constants.FIRST_STATIONS[new_type])
            first_station.add_job(new_job)
            if first_station.has_available_worker():  # Se c'è un server disponibile a servire il cliente
                first_station.job_arrived_event.succeed()  # Innesca l'evento per avviare il dispatcher
            yield self._env.timeout(JobsGenerator._inter_time())

    ##
    # Generates the type that will be associated to the job
    # according to an empirical distribution.
    #
    # The following proportion for the job types is defined:
    # type1 - 0.4
    # type2 - 0.3
    # type3 - 0.2
    # type4 - 0.1
    @staticmethod
    def _get_job_type():
        digit = JobsGenerator._job_type_distr.next()
        if digit <= 40:
            return 1
        if digit <= 70:
            return 2
        if digit <= 90:
            return 3
        return 4

    ##
    # Returns the next interarrival time.
    @staticmethod
    def _inter_time():
        return JobsGenerator._interarrival_time_distr.next()