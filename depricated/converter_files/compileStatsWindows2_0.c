// Import proper libraries and header files
#include <stdlib.h>
#include <stdio.h>
#include "compileStatsWindows2_0.h"
#include <malloc.h>
#include <dirent.h>
#include <ctype.h>

int isDirGood(char *directoryName) {
	
	DIR *dir = opendir(directoryName);
	if (dir) {
		closedir(dir);
		return 0;    //indicate that the directory is fine
	} else {
		printf("The directory you have entered does not exist. Please try again {(n) to exit)}\n");
        return 1;   //indicate that it did not work
    }	
	closedir(dir);
}

void getResponse(char *EVAfileName) {
	
	char response = 'n';   //default will be no
	
	printf("The roster file %s cannot be matched with the EVA file, do you wish to continue? \n", EVAfileName);
	if (scanf(" %c", &response) == 1) {
		if ((response == 'Y') || (response == 'y')) {
		    printf("Okay, we shall continue.\n");	
		} else if ((response == 'n') || (response == 'N')) {
		    printf("Okay, the processing as stopped at %s.\n", EVAfileName);	
			    exit(2);
		} else {
		    printf("Invalid Response. The processing as stopped at %s.\n", EVAfileName);
			exit(2);
	    }
	}
}

char *detectTeamName(char *fileName) {
	
    char *fileTeamName = malloc(4 * sizeof(char));
	int counter = 0;
	
	if (!fileTeamName) {                // Check if pointer is null
	    printf("An error occurred in detecting the Team name.\n");
	    exit(5);
	}
	for (int i = 0; i < 3; i++) {  // Skip the file type at the end  
		if (!isdigit(fileName[i])) {
			counter++;
			if (counter > 3) {
			    printf("The team name in the file cannot be detected.\n");
				printf("Make sure the file is formatted as a proper EVA or ROS file.\n");
			    exit(100);
			}
			fileTeamName[counter - 1] = fileName[i];
		}
	}
	if(counter != 3) {
		printf("The team name in the file cannot be detected.\n");
		printf("Make sure the file is formatted as a proper EVA or ROS file.\n");
		exit(101);
	}
	fileTeamName[3] = '\0';     // add a null character
	return fileTeamName;	
}

char *detectYear(char *fileName) {
    
    char *fileYear = malloc(5 * sizeof(char));
	printf("%d\n", fileName);
	int counter = 0;
	
	if (!fileYear) {                // Check if pointer is null
		printf("An error occurred in detecting the year.\n");
		exit(5);
	}
	for (int i = 0; i < 4; i++) {     
		if (isdigit(fileName[i])) {
			printf("%c", fileName[i]);
			counter++;
			if (counter > 4) {
				printf("\n");
				printf("%c", fileName[i]);
			    printf("The year in the file cannot be detected.\n");
				printf("Make sure the file is formatted as a proper EVA or ROS file.\n");
			    exit(102);
			}
			fileYear[counter - 1] = fileName[i];
		}
	} 
	if(counter != 4) {
		printf("The year in the file cannot be detected.\n");
		printf("Make sure the file is formatted as a proper EVA or ROS file.\n");
		exit(103);
	}
	fileYear[4] = '\0';     // add a null character
	return fileYear;
}

void checkForRosterFile(char *fileName, char *directoryName) {
	
	char rosterFileName[strlen(directoryName) + 14];     // Add additional room for the roster file to be added
	char *teamName = detectTeamName(fileName);    // Roster files are laid out as such (TeamCode_Year.ROS  Ex: WAS2017.ROS)
	char *seasonYear = detectYear(fileName);

	strcpy(rosterFileName, directoryName);    // Reconstruct the file name with strcat and strcpy
    strcat(rosterFileName, "\\");	
	strcat(rosterFileName, teamName);
	strcat(rosterFileName, seasonYear);
    strcat(rosterFileName, ".ROS");
    if (access(rosterFileName, F_OK) != 0) {
		getResponse(rosterFileName);
	} 
	printf("The file is in here!!\n");
}

char *getDirectoryName() {
	
	char *directory = malloc(300 * sizeof(char));   // store directory name on heap 
	int checkDir = 1;    //check if the directory is readable
	
	while(checkDir == 1) {
		printf("Please enter a directory name. {(n) to exit} \n");
		scanf("%300s", directory);     // limit the size to 75 to prevent a crash
		if((*directory == 'n') || (*directory == 'N')) {
			printf("Goodbye!\n");
			exit(0);   // exit if response is n
		} else {
			checkDir = isDirGood(directory);
		}
	}
	return directory;
}

