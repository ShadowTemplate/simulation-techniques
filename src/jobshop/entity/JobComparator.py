from jobshop.entity.Job import Job


##
# Abstract class that defines some methods necessary to sort
# jobs within the stations' waiting queue.
#
# Each time a new sorting criterion needs to be added
# it will be sufficient to extend this class and implement all the
# methods to model appropriately the logic behind the sorting criterion.
#
class JobComparator:
    ##
    # Says when a job instance is lower than another.
    #
    # @param this first job that will be compared
    # @param other second job that will be compared
    # @return True if 'this' is lower than 'other', False otherwise
    def lower_than(self, this, other):
        pass

    ##
    # Says when a job instance is greater than another.
    #
    # @param this first job that will be compared
    # @param other second job that will be compared
    # @return True if 'this' is greater than 'other', False otherwise
    def greater_then(self, this, other):
        pass

    ##
    # Says when a job instance is equal than another.
    #
    # @param this first job that will be compared
    # @param other second job that will be compared
    # @return True if 'this' is equal to 'other', False otherwise
    def equal(self, this, other):
        pass

    ##
    # Says when a job instance is lower or equal to another.
    #
    # @param this first job that will be compared
    # @param other second job that will be compared
    # @return True if 'this' is lower or equal to 'other', False otherwise
    def lower_equal_than(self, this, other):
        pass

    ##
    # Says when a job instance is greater or equal to another.
    #
    # @param this first job that will be compared
    # @param other second job that will be compared
    # @return True if 'this' is greater or equal to 'other', False otherwise
    def greater_equal_than(self, this, other):
        pass


##
# This class sorts jobs using their types.
# A job with a type lower than another has higher priority.
#
class ByTypeComparator(JobComparator):
    def lower_than(self, this, other):
        assert isinstance(this, Job) and isinstance(other, Job)

        return this.type < other.type

    def greater_then(self, this, other):
        assert isinstance(this, Job) and isinstance(other, Job)

        return this.type > other.type

    def equal(self, this, other):
        if not isinstance(this, Job) or not isinstance(other, Job):
            return False

        return this.type == other.type

    def lower_equal_than(self, this, other):
        assert isinstance(this, Job) and isinstance(other, Job)

        return this.type <= other.type

    def greater_equal_than(self, this, other):
        assert isinstance(this, Job) and isinstance(other, Job)

        return this.type >= other.type


##
# This class sorts jobs using a FIFO criterion.
#
class FIFOComparator(JobComparator):
    def lower_than(self, this, other):
        assert isinstance(this, Job) and isinstance(other, Job)

        return False

    def greater_then(self, this, other):
        assert isinstance(this, Job) and isinstance(other, Job)

        return False

    def equal(self, this, other):
        if not isinstance(this, Job) or not isinstance(other, Job):
            return False

        return False

    def lower_equal_than(self, this, other):
        assert isinstance(this, Job) and isinstance(other, Job)

        return False

    def greater_equal_than(self, this, other):
        assert isinstance(this, Job) and isinstance(other, Job)

        return False