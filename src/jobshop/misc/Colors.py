from jobshop.misc.Constants import Constants


##
# A util function introduced for the aesthetic sake.
# Prints the specified string using a specific color.
#
# @param text the string that will be printed
# @param color the color that will be used to print the string
def c_print(text, color):
    print(Constants.COLORS[color] + text + '\033[0m')