void checkForBEVENT(char *directoryName) {
	
	
    char stringCopy[strlen(directoryName) + 12]; // Add room to include the BEVENT name and null character

	strcpy(stringCopy, directoryName);    
    strcat(stringCopy, "\\BEVENT.EXE\0");   // Append null character
	if (access(stringCopy, F_OK) != 0) {
		printf("Sorry you must have the BEVENT file in the working directory.\n");
		printf("%s does not exist in your directory.\n", stringCopy);
		exit(6);
	} 
}

int countFileType(char *directoryName, char *fileType) {
	
	DIR *dir;
	struct dirent *ent;
	int fileCount = 0;
	
	dir = opendir(directoryName);
	if (dir == NULL) {
		printf("Directory cannot be opened in countFileType.\n");
		exit(20);
	}
	ent = readdir(dir);
	while (ent != NULL) {
		if (strstr(ent->d_name, fileType) != NULL) {       // If the type is a file
		    fileCount++;
		}
	    ent = readdir(dir);   // Move onto the next file
	}
	closedir(dir);
	return fileCount;
}

char **filesToHandle(char *directoryName, char *fileType) {

	
	DIR *dir;         
	struct dirent *ent;
	char **filesToHandle;
	char *fileName;
	int numberOfFiles = countFileType(directoryName, fileType);
	int counter = 0;
	
	filesToHandle = malloc(numberOfFiles * sizeof(char*) + 1); //add null char to end array of strings  
    dir = opendir(directoryName);
	if (dir == NULL) {       // Create a stream to a directory
		printf("Directory cannot be opened in rosterFilesToProcess.\n");
		exit(20);
	}
	ent = readdir(dir);
	while (ent != NULL) {
		if (strstr(ent->d_name, fileType) != NULL) {       // If the type is a file
		    fileName = malloc(strlen(ent->d_name) * sizeof(char));
			strcpy(fileName, ent->d_name);
			filesToHandle[counter] = fileName;
			counter++;
		}
		if (counter > numberOfFiles) {      // Exit if counter reaches a certain length
			printf("Error: Number of files to process exceeds array size.\n");
			exit(8);
		}
	    ent = readdir(dir);   // Move onto the next file
	}
	filesToHandle[numberOfFiles] = NULL;    // Add a null to terminate the array
	closedir(dir);
	return filesToHandle;
}

void runCommand(char *fileName, char *directoryName, char *finalDestination) {
	
	char fullFileName[340];					// Ensure the length of the string is long enough to hold its contents
	char commandString[600];
    char fullCommand[700];	
	char *year;
	char *team;
	
	year = detectYear(fileName);			// Begin to build the command
	team = detectTeamName(fileName);
	strcpy(fullCommand, "cd ");
	strcat(fullCommand, directoryName); 
	strcat(fullCommand, " && ");
	strcpy(fullFileName, directoryName);
	strcat(fullFileName, "\\");
	strcat(fullFileName, fileName);      // Create the final name
    strcpy(commandString, directoryName);
	strcat(commandString, "\\BEVENT -f 0-95 -y ");     // This will always remain the same 
	strcat(commandString, year);	
	strcat(commandString, " ");
	strcat(commandString, fullFileName);
	strcat(commandString, ">");
	strcat(commandString, finalDestination);
	strcat(commandString, "\\");
	strcat(commandString, team);
	strcat(commandString, "inYear");
	strcat(commandString, year);
	strcat(commandString, ".txt");
	strcat(fullCommand, commandString);
	printf("%s", commandString);
	system(fullCommand);     // Execute command
}

int main () {
	
	char *directoryName;
	char *targetDirectoryName;
	char **files;
	int counter = 0;
	
	printf("Inputs Required:\n 1. Folder with all the necessary files INCLUDING the BEVENT.EXE file. \n 2. The destination folder. \n");
	directoryName = getDirectoryName();    // Retrieve the name of the directory
	checkForBEVENT(directoryName);      // Ensure directory contains BEVENT
	files = filesToHandle(directoryName, ".EVA");
	printf("Now please enter the location of where to place the text files.\n");
	targetDirectoryName = getDirectoryName();
	while (files[counter] != NULL) {
		runCommand(files[counter], directoryName, targetDirectoryName);	
		counter++;
		printf("On FILE ---------%d----- \n", counter);
	}
	return 0;
}