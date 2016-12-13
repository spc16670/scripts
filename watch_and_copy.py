#!/usr/bin/env python

import os
import sys
import uuid
import time
from shutil import copyfile

''' ===========================================================================
    The purpose of this script is to poll some location and copy file(s) which 
    match a specified pattern, into some destination.
    ___________________________________________________________________________
'''

# GLOBALS
input_part_counter = 0                      
keep_polling = True
dotter = 0

# CONSTANTS

''' If set to True the files are copied, otherwise files are moved '''
JUST_COPY = True

SOURCE_FOLDER = "/cygdrive/c/Users/szymon.czaja/Desktop/in/"

DESTINATION_FOLDER = "/cygdrive/c/Users/szymon.czaja/Desktop/out"

EXPECTED_FILENAME_REPLACEMENT_TOKEN = "[input_part_counter]"
EXPECTED_FILENAME = "eeg_" + EXPECTED_FILENAME_REPLACEMENT_TOKEN + ".txt"


''' file name patterns for intermittent files '''
MOLE_FILENAME_REPLACEMENT_TOKEN = "[uuid]"
MOLE_FILENAME_EXTENSION = ".mole"
MOLE_FILENAME = MOLE_FILENAME_REPLACEMENT_TOKEN + MOLE_FILENAME_EXTENSION

POLL_INTERVAL = 1               # seconds
LOCK_REATTEMPT_DELAY = 0.1      # seconds 


def main(argv):
    firstfilepath = get_expected_file()
    print ("Expecting file: {:s}").format(firstfilepath)
    
    source_dir_exists = os.path.isdir(SOURCE_FOLDER)
    if not source_dir_exists:
        print ("Does source folder exist? {:s}").format(SOURCE_FOLDER)
        return

    dest_dir_exists = os.path.isdir(DESTINATION_FOLDER)
    if not dest_dir_exists:
        print ("Does destination folder exist? {:s}").format(DESTINATION_FOLDER)
        return 

    poll(firstfilepath)


''' ===========================================================================
    Checks if the files are ready.
    For a file to be ready it must exist and can be opened in append mode.
    ___________________________________________________________________________
'''

def poll(filepath):
    global keep_polling
    try: 
        while keep_polling:
            sys.stdout.flush()
            check_candidates()
            time.sleep(POLL_INTERVAL)
    except KeyboardInterrupt:
        keep_polling = False
        


''' ===========================================================================
    List files in the watched folder and start copy operation if the expected 
    file has appeared.
    ___________________________________________________________________________
'''

def check_candidates():
    global keep_polling
    expected = get_expected_file()
    global dotter
    if (dotter % 20 == 0):
        print "awaiting {:s} ".format(expected)
    else:
        print ".",
    dotter = dotter + 1
    files = os.listdir(SOURCE_FOLDER)
    for f in files:    
        if expected == f:
            advance_count()
            atomic_copy(expected)
        

''' ===========================================================================
    Atomic copy operation based on the 'whack-a-mole' algorithm as explaied here:
    http://stackoverflow.com/questions/11614815/a-safe-atomic-file-copy-operation
    ___________________________________________________________________________
'''
def atomic_copy(expected):
    print "*"
    in_file_path = os.path.join(SOURCE_FOLDER, expected)
    while is_locked(in_file_path):
        time.sleep(LOCK_REATTEMPT_DELAY)
        
    print "\nAttempting to move: {:s}".format(expected)

    out_file_path = os.path.join(DESTINATION_FOLDER, expected)
    
    # Check whether the file already exists in the destination folder. Stop if it does.
    if os.path.isfile(out_file_path):
        print "{:s} already exists - Skipping and moving onto the next file".format(expected)
        return

    # Generate a unique ID
    uuid_str = str(uuid.uuid4())

    # Copy the source file to the target folder with a temporary name [UUID].tmp.
    temp_file = "{:s}.tmp".format(uuid_str)
    tmp_out_file_path = os.path.join(DESTINATION_FOLDER, temp_file)

    if JUST_COPY: 
        copyfile(in_file_path, tmp_out_file_path)
    else:
        os.rename(in_file_path, tmp_out_file_path)
     
    # Rename the copy to [UUID].tmp to [UUID].mole.
    mole_file = MOLE_FILENAME.replace(MOLE_FILENAME_REPLACEMENT_TOKEN, uuid_str)
    mole_out_file_path = os.path.join(DESTINATION_FOLDER, mole_file)
    os.rename(tmp_out_file_path, mole_out_file_path)

    ### simple copy
    final_file_path = os.path.join(DESTINATION_FOLDER, expected)
    os.rename(mole_out_file_path, final_file_path)

    ### copy using whack a mole algorithm
    # Look for any other files matching the pattern [UUID].mole.
    #list_moles(uuid_str, mole_file)

    # If their UUID compares greater than yours, attempt to delete it. (Don't worry if it's gone.)

    # If their UUID compares less than yours, attempt to delete your own. (Again, don't worry if it's gone.) From now on, treat their UUID as if it were your own.

    # Check again to see if the destination file already exists. If so, attempt to delete your temporary file. (Don't worry if it's gone. Remember your UUID may have changed in step 5.)

    # Attempt to rename your temporary file to its final name, <target>. (Don't worry if it's gone.)



'''
'''

def list_moles(uuid_str, mole_file_name):
    existing_files = os.listdir(DESTINATION_FOLDER)
    for existing in existing_files:
        if MOLE_FILENAME_EXTENSION in existing:
            existing_uuid = existing.replace(MOLE_FILENAME_EXTENSION, "")
            print "exisitng {:s}".format(existing_uuid)
            if existing_uuid > uuid_str:
                existing_file = os.path.join(DESTINATION_FOLDER, existing)
                remove_file(existing_file)
            else:
                existing_file = os.path.join(DESTINATION_FOLDER, mole_file_name)
                remove_file(existing_file)




'''
'''
def get_expected_file():
    part_counter_str = str(input_part_counter)
    fileName = EXPECTED_FILENAME.replace(EXPECTED_FILENAME_REPLACEMENT_TOKEN, part_counter_str)
    return fileName


'''
'''
def advance_count():
    global input_part_counter
    input_part_counter += 1


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
            print "%s file detected." % filepath
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
    else:
         print "%s not found." % filepath
    return locked


'''

'''
def remove_file(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


'''
    This file is run as the main program

'''
if __name__ == "__main__":
    main(sys.argv[1:])

