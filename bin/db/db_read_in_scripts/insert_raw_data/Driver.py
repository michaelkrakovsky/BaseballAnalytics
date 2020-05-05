# Module Description: The module will be the parent for all the child drivers. The main commonality
#    is that each module will require a query insertion. Each table will require specific insertion functions
#    that are delegated to the specific module. 
# Module Version: 1.0
# Module Author: Michael Krakovsky

from warnings import filterwarnings                         # Handle warnings from mysql.
from Driver_Exceptions import UnrecognisableMySQLBehaviour
from pathlib import Path
from os import path, listdir

class Driver():

    def __init__(self, db_connection):

        # Function Description: Intialise the Parent Driver. The Parent Driver will provide general functionality accross all Drivers.
        #       Most noteably, it will provide a general query executor.
        # Function Parameters: db_connection (pymysql.connections.Connection: The connection to the database.) 
        # Function Throws: ValueError (The error is thrown when the connection type is incorrect.)
        # Function Returns: Nothing

        if (str(type(db_connection)) == '<class \'pymysql.connections.Connection\'>'):
            self.__db_connection__ = db_connection
        else:
            raise ValueError("The user did not provide the correct pymysql connector.")
        self.log_folder = Path('BaseballAnalytics/logs/insert_file_logs') 

    def __get_latest_log_file(self):

        # Function Description: Get the latest file from the log directory.
        # Function Parameters: Nothing
        # Function Throws: Nothing
        # Function Returns: The path to the file.

        files = listdir(self.log_folder)
        files = sorted(files)
        return self.log_folder / files[-1]

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

    def write_into_log_file(self, path_to_log_file, msg):

        # Function Description: Write contents into the log file.
        # Function Parameters: path_to_log_file (The path to the log file.)
        #     msg (The message to write into the file.)
        # Function Throws: Nothing
        # Function Returns: Nothing

        if not path.isfile(path_to_log_file): raise ValueError("The path does not lead to a file: {}".format(path_to_log_file))
        with open(path_to_log_file, 'a') as f: 
            for m in msg:
                f.write(m)

    def create_query_string(self, column_names, event_query_dict, table_name):

        # Function Description: Build Insert statements based on the names and values given.
        # Function Parameters: column_names (The names of the columns to insert into the database.), 
        #     event_query_dict (The dictionary that contains all the values that will be inserted into the database.), 
        #     table_name (The name of the table that will recieve the new content.) 
        # Function Throws: Nothing
        # Function Returns: query (The query that can readily be executed.)

        query = "INSERT IGNORE INTO " + table_name + " ("
        second_query_half = ") Values ("
        for i in column_names:
            query += i + ", "                                 # Add the column names.  
            try:
                val = int(event_query_dict[i])
                second_query_half += str(val) + " , "
            except ValueError:                                # Must be a string, insert as a string.
                second_query_half += "\'" + event_query_dict[i] + "\' , "
        query = query[:-2]                                    # Remove the ending of the string (The comma and space)
        second_query_half = second_query_half[:-3]
        query += second_query_half + ");"
        return query  

    def execute_queries(self, queries):

        # Function Description: The generic query executor that utilises the current connection to the database and executes a query.
        # Function Parameters: queries (The queries that will be executed.)
        # Function Throws: Nothing
        # Function Returns: True or False (True will be turned if there are no warnings or errors. False will be returned otherwise.)

        cursor = self.__db_connection__.cursor() 
        filterwarnings('error')                                     # Convert warnings into exceptions to be caught.                   
        status = 1
        for query in queries:    
            try:
                temp_status = cursor.execute(query)                 # Execute Query: And close the cursor.
                if status != 0: status = temp_status                # Do not change the status if the query status is incorrect. 
            except Exception as ex:
                log_file = self.__get_latest_log_file()
                self.write_into_log_file(log_file, ["\n The Caught Warning: {}".format(ex), "\n The Query: {}".format(query)])
                status = 0
        self.__db_connection__.commit()                             # This saves the query execution to the database.
        filterwarnings('always')                                    # Turn the filter for warnings back on.
        cursor.close()
        return bool(status)

    def execute_query(self, query):

        # Function Description: The generic query executor that utilises the current connection to the database and executes a query.
        # Function Parameters: query (The query that will be executed.)
        # Function Throws: Nothing
        # Function Returns: True or False (True will be returned if there are no warnings or errors. False will be returned otherwise.)

        cursor = self.__db_connection__.cursor() 
        filterwarnings('error')                                     # Convert warnings into exceptions to be caught.                   
        try:
            status = cursor.execute(query)                          # Execute Query: And close the cursor.
            self.__db_connection__.commit()                         # This essentially saves the query execution to the database.
        except Exception as ex:
            log_file = self.__get_latest_log_file()
            self.write_into_log_file(log_file, ["\n The Caught Warning: {}".format(ex), "\n The Query: {}".format(query)])
            status = 0
        filterwarnings('always')                                    # Turn the filter for warnings back on.
        cursor.close()
        return bool(status)

    def execute_many(self, query, data):

        # Function Description: The query will enter multiple queries at once, specifically insert data.
        # Function Parameters: query (The beginning part of the query.) data (The data to insert into the table.)
        # Function Throws: Nothing
        # Function Returns: True or False (True will be returned if there are no warnings or errors. False will be returned otherwise.)

        cursor = self.__db_connection__.cursor()
        filterwarnings('error')                                     # Convert warnings into exceptions to be caught.                   
        try:
            status = cursor.executemany(query, data)                # Execute Query: And close the cursor.
            self.__db_connection__.commit()                         # This essentially saves the query execution to the database.
        except Exception as ex:
            log_file = self.__get_latest_log_file()
            self.write_into_log_file(log_file, ["\n The Caught Warning: {}".format(ex), 
                                                "\n The Query: {}".format(query), 
                                                "\n The Data: {}".format(str(data))])
            status = 0
        filterwarnings('always')                                    # Turn the filter for warnings back on.
        cursor.close()
        return bool(status)