from jobshop.entity.Station import Station
from jobshop.misc.Constants import Constants
from jobshop.misc.InvalidJobPathException import InvalidJobPathException


##
# Class which represents the main structure of the system.
# It initializes all the stations that will be used by the system
# to satisfy all the jobs.
class JobShop:
    ##
    # Initializes the whole system using the specified
    # simulation environment.
    #
    # @param env the simulation environment in which the system works
    def __init__(self, env):
        self.stations = {i: Station(self, env, i, Constants.STATIONS_DISTRIBUTIONS[i])
                         for i in range(1, Constants.STATIONS_NUM + 1)}
        for i in range(1, Constants.STATIONS_NUM + 1):
            env.process(self.stations[i].run())

    ##
    # Returns the station with the specified identifier.
    #
    # @param id station identifier
    # @return the station that has the specified identifier or KeyError if the id is incorrect
    def get_station(self, id):
        return self.stations[id]

    ##
    # Returns the next that should be visited by a specific job
    # with the specified job type.
    #
    # @param curr_station the station in which the job is
    # @param job_type job's type
    # @return a Station instance if the next station is available, None if the job has finished its path
    # @throw InvalidPathException if invalid parameters were specified to the method
    def get_next_station(self, curr_station, job_type):
        if job_type == 1:
            if curr_station == 1:
                return self.stations[2]
            if curr_station == 2:
                return self.stations[3]
            if curr_station == 3:
                return self.stations[4]
            if curr_station == 4:
                return None
        if job_type == 2:
            if curr_station == 1:
                return self.stations[3]
            if curr_station == 3:
                return self.stations[4]
            if curr_station == 4:
                return None
        if job_type == 3:
            if curr_station == 2:
                return self.stations[4]
            if curr_station == 4:
                return self.stations[3]
            if curr_station == 3:
                return None
        if job_type == 4:
            if curr_station == 1:
                return self.stations[4]
            if curr_station == 4:
                return None

        raise InvalidJobPathException('Unable to find the next station: invalid path followed')