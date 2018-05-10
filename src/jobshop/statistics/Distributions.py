import scipy.stats


##
# Abstract class that defines the methods that a new
# probability distribution should have.
#
class Distribution:
    ##
    # Initializes the current distribution instance
    # using the specified parameters.
    #
    # @param params distribution's specific parameters
    def __init__(self, *params):
        pass

    ##
    # Returns a new value according the probability distribution.
    def next(self):
        pass

    ##
    # Computes the inverse function of the current
    # probability distribution using the specified parameter.
    #
    # @param q the inverse function's argument
    def get_inverse(self, q):
        pass

    ##
    # Returns an array that contains values belonging
    # to the current distribution.
    #
    # @param n total number of values that will be generated
    def get_sample_data(self, n):
        pass

    def __str__(self):
        pass


##
# Class that represents the Gaussian (normal)
# probability distribution.
#
class GaussianDistribution(Distribution):
    ##
    # Initializes the current Gaussian probability
    # distribution using the specified mean and
    # standard deviation.
    #
    # @param params params[0] = mean, params[1] = std
    def __init__(self, *params):
        Distribution.__init__(self, params)
        self._mean = params[0]
        self._std = params[1]
        self._distr = scipy.stats.norm(loc=self._mean, scale=self._std)

    def next(self):
        return self._distr.rvs(size=1)[0]

    def get_sample_data(self, n):
        return self._distr.rvs(size=n)

    def get_inverse(self, q):
        return self._distr.ppf(q)

    def __str__(self):
        return 'Normal (mean: {0}, std: {1})'.format(self._mean, self._std)


##
# Class that represents the uniform probability distribution.
#
class UniformDistribution(Distribution):
    ##
    # Initializes the current uniform probability
    # distribution instance using the specified parameters
    # which represent the probability definition co-domain.
    def __init__(self, *params):
        Distribution.__init__(self, params)
        self._lower = params[0]
        self._upper = params[1]
        self._distr = scipy.stats.uniform(loc=self._lower, scale=self._upper)

    def next(self):
        return self._distr.rvs(size=1)[0]

    def get_inverse(self, q):
        return q

    def get_sample_data(self, n):
        return self._distr.rvs(size=n)

    def __str__(self):
        return 'Uniform (min: {0}, max: {1})'.format(self._lower, self._upper)


##
# Class that represents an exponential probability distribution.
class ExponentialDistribution(Distribution):
    ##
    # Initializes the current exponential distribution
    # using the specified parameter, which represents the
    # mean.
    #
    # @param params the mean (params[0])
    def __init__(self, *params):
        Distribution.__init__(self, params)
        self._mean = params[0]
        self._distr = scipy.stats.expon(loc=1 / self._mean)

    def next(self):
        return self._distr.rvs(size=1)[0]

    def get_inverse(self, q):
        return self._distr.ppf(q)

    def get_sample_data(self, n):
        return self._distr.rvs(size=n)

    def __str__(self):
        return 'Exponential (mean: {0})'.format(self._mean)
