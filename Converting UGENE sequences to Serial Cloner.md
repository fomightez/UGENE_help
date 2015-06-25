# Converting a Unipro UGENE sequence to Serial Cloner

This describes how to take a sequence with annotated features and move it into [Serial Cloner](http://serialbasics.free.fr/Serial_Cloner.html) with your favorite text editor and minimal effort. The annotated features from [Unipro UGENE](http://ugene.unipro.ru/) will ultimately be intact and displayed in Serial Cloner if you follow this process. One of the reasons for possibly doing this is in order to take advantage of the tools in Serial Cloner that UGENE seems to lack/approaches differently, in particular Serial Cloner allows for easily making and printing full graphical `Graph Maps` or classical restriction sequence maps (`Seq. Maps`) with features and restriction sites indicated.


## Step 1: locate UGENE-generated files you'll need

You'll need to find the sequence and the associated annotations that UGENE generated. How to do this requires some examination of your UGENE files:

	- The sequence and annotations files should be together in the project folder along with your project data information file that ends in the extension `.uprj`. You do not need any information from this file to perform the conversion, but examining it in your text editor or UGENE may help you identify the specific, related sequence and feature annotations files you need to do the conversion.

	- The UGENE sequence will be a FASTA format sequence file ending in `.fa`. You need to indentify the specific sequence file related to the specific molecule you are trying to port over to Serial Cloner. Your project folder may or may not have additional files with the same extension in it depending on how you choose to work with UGENE and its project and documents.

	- The file with the feature annotations will end in `.gb`. You need to identify the specific Genbank-like formatted feature annotations file related to the specific molecule you are trying to port over to Serial Cloner. Your project folder may or may not have additional files in it with the same extension depending on how you choose to work with UGENE and its project and documents.

## Step 2: Prepare a 'bridging file' to be used for importing into Serial Cloner

You'll need to add the sequence from `.fa` file to the bottom of the `.gb` to make a Genbank file in a format that Serial Cloner will identify and use. The steps for that follow:

	- In a good text editor equipped to handle coding, like [Sublime Text](http://www.sublimetext.com/) or [Brackets](http://brackets.io/) or TextWrangler (basically, anything aside from Window's Notepad, Microsoft Word, or other too basic text software/too fancy Word Processing software), open the UGENE file with the feature annotations that ends in `.gb`.

	- So that you don't destroy your UGENE files and projects, immediately save the `.gb` file as another name, preferably in a new directory. Once it is saved you are ready to edit it safely.

	- The sequence will be placed right before the `//` at the end of the `.gb` gile. It has to be prefixed by a signal. Therefore on the line just above `//`, type `ORIGIN` and hit return. Now that you have the `ORIGIN` signal that indicates a sequence follows, you paste in the sequence in the next line.
	- Open in a text editor the sequence `.fa` file identified above and copy the sequence portion and then paste it on the line after `ORIGIN` in the `.gb` file you are making.

	- Save the 'bridging' `.gb` intermediate file and close it.


## Step 3: Bring the sequence and annotations into Serial Cloner

	- Right click the combined `.gb` and select to open it in Serial Cloner.

	- It will give a message that you imported a NCBI-formatted Genbank file.

	- Your full sequence should be there. As a verification of the process thus far, it is advised you confirm the length matches.

	- Toggle on `circular` option in the `Sequence` tab if the sequence is a plasmid.

## Step 4: Enable the imported annotated features to show in Serial Cloner

	- Go to the `Features` tab and click `Edit` in the bottom right corner of the features window so you can toggle on `Show`.

	- Toggle on `Show` in the bottom left so all the features will show in Serial Cloner tools. The will become bold text when `show` is enabled.

Sadly, you have to do them one by one. I have not found a way to selected all of them at once.

## Step 5: Save as Serial Cloner '.xdna' format and clean up

- Save the file so you can open it in Serial Cloner later without needing to repeat all these steps. It is advised that you save it in a manner to clearly distinguishable from the UGENE files, optionally even in a separate folder.
*Helpful tip*: The saved file will end in the Serial cloner `.xdna` extension, and so if you have extensions viewable it should still be distinguishable even if the file name or folder doesn't clearly indicate.

- Now you can make and print `Graph Maps` or `Seq. Maps` using the tool bar buttons in Serial Cloner and the imported features will be visible.

- You should delete the intermediate, 'bridging file' at this point to avoid confusion later.

## Additional notes

There is a separate Serial Cloner Genbank format that Serial Cloner can save and import. This format includes color and other information in the features list. You could optionally take advantage of this ability and add related code if you want at `step #2`. I considered making a script to do some of these steps, particularly the optional ones, but the process as described here is more transparent and seems acceptable for now.
