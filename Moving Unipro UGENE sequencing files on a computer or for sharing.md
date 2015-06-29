# Moving Unipro UGENE sequencing files on a computer or for sharing

This covers moving the files around on a local computer or sharing on Dropbox shared folder or shared network server. Plus sending by e-mail.

** DO NOT MOVE OR COPY UGENE FILES WITH THE INVOLVED PROJECT OR FILES OPEN IN THE UGENE PROGRAM. THIS WILL TRIGGER THE PROGRAM TO TRY AND SAVE ADDITIONAL PROJECT INFORMATION THAT MAY OVERWRITE YOUR GOOD INFORMATION INADVERTANTLY ***

Also it is highly recommended you back up your drive prior to initiating anything like this and you do any adjustments that involve opening up files in UGENE somewhere that is backed up with each version as you work, i.e., a folder monitored by Dropbox. I have found it very easy to irreversibly destroy such files trying to play around with them.


## Background

It is helpful to understand that there can be up to three files for each project.

- The sequence and annotations files should be together in the project folder along with your project data information file that ends in the extension `.uprj`. You do not need any information from this file to perform the conversion, but examining it in your text editor or UGENE may help you identify the specific, related sequence and feature annotations files you need to do the conversion.

- The UGENE sequence will be a FASTA format sequence file ending in `.fa`. You need to indentify the specific sequence file related to the specific molecule you are trying to port over to Serial Cloner. Your project folder may or may not have additional files with the same extension in it depending on how you choose to work with UGENE and its project and documents. These will be the sequences of other molecules in that project.

- The file with the feature annotations will end in `.gb`. You need to identify the specific Genbank-like formatted feature annotations file related to the specific molecule you are trying to port over to Serial Cloner. Your project folder may or may not have additional files in it with the same extension depending on how you choose to work with UGENE and its project and documents. These will be the annotations for other molecules in that project.


It seems to the case that when, under the `Cloning` entry under `Actions` you use `Create fragment..` to make fragments that you then use to `Construct molecule..`, this generates a Genbank-like format with extension `.gb` that has both the sequence and annotations, and there is no corresponding `.fa` file. And thus the Genbank file UGENE generates is more like typical Genbank file in these cases. (I still don't understand the reasoning for the different results yet.)

** DO NOT MOVE OR COPY UGENE FILES WITH THE INVOLVED PROJECT OR FILES OPEN IN UGENE PROGRAM. THIS WILL TRIGGER THE PROGRAM TO TRY AND SAVE ADDITIONAL PROJECT INFORMATION THAT MAY OVERWRITE YOUR GOOD INFORMATION INADVERTANTLY ***


## The issue

So far from my limited experience, it seems you need several files to properly move a sequence and its annotated features so they will open correctly in UGENE after a move or copying. If you don't copy everything, the program won't know which sequence file (ends in `.fa`) and annotated features file (ends in `.gb`) are linked.


## Solution
IMPORTANT: Close all instances of the UGENE program before moving or copying.

If you move the directory containing all the project files, everything should continue to work. (On a Mac you can hold down option to click and drag to copy.)

It also seems with the UGENE software closed you can change the folder it is in by simply changing the name of the folder that is ABOVE the project file, genbank files, and annotated files.

Alternatively, copying can be done by using the `Export project` to move the files with UGENE open.

- From the `File` menu > `Export project` , specify a destination folder name and click ' `...` to navigate to your new location or shared folder and click `Export`.



## Caveats

CAUTION: When moving or copying, don't change the project or file names WITHIN the directory.
Changing any names of the component files will destroy associations because the path information seems to be stored in BOTH text and binary form inside the mixed form of the data in the project data information file that ends in the extension `.uprj`. When the association link is lost the features aren't show on the sequence in UGENE even though you load the sequence file in to the program. You'll see a red dialog box on the bottom right corner and clicking on that will relate some of the issue. (At least this is what I have surmised. After I changed file names for the `.fa` and `.gb` files I did try to change the text part within the project data information file that ends in the extension `.uprj` and even with this change the association gets destroyed so the information seems to be elsewhere in file. You can revert the changes and it will restore the sequence file and annotations association as long as you don't try this with UGENE still open. It will become irreversibly broken if you try with it open and even copying in a the original `.uprj` project file won't fix it although I cannot understand why.)

And as mentioned several times above, ALWAYS close all instances of UGENE before trying to move or copy anything. This insures the program doesn't autosave any information about the data project to a file that is no longer present.

Also it is highly recommended you back up your drive prior to initiating anything like this and you do any adjustments that involve opening up files in UGENE somewhere that is backed up with each version as you work, i.e., a folder monitored by Dropbox. I have found it very easy to irreversibly destroy such files trying to play around with them.


## E-mailing

Zip up (compress) the entire directory with the sequence and annotations files and send via e-mail. The receiver should be able to unpack and point UGENE at the project file ending in the extension `.uprj` and open the sequence and annotations.


