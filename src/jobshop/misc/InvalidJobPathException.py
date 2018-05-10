

##
# Class which defines an exceptional event that happens
# when there is no station to assign to a specific job.
#
class InvalidJobPathException(Exception):
    def __init__(self, string):
        Exception.__init__(self, string)