***********
miloPlot.py
***********

Overview
########

This program is intended to be used to generate plots from an OTIS4 plot file using  matplotlib.pyplot and numpy.

I wrote this  code to facilitate getting trajectory results plotted and inserted in
powerpoint and keynote. You might notice that the varible titles change based on the 
number of subplots along with the number of y gridlines.

miloPlot has successfully run using python 2.7x on macOS and debian linux.
miloPlot has also successfully run using python 3.6x on win10.

 written by S.W.Paris January 2017
   Paris Aerospace Technologies

This is version 0.9 
   things that still need to be done
     expand the titles to include more otis ABLOCK variables
     add help function(s)
     better documentation
 
   Copyright (C) 2017  Paris Aerospace Technologies

Dependencies
############

numpy
matplotlib

Installation
############

You might want to add location of miloPlot.py in your PATH

Running
#######

miloPlot.py is just a python program. There are several ways to run it
I always use the terminal (command_line).

option 1 interactive (run from the "terminal")

::

    [yourComputersPrompt]python miloPlot.py

This will launch an interactive session where you will be prompted for the files
that contain the data to be plotted. You will also be prompted for the variables to be
plotted. An example interactive session is shown in the file interactiveSession.txt

option 2 uses a file of commands to drive the program.  This is launched from the 
terminal as follows

::

    [yourComputersPrompt] python miloPlot.py -f commandsFile


commandFile is just a text file with the following form

::

    inputFile nameOfYourFirstDataFile optionalDatalegend
    inputFile nameOfYourNextDataFile  optionalDatalegend
                                    - you can repeat this as many times as you like
                                      testing has been limited to 3 files or less
    outputFile  nameOfYourOutputPdfFile - this is optional, if you do not specify an
                                        outputfile is is set to miloPlot.pdf
    plot xVariableName yVariableName - there can be multiple y variable names
                                       each y variable is plotted on a separate subplot
                                       repeat plot lines for each new plot

Examples of commandFiles are included as commands1.txt and commands2.txt. 
If you request plots of variables in the commandFile that aren't in the data file,
miloPlot just ignores those inputs.
                                       
option 3 you can always use a script that contains the interactive commands

This is launched from the terminal as follows

::

    [yourComputersPrompt]python miloPlot.py < script.txt

An example script file is included as script.txt

Also included in the repository are three example data files, which are variations on the
Bryson minimum time for a supersonic interceptor trajectory

::

   test1.op1
   test2.op1
   test3.op1                                                                                                                
     
License
#######

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Disclaimer
##########

My python skills are primitive at best, but this code does what I need it to do. It you find it useful great. If you see better ways to do things, let me know.

My "go to" reference for this work was the book:
A Student’s Guide to Python for Physical Modeling, by
Jesse M. Kinder & Philip Nelson

An awesome quick start for python. 
