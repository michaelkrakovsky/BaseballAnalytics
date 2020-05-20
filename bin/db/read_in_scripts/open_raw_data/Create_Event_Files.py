# Script Description: The script transforms raw data into Event Files (or other functions) for the Data Driver to consume.
# Author: Michael Krakovsky
# Version: 1.0

from pathlib import Path
from zipfile import ZipFile
from os import makedirs
from os.path import exists, join, isfile
from os import listdir, system
from re import sub
from time import gmtime, strftime

class Create_Event_Files():

    def __init__(self):

        # Class Description: The main driver in creating event files. The script will unzip the files and process the files into the database.

        self.path_to_data = Path("BaseballAnalytics/bin/db/raw_data/")                                                 # The path to the raw data files.
        self.path_to_data_creators = Path("BaseballAnalytics/bin/db/db_read_in_scripts/open_raw_data/data_creators")   # The path to the .exe files that create the data.
        self.path_to_logs = Path("BaseballAnalytics/logs/create_files_logs/")                                      # The path to the logs specific to creating event files.

    def __extract_files(self, source, dest):

        # Function Description: Given the source of files and the destination in which they are heading, unpack all the files.
        # Function Parameters: source (Path: The source of the files), dest (Path: The destination of the files)
        # Function Throws: Nothing
        # Function Returns: Nothing

        if not exists(dest): makedirs(dest)                                          # Ensure the proper directories are in place and created.
        if not exists(source.absolute()): raise SystemError("The {} source data cannot be found.".format(source.absolute()))
        with ZipFile(source.absolute(), 'r') as zip_ref:                                                                      # Extract the source data into a new folder.
            zip_ref.extractall(dest.absolute())

    def __create_cmd_command(self, files_loc, file_name, bevent_file, files_dest_loc, log_file):

        # Function Description: The function will build the string to be executed as a cmd line.
        # Function Paramters: files_loc (The path to the location of all the raw data), file_name (The name of the file to be processed), 
        #    bevent_file (The full path to the event file), files_dest_loc (Path: The path to the files location), 
        #    log_file (The log files to store the output from the data conversions)
        # Function Throws: Nothing
        # Function Returns: command (The command to be executed within cmd. The command will be as follows:)
        #      cd (Directory) && (Path_To_Bevent) -f 0-95 -y (year) (File Name) > (New File Name (.txt))
        
        if not exists(files_dest_loc): makedirs(files_dest_loc)
        full_file_name = files_loc / file_name
        year_num = file_name[0:4]                                        # Get the year and team from the file name Assume file name is formatted like such YYYYRRR.(EVN | EVA) (Y = Year, R = Roster)
        team_name = file_name[4:7]
        roster_file_name = team_name + year_num + '.ROS'                 # Ensure the Roster File is found in the directory.
        if not isfile(join(files_loc.absolute(), roster_file_name)):
            raise ValueError("The Roster '{}' file does not exist with the associated EVN or EVA file '{}'.".format(roster_file_name, file_name))
        file_dest = files_dest_loc / (year_num + team_name + '.txt')
        command = 'cd ' + str(files_loc.absolute()) + ' && (' + str(bevent_file.absolute()) + ' -f 0-95 -y ' + year_num + ' ' + str(full_file_name.absolute()) + ' > ' + str(file_dest.absolute()) + ')'
        command += ' 1>> ' + str(log_file.absolute()) + ' 2>>&1'
        return command

    def __create_log_file_name(self):

        # Function Description: Create the name of the log file to store all the logs output.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: log_file_name (String: The name of the log file. The file is formatted as Day_Time.)

        log_file_name = strftime("%Y-%m-%d_%H_%M_%S", gmtime()) + '.txt'
        log_file_name = self.path_to_logs / log_file_name
        with open(log_file_name.absolute(), 'w'): pass
        return log_file_name
    
    def create_event_files(self):

        # Function Description: Create the Event Files straight from the zipped source data.
        # Function Parameters: Nothing
        # Function Throws: ValueError (When the Roster file is not found.)
        # Function Returns: Nothing

        source_data = self.path_to_data / '1990_2019.zip'                     # The path to the source data.
        data_dest = self.path_to_data / '1990_2019'                           # The path to the destination file.
        dest_event_files = self.path_to_data / '1990_2019_Event_Files' 
        self.__extract_files(source_data, data_dest)
        log_file_name = self.__create_log_file_name()                         # We only want to create one file.
        for file_name in listdir(data_dest.absolute()):
            if file_name.endswith(".EVN") or file_name.endswith(".EVA"):
                cmd_string = self.__create_cmd_command(data_dest, file_name, self.path_to_data_creators / 'BEVENT.EXE', 
                                                        dest_event_files, log_file_name)
                system(cmd_string)                                                                                      # Execute the command.

