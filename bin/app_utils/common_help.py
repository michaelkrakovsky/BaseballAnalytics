# Script Discription: The script will contain helper functions used across stages.
# Script Version 1.0

from pathlib import Path
from datetime import datetime
from os import path, makedirs

class Log_Helper():

    def __init__(self):

        # Class Description: The class will contain functions related to printing messages to the console.

        self.log_folder = Path('BaseballAnalytics/logs/')                    # The path to the generic log folder.

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

    def create_log_file(self, name_of_log_folder, file_name):

        # Function Description: Create a file to store all kinds of error logs. The following can be used accross function type.
        # Function Parameters: path_to_log_folder (The location you wish the store the ), file_name (The name of the file.)
        # Function Throws: Nothing
        # Function Returns: The complete path to the log file.

        get_date = datetime.now().strftime('%b-%d-%I%M%p-%G')                           # Create the file name.
        complete_folder_name = self.log_folder / name_of_log_folder
        complete_folder_name = complete_folder_name.absolute()
        mod_name = file_name + get_date + '.txt'                                
        if not path.exists(complete_folder_name): makedirs(complete_folder_name)        # Ensure folder exists, then create the file.
        full_path = self.log_folder / name_of_log_folder / mod_name
        with open(full_path.absolute(), 'w+'): pass
        return full_path.absolute()

    def log_error_in_file(self, path_to_file, msg):

        # Function Description: Given the name of a path to a file, write errors into the logs.
        # Function Parameters: path_to_file (The full path to the folder in which to write logs.), 
        #    msg (The message to write into the logs.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        with open(path_to_file, 'a+') as f: f.write(msg)