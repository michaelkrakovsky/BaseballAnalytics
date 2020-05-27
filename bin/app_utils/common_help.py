# Script Discription: The script will contain helper functions used across stages.
# Script Version 1.0

class Log_Helper():

    def __init__(self):

        # Class Description: The class will contain functions related to printing messages to the console.

        pass

    def print_progress_bar(self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '|', printEnd = "\r"):
        
        # Function Description: Call in a loop to create terminal progress bar.
        # Function Parameters: iteration - Required : current iteration (Int), total - Required : total iterations (Int)
        #    prefix - Optional : prefix string (Str), suffix - Optional : suffix string (Str), 
        #    decimals - Optional : positive number of decimals in percent complete (Int), 
        #    length - Optional : character length of bar (Int), fill - Optional  : bar fill character (Str), 
        #    printEnd - Optional : end character (e.g. "\r", "\r\n") (Str)

        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
        if iteration == total: print()                                              # Print New Line on Complete