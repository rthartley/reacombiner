ReaCombiner
The purpose of the program is to collect all of your Reaper projects in one, place, to 
show an archive the essential aspects of each project, and to print out the same
information for later reference. It does not replace Reaper itself in any way, and is
incapable of changing anything in the .rpp file.

The essential parts of a project

Since a Reaper project consists of a bunch of tracks each of which contains a bunch of items,
it makes sense to use this hierarchy. At the project level, the properties shown are:
ReaCombiner is opinionated in that a folder structure containing reaper projects is as follows.

 - top level folder: project name
 - next level: mixes as .rpp files
 
For instance, we might have
 - Awesome Song
   - Mix1.rpp
   - Mix2.rpp
   - etc.
   
Other essential project components are the plugins used, and the location of audio 
files. 

The ReaCombiner project
 - name
 - mix name
 - date last modified
 - location
 - tempo
 - record path (if any)
 - sample rate
 - project notes (if any)
 
The ReaCombiner track
 
  - track number
  - track name
  - main send (yes or no)
  - volume
  - pan
  - receives (list of track numbers)
  - track notes (if any)
  
The ReaCombiner item
 - item name
 - item source (Usually WAVE, MIDI or MP3)
 - position (seconds)
 - file name
 
The ReaCombiner plugin
 - plugin name
 - plugin file name
 - preset (if any)
 
The display

The display consists of three tables and a bunch of fixed labeled fields. The
'Projects' table shows all stored projects by name and mix/date. Clicking on a row
shows th tracks for that project in the 'Tracks' table, by number of name.
Clicking on a track shows the track's items in the 'Items' table, by name,
source and position.

The File menu
Three actions are available in the File menu:

 - Add Project: a dialog to browse to an .rpp file is shown; the project is
 added to end of the Projects table
 - Delete Project: a dialog is shown for confirmation before the project is deleted
 from the archive; a project table row must be selected first
 - Print Project: a dialog to browse to a folder is shown; a project table row must
 be selected first; the output is a PDF file
 
The Run menu
  A selected project/mix can be opened by Reaper by selecting a row in the Projects table
 an then choosing Run/Run Reaper. ReaCombiner will remain open while Reaper runs and
 may be continued after Reaper exits. At the time of writing any changes to the file
 will not be reflected in ReaCombiner. Either the mix was changed, in which case 
 deleting and adding project/mix again will solve the problem, or a new mix was added, in
 case, adding the new mix will work.
 
The Help menu
  Selecting Help displays this file.
 
