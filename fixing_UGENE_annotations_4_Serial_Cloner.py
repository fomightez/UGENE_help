#! /usr/bin/env python

# fixing_UGENE_annotations_4_ Serial_Cloner.py by Wayne Decatur
# ver 0.1
#
#*******************************************************************************
# USES Python 2.7
# PURPOSE: Takes a UGENE Genbnak file that may have been modified to include the
# sequence and fixes the text in the annotations so upon import into Serial
# Cloner the features are named similar to as they were in UGENE.
#
# In the default conversion without this script, the feature names seems to be
# taken from the 'notes' data and can often result in a less than desirable name.
# This script is meant to help with that.
# The conversion process this is meant to aid in is outlined at
# https://github.com/fomightez/UGENE_help/blob/master/Converting%20UGENE%20sequences%20to%20Serial%20Cloner.md .
#
#
#
# Dependencies:
#
#
# v.0.1. Started. A bit clunky because I wrote it originally forgetting notes
# and possibly names could span more than one line in the .gb file.
#
#
# Caveats: This program will have problems if you use normal quotes in your annotation
# notes and names. Single-quotes shouldn't be a problem. Also, any text with
# "\ " in names entry will be mis-identified by the program as escaped spaces
# generated by Ugene and they will be removed during the conversion process.
#
# To do:
# - Make a version on my fomightez site. Should be easy as this is a small script.
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# python fixing_UGENE_annotations_4_ Serial_Cloner.py file2convert.gb
#-----------------------------------
# Where 'file2convert.gb' would be replaced with your file to convert
# following the process outlined at https://github.com/fomightez/UGENE_help/blob/master/Converting%20UGENE%20sequences%20to%20Serial%20Cloner.md .
#
#
#
#
#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************










#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER ANY VALUES ABOVE###

import os
import sys
#import logging
import argparse
from argparse import RawTextHelpFormatter
#import urllib
#import re


#DEBUG CONTROL
#comment line below to turn off debug print statements
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)



###---------------------------HELPER FUNCTIONS---------------------------------###

def generate_output_file_name(file_name):
    '''
    Takes a file name as an argument and returns string for the name of the
    output file. The generated name is based on the original file
    name.

    Specific example
    ================
    Calling function with
        ("pGEM-T vector.gb")
    returns
        "pGEM-T vector_fixed.gb"
    '''
    main_part_of_name, file_extension = os.path.splitext(
        file_name) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
        return main_part_of_name + "_fixed.gb"
    else:
        return file_name + "_fixed.gb"

