#!/usr/bin/env python

import os
import sys
import uuid


''' ===========================================================================
    The purpose of this script is to poll some location and copy file(s) which 
    match a specified pattern, into some destination.
    ___________________________________________________________________________
'''

# GLOBALS
input_part_counter = 0                      

# CONSTANTS
WATCHED_FOLDER = "/cygdrive/c/Aso_experiment/Aso-44channelActive/Loreta/Loreta/bin/Debug/WatchFolderEEG/"
EXPECTED_FILENAME_REPLACEMENT_TOKEN = "[input_part_counter]"
EXPECTED_FILENAME = "eeg_" + EXPECTED_FILENAME_REPLACEMENT_TOKEN + ".txt"
DESTINATION_FOLDER = "/cygdrive/c/Users/1005120z/Desktop/"

POLL_INTERVAL = 1               # seconds
LOCK_REATTEMPT_DELAY = 0.1      # seconds 

def main(argv):
    global input_part_counter
    firstfilepath = first_file_path()
    print ("Starting with file: {:s}").format(firstfilepath)

''' ===========================================================================
    Checks if the files are ready.
    For a file to be ready it must exist and can be opened in append mode.
    ___________________________________________________________________________
'''
def poll(filepath):

    while not os.path.exists(filepath):
        print "%s hasn't arrived. Waiting %s seconds." % (filepath, wait_time) 
        time.sleep(POLL_INTERVAL)

        # If the file exists but locked, wait wait_time seconds and check 
        # again until it's no longer locked by another process.

        while is_locked(filepath):
            time.sleep(LOCK_REATTEMPT_DEPLAY)




''' ===========================================================================
    Atomic copy operation based on the 'whack-a-mole' algorithm as explaied here:
    http://stackoverflow.com/questions/11614815/a-safe-atomic-file-copy-operation
    ___________________________________________________________________________
'''
def atomic_copy():
    # Check whether the file already exists in the destination folder. Stop if it does.

    # Generate a unique ID
    
    uuid_str = uuid.uuid4()

    # Copy the source file to the target folder with a temporary name, say, <target>.<UUID>.tmp.

    

    # Rename the copy <target>-<UUID>.mole.tmp.

    # Look for any other files matching the pattern <target>-*.mole.tmp.

    # If their UUID compares greater than yours, attempt to delete it. (Don't worry if it's gone.)

    # If their UUID compares less than yours, attempt to delete your own. (Again, don't worry if it's gone.) From now on, treat their UUID as if it were your own.

    # Check again to see if the destination file already exists. If so, attempt to delete your temporary file. (Don't worry if it's gone. Remember your UUID may have changed in step 5.)

    # Attempt to rename your temporary file to its final name, <target>. (Don't worry if it's gone.)


def first_file_path():
    part_counter_str = str(input_part_counter)
    fileName = EXPECTED_FILENAME.replace(EXPECTED_FILENAME_REPLACEMENT_TOKEN, part_counter_str)
    filePath = (
        WATCHED_FOLDER
        + fileName
    )
    return filePath

''' ===========================================================================
    Checks if a file is locked by opening it in append mode.
    If no exception thrown, then the file is not locked.
    ___________________________________________________________________________
'''

def is_locked(filepath):
    locked = None
    file_object = None
    if os.path.exists(filepath):
        try:
            print "Trying to open %s." % filepath
            buffer_size = 8
            # Opening file in append mode and read the first 8 characters.
            file_object = open(filepath, 'a', buffer_size)
            if file_object:
                print "%s is available." % filepath
                locked = False
        except IOError, message:
            print "File is locked (unable to open in append mode). %s." % message
            locked = True
        finally:
            if file_object:
                file_object.close()
                print "%s closed." % filepath
    else:
         print "%s not found." % filepath
    return locked


'''
    This file is run as the main program

'''
if __name__ == "__main__":
    main(sys.argv[1:])

