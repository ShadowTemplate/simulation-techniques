from jobshop.entity.JobsGenerator import JobsGenerator
from jobshop.misc.Colors import c_print
from jobshop.misc.Constants import Constants


##
# Process that represents a worker that belong to a specific
# station and which is able to complete some jobs.
#
# The class presents some attributes to collect some statistics
# about the current worker.
#
class Worker:
    ##
    # Initializes the current worker with the specified
    # id and saves the reference to the simulation environment,
    # to a JobShop instance and to the specific station it belongs to.
    #
    def __init__(self, shop, env, station, id):
        self._shop = shop
        self._env = env
        self._station = station
        self._id = id
        self.start_working_event = self._env.event()
        self.total_work_time = 0

    ##
    # Starts the worker process. It will always be available
    # to receive requests from the station it belongs to.
    def run(self):
        while True:
            # waits until a new job is available
            yield self.start_working_event
            # gets the job that will be served
            job = self.start_working_event.value
            # generates a new event for future works
            self.start_working_event = self._env.event()
            if Constants.DEBUG_MODE:
                c_print('START: Job {0}({1}) (Stat {2}, Work {3}) at {4}'.format(job.id, job.type, self._station, self._id, self._env.now), 'GREEN')
            job.wait_t += self._env.now - job.start_t
            service_time = self._station.get_service_time(job.type)
            yield self._env.timeout(service_time)
            end_time = self._env.now
            if Constants.DEBUG_MODE:
                c_print('END: Job {0}({1}) (Stat {2}, Work {3}) at {4}'.format(job.id, job.type, self._station, self._id, end_time), 'RED')
            if self._env.now > Constants.STARTUP_TIME:
                self.total_work_time += service_time
            next_station = self._shop.get_next_station(self._station.get_id(), job.type)
            # checks if there is a next station to be visited or if the job is completed
            if next_station is None:
                job.end_t = end_time
                # saves the job that has been served
                if job.start_t > Constants.STARTUP_TIME:
                    JobsGenerator.served_job_list.append(job)
            else:
                # add the job to the next station
                next_station.add_job(job)
                # if there is an available worker in the next station
                if next_station.has_available_worker():
                    # fires the event in order to alert the station that a new job must be served
                    next_station.job_arrived_event.succeed()
            # the worker has finished its job: now it is free
            self._station.add_idle_worker(self)

    ##
    # Returns the current worker's identifier.
    #
    # @return current worker's identifier
    def get_id(self):
        return self._id

    def __eq__(self, other):
        if not isinstance(other, Worker):
            return False
        return self._id == other.get_id()

    def __hash__(self):
        return self._id