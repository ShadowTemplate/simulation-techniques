from queue import PriorityQueue
from jobshop.entity.Worker import Worker
from jobshop.misc.Constants import Constants
from jobshop.statistics import Distributions


##
# Process that model the logic inside each station of the system.
class Station:
    ##
    # Initializes the current station with a specific distribution
    # that defines the processing time per job and an id.
    #
    # @param shop a reference to the job shop which the current station belongs
    # @param env a reference to the simulation environment
    # @param id the station's identifier
    # @param distrib the distribution used for service times
    def __init__(self, shop, env, id, distrib):
        self._shop = shop
        self._env = env
        self._id = id
        self._distributions = distrib
        self.job_arrived_event = self._env.event()
        self._job_queue = PriorityQueue(Constants.STATION_QUEUE_SIZE)
        self._busy_workers_list = []
        self._idle_workers_list = []
        # Initializes a dictionary which has as key the job type identifier and as a value
        # the specific distribution instance associated to it
        self._distr_per_type = {type: Distributions.GaussianDistribution(self._distributions[type][0],
                            self._distributions[type][1]) if not self._distributions[type] is None else None
                            for type in self._distributions.keys()}

        for i in range(1, Constants.STATIONS_CAPACITY[self._id] + 1):
            self._idle_workers_list.append(Worker(self._shop, self._env, self, i))
            env.process(self._idle_workers_list[-1].run())

    ##
    # Starts the cycle in which the station is able to manage
    # the job arrivals and each worker which is able to satisfy
    # the job's request.
    #
    def run(self):
        while True:
            yield self.job_arrived_event  # Waits until a new client arrives
            # Creates a new instance for the next arrive
            self.job_arrived_event = self._env.event()
            # Chooses the server that will do the work
            curr_worker = self._idle_workers_list[0]
            self._idle_workers_list.remove(curr_worker)
            self._busy_workers_list.append(curr_worker)
            # print('Handled by Server %s' % self._id)
            # Fires the event that will start the specific worker
            curr_worker.start_working_event.succeed(self._job_queue.get())

    ##
    # Returns the processing time for the type of
    # job specified as a parameter to the function.
    #
    # @param type the job's type
    # @return service time amount for the specific type of job
    def get_service_time(self, type):
        return abs(self._distr_per_type[type].next())

    ##
    # Adds the specified job to the jobs' queue of the current
    # station.
    #
    # @param job the job that will be added to the queue
    def add_job(self, job):
        self._job_queue.put(job)

    ##
    # Releases the specified worker putting it in the idle queue
    # and removing it from the busy workers' queue.
    #
    # @param server the server that will be added to the idle queue
    def add_idle_worker(self, server):
        self._busy_workers_list.remove(server)
        self._idle_workers_list.append(server)

    ##
    # States if the current station has other available workers.
    #
    # @return True if the idle workers' list is not empty, False otherwise
    def has_available_worker(self):
        return True if self._idle_workers_list else False

    ##
    # Returns all the workers that belong to the current station.
    #
    # @return list of the current station's workers
    def get_workers_list(self):
        return set(self._busy_workers_list).union(self._idle_workers_list)

    ##
    # Returns the current station's identifier.
    #
    # @return the station's identifier
    def get_id(self):
        return self._id

    def __str__(self):
        return str(self._id)
