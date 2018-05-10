from jobshop.misc.Constants import Constants


##
# Defines the logical structure of a job that will be
# completed by a specific worker in the system.
#
class Job:
    ##
    # Initializes the current job using the parameters
    # specified in input.
    #
    # @param id the job's identifier
    # @param type type of the job
    # @param start_time simulation time at which the job arrived to the system
    def __init__(self, id, type, start_time):
        self.id = id
        self.type = type
        self.start_t = start_time
        self.wait_t = 0
        self.end_t = 0

    def __str__(self):
        return 'ID:{0} TY:{1} A:{2} W:{3} E:{4}'.format(self.id, self.type, self.start_t, self.wait_t, self.end_t)

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        assert not Constants.JOB_COMPARATOR is None

        return Constants.JOB_COMPARATOR.lower_than(self, other)

    def __gt__(self, other):
        assert not Constants.JOB_COMPARATOR is None

        return Constants.JOB_COMPARATOR.greater_than(self, other)

    def __eq__(self, other):
        assert not Constants.JOB_COMPARATOR is None

        return Constants.JOB_COMPARATOR.equal(self, other)

    def __le__(self, other):
        assert not Constants.JOB_COMPARATOR is None

        return Constants.JOB_COMPARATOR.lower_equal_than(self, other)

    def __ge__(self, other):
        assert not Constants.JOB_COMPARATOR is None

        return Constants.JOB_COMPARATOR.greater_equal_than(self, other)

    def __ne__(self, other):
        assert not Constants.JOB_COMPARATOR is None

        return not Constants.JOB_COMPARATOR.equal(self, other)