def process_recent_lines(lines_list):
    '''
    The function takes the last few lines of text and parses it to
    determine if a `note` present and extracts what UGENE had set as
    the `name` for the annotation.
    Then it takes the content from the `name` record element and either replaces
    the UGENE based `note` record element for the annotation with that (if
    there was an original note, the content from that record element gets
    swapped into the `name` record entry) or it creates a `note` record entry
    from scratch using the text content from the `name` record entry.

    The function returns a multiline text string that is the re-ordered/modified
    annotation.
    '''
    #initialize the results string and intermediate collectors and indicators
    processed_text_string = ""
    lines_before_notes_or_names = ""
    lines_after_notes_or_names = ""
    new_note_content = ""
    new_name_content = ""
    before_notes_or_names = True
    note_originally_had_content = False
    multiline_entry_encountered = False
    collected_multiline_entry = ""
    multiline_note = False
    multiline_name = False
    #define signals
    note_signal = '                     /note="'
    name_signal = '                     /ugene_name="'
    # now go through the lines moving each to appropriate place or extracting
    # needed content
    for current_line in lines_list:
        if multiline_entry_encountered == True:
            #see if signal for complete set of lines, the close quote, there
            if '"' in current_line:
                index_of_quote = current_line.index('"')
                #only want up to quote because default handling had been taking
                # what was between quotes when was on one line and then adding
                # closing quote and next line.
                collected_multiline_entry += current_line[:index_of_quote]
                # since multiline record entry now complete process it
                if multiline_note:
                    new_name_content = collected_multiline_entry
                    # reset for multiline note detection
                    multiline_note = False
                elif multiline_name:
                    new_note_content = collected_multiline_entry
                    # reset for multiline name record detection
                    multiline_name = False
                else:
                    print "problem with multiline record entry being neither a note or name"
                # reset for handling multi-line entry
                multiline_entry_encountered = False
                collected_multiline_entry = ""
            else:
                collected_multiline_entry += current_line
        elif current_line.startswith(note_signal):
            before_notes_or_names = False
            note_originally_had_content = True
            if current_line.count('"') == 2:
                extracted_note_content = current_line.split('"')[1::2][0] # from
                # http://stackoverflow.com/questions/2076343/extract-string-from-between-quotations
                new_name_content = extracted_note_content
            else:
                # NEED TO HANDLE IF NOTE GOES TO NEXT LINE BY COLLECTING NEXT
                # LINE OF TEXT WHEN CLOSE QUOTES NOT PRESENT
                multiline_entry_encountered = True
                multiline_note = True
                collected_multiline_entry = current_line[28:]
        elif current_line.startswith(name_signal):
            before_notes_or_names = False
            if current_line.count('"') == 2:
                extracted_name_content = current_line.split('"')[1::2][0] # from
                # http://stackoverflow.com/questions/2076343/extract-string-from-between-quotations
                new_note_content = extracted_name_content
            else:
                # NEED TO HANDLE IF NOTE GOES TO NEXT LINE BY COLLECTING NEXT
                # LINE OF TEXT WHEN CLOSE QUOTES NOT PRESENT
                multiline_entry_encountered = True
                multiline_name = True
                collected_multiline_entry = current_line[34:]
        elif before_notes_or_names:
            lines_before_notes_or_names += current_line
        else:
            lines_after_notes_or_names += current_line
    # fix so '\ ' are simply spaces
    new_note_content = new_note_content.replace('\ ', ' ') # need to
    # replace because Ugene escapes spaces in `ugene_name` entries to '\ '.
    # Originally tried method used in  Jochen's answer at
    # http://stackoverflow.com/questions/5186839/python-replace-with
    # , but that didn't seem to work, maybe because not escaped in same manner
    # as the text `.decode` meant to handle?
    #
    # now build modified annotation from parts
    middle_content = '                     /note="' + new_note_content + '"\n'
    if note_originally_had_content:
        middle_content += '                     /ugene_name="' + new_name_content + '"\n'
    processed_text_string = (lines_before_notes_or_names + middle_content
        + lines_after_notes_or_names)
    return processed_text_string


def fix_annotation_names(the_file_name):
    '''
    The function takes a file name for a genbank-formatted file from UGENE
    and fixes the information for each annotation so more appropriate text
    gets used in the names in the features instead of whatever was in the
    notes entry.

    The function generates a `fixed` file with a name distinguishing it from
    the input file. The file will be in the same directory as the input file.

    The function returns the following:
        * number of annotations processed
        * output file name
    '''
    # in preparation use the file name to generate a prefix for the
    # name of the output files.
    output_file_name = generate_output_file_name(the_file_name)
    #initialize holder for text that will be output
    new_file_text = ""
    # initialize a list that will be the last few lines of the file when in
    # features section and a counter for annotations processed
    last_few_features_text_lines_list = []
    annotations_processed = 0
    # define signals for sections, see `Notes on the Genbank file format specifications to help with parsing.md`
    # and section 3.4 of ftp://ftp.ncbi.nih.gov/genbank/gbrel.txt
    features_section_start_tag = "FEATURES"
    features_section_end_tags = ["CONTIG", "ORIGIN", "BASE COUNT", "WGS"]
    parsing_feature_section = False

    # open input file and start reading
    input_file_stream = open(the_file_name , "r")
    for line in input_file_stream:
        if line[0:10].strip() == features_section_start_tag:
            parsing_feature_section = True
            new_file_text = new_file_text + line
        elif line[0:10].strip() in features_section_end_tags:
            parsing_feature_section = False
            # end of feature section has been hit and so need to complete the
            # processing of the annotation currently just parsed
            new_file_text = new_file_text + process_recent_lines(
                last_few_features_text_lines_list)
            annotations_processed += 1
            # and add the current line to text that will become output
            new_file_text = new_file_text + line
        elif parsing_feature_section:
            if line[0:10].strip() in features_section_end_tags:
                parsing_feature_section = False
                # need to complete the processing of the annotation
                # currently being parsed
                new_file_text = new_file_text + process_recent_lines(
                    last_few_features_text_lines_list)
                # add the current line to future output
                new_file_text = new_file_text + line
            elif (len(line[5:20].strip()) > 0) and (
                last_few_features_text_lines_list != []):
                # see section 3.4.12.1 of ftp://ftp.ncbi.nih.gov/genbank/gbrel.txt
                # for source of `[5:20]` above first part. I added the checking
                # that the last few lines list not empty so that when it hits
                # the very first feature key name, it doesn't add 'note="' at
                # start of the feature section.
                #
                # Next feature has been hit so need to complete the processing
                # of the annotation just parsed
                new_file_text = new_file_text + process_recent_lines(
                    last_few_features_text_lines_list)
                annotations_processed += 1
                # set collecting lines list to this current line which is start
                # of new annotation
                last_few_features_text_lines_list = [line]
            else:
                last_few_features_text_lines_list.append(line)
        else:
            new_file_text = new_file_text + line
    #Completed scan of input file and therefore close file, write new files,
    # and return details for making feedback to user.
    input_file_stream.close()
    output_file = open(output_file_name, "w")
    output_file.write(new_file_text.rstrip('\r\n')) #rstrip to remove trailing newline
    # from http://stackoverflow.com/questions/275018/how-can-i-remove-chomp-a-newline-in-python
    # That chomp just insures everything clean at the end and no extra new line added.
    output_file.close()
    return (annotations_processed, output_file_name)




