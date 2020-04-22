/* 
* The following program will receive a string as an input and convert several typed EVN files into text files.
* The purpose of the program is to make it easy to convert several hundred EVA files into usable text files containing baseball stats.
* Assume that the EVA files are formatted as YYYYNNN.EVA  (Year_Three Letter Team Code.File Type)
* Author: Michael Krakovsky
* Version 1.0
* Date: February 22, 2018
*/

// Function Purpose: The function will find the year within the Event file name.
// The year of the file is needed to run the bevent file with the y tag. (See documentation)
// There will also be a check within the directory that the corresponding roster file exists.
// Parameters: Filename (String)
// Return: Year (String Format)
char *detectYear(char *fileName);

// Function Purpose: The function will throw an error if the directory does not exist and allow the user to recover.
// Parameters: Directory Name
// Return: An integer indicating a good or sour directory (0 for good, 1 for sour)
int isDirGood(char * directoryName);

// Function Purpose: The function will find the team name within the Event file name.
// The team name of the file is needed to create an appropriate text file name when the EVA is converted to a text file.
// There will also be a check within the directory that the corresponding roster file exists.
// Parameters: Filename (String)
// Return: Team Name (String Format)
char *detectTeamName(char *fileName);

// Function Purpose: The function will read the user input and indicate either yes or no
// The user should only be entering: (a) Y (b) y (c) n (d) N
// The program will exit when a N or n is indicated.
// Parameters: EVAfileName will print what file caused the error
// Return: N/A
void getResponse(char *EVAfileName);

// Function Purpose: The function will accept a string from the user and check if it is a working directory.
// The user should only be entering: (a) [A Directory Name] 
// The program will exit when a N or n is indicated.
// Parameters: N/A
// Return: Directory Name
char *getDirectoryName();

// Function Purpose: Check to see if the BEVENT file is present in the current working directory
// The function will exit and not allow a chance to recover. An error will be indicated.
// Parameters: directoryName (Directory Name)
// Return: N/A
void checkForBEVENT(char *directoryName);

// Function Purpose: Opens a directory and counts the number of files to process
// Parameters: directoryName (Directory Name) fileType (An example type could be .ROS)
// Return: fileCount (The number of files)
int countFileType(char *directoryName, char *fileType);

// Function Purpose: The function will check if the correct roster file is within the directory.
// The function will throw an error indicating if the absence of the roster file, and allow the user to recover.
// Parameters: fileName (Ex. Check if the corresponding .ROS file for the EVA file) directoryName (Location of these files)
// Return: void
void checkForRosterFile(char *fileName, char *directoryName);

// Function Purpose: The function will go to the indicated directory and find all of the specific files to process.
// The function will indicate the number of files to be processed.
// Parameters: currentDirectory (Directory to process files) fileType (An example type could be .ROS)
// Return: an array of file names to process
char **filesToHandle(char *directoryName, char *fileType); 

// Function Purpose: The function will finally execute the command and create a text file with the team stats
// Parameters: listOfFilesToProcess (List of files that will receive the command)
// Parameters: directoryName (The name of the directory) finalDestination (Where to put the text files) 
// Target String: "bevent -f 0-95 -y $YEAR ${YEAR}${NAME}.EVA>${NAME}inYear${YEAR}.txt"  
//Return: void
void runCommand(char *fileName, char *directoryName, char *finalDestination);

// Main function
int main();