###--------------------------END OF HELPER FUNCTIONS---------------------------###







###-----------------Actual Main function of script---------------------------###
###----------------------GET FILE AND PREPARE TO PARSE-----------------------###
#file to be provided as a argument when call program.
#argparser from http://docs.python.org/2/library/argparse.html#module-argparse and http://docs.python.org/2/howto/argparse.html#id1
parser = argparse.ArgumentParser(
    prog='fixing_UGENE_annotations_4_ Serial_Cloner.py',description="fixing_UGENE_annotations_4_ Serial_Cloner.py fixes the annotations in the Genbank style output from UGENE\n so that the corresponding feature is named appropriately upon import into Serial Cloner.\n\nWritten by Wayne Decatur --> Fomightez @ Github or Twitter.  \n \nCaveat: The program will fail to resolve annotation notes and names correctly if they contain normal quotes. Single-quotes shouldn't be a problem.\nActual example what to enter on command line to run program:\npython fixing_UGENE_annotations_4_ Serial_Cloner.py input_file.gb\n \n \n \n ", formatter_class=RawTextHelpFormatter
    )
#learned how to control line breaks in description above from http://stackoverflow.com/questions/3853722/python-argparse-how-to-insert-newline-the-help-text
#DANG THOUGH THE 'RawTextHelpFormatter' setting seems to apply to all the text for argument choices. I don't know yet if that is what really what I wanted.
parser.add_argument("InputFile", help="name of Genbank-formatted file being used in the conversion from UGENE to Serial Cloner. REQUIRED.")
#I would also like trigger help to display if no arguments provided because need at least input file
if len(sys.argv)==1:    #from http://stackoverflow.com/questions/4042452/display-help-message-with-python-argparse-when-script-is-called-without-any-argu
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if os.path.isfile(args.InputFile):
    the_file2fix = args.InputFile


    #Read in Genbank-formatted file and fix it.
    #THIS FUNCTION CALL IS THE MAIN POINT OF THIS PROGRAM.
    sys.stderr.write("Reading in your file...")
    number_of_annotations, output_file_name = (
        fix_annotation_names(the_file2fix))

    #FOR DEBUGGING
    #logging.debug(number_of_annotations)

    #give user some stats and feeback
    sys.stderr.write("\nConcluded. \n")
    sys.stderr.write("There were "+ str(number_of_annotations)+" annotations fixed. ")
    sys.stderr.write("\nA file named '"+
        output_file_name+"' was saved with the results "+
        "\nin same directory as the input file.\n\n")


else:
    sys.stderr.write("SORRY. " + args.InputFile + " IS NOT RECOGNIZED AS A FILE.\n\n")
    parser.print_help()
    sys.exit(1)


#*******************************************************************************
###-***********************END MAIN PORTION OF SCRIPT***********************-###
#*******************************************************************************
