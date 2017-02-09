#!/usr/bin/env python
######################################################################################################
#*--* *- *-* ** ***     *- * *-* --- *** *--* *- -*-* *     - * -*-* **** -* --- *-** --- --* ** * ***
######################################################################################################
"""  
  miloPlot.py Version 0.92

  This program is intended to be used to generate plots from an OTIS4 plot file using 
    matplotlib.pyplot and numpy. Should work with python 2.7x and python 3.x
 
   written by S.W.Paris January 2017
     Paris Aerospace Technologies
   updated by S.W.Paris February 2017
      
    recent changes
      - more input error checking 
      - fixed an issue where miloPlot.pdf was getting corrupted
      - using docstrings instead of comments to describe what each code module does
        
    things that still need to be done
      expand the titles to include more otis ABLOCK variables, 
          maybe allow for a file input of titles
      add help function(s)
      more os testing -  so far only macOS, debian Linux & win10
      
   Copyright (C) 2017  Paris Aerospace Technologies
 
 
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
 
        http://www.apache.org/licenses/LICENSE-2.0
 
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
 
"""
######################################################################################################
#*--* *- *-* ** ***     *- * *-* --- *** *--* *- -*-* *     - * -*-* **** -* --- *-** --- --* ** * ***
######################################################################################################
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
######################################################################################################
# fix for python2.x and python 3.x compatibility
try:
    input = raw_input
except NameError:
    pass
######################################################################################################
def done(trigger):
     """
     done checks for a trigger word (quit) to terminate the program
     """
     if trigger.upper()[:4] == "QUIT" :print("");sys.exit()
     return 
######################################################################################################
def readCommands(file):
   """
   readCommands reads the command file and extracts the commands
   and associated data  
   """
#  read first line to get parameter names
   with open(file, 'r')as fInput:
       line = fInput.read().splitlines()
# done reading the file
   fInput.close()
   return (line)
######################################################################################################
def readPlotFile(file):
   """
   readPlotFile reads an OTIS plot file and extracts & stores the variable names
   and associated data
   """  
   inputNames=[]
   rawData=[]
   inputValues=[]
   inputNumVars=0
# read first line to get parameter names
   with open(file, 'r')as fInput:
       line = fInput.readline()
       inputNames =(' '.join(line.split())).split(" ")
       inputNumVars=len(inputNames)
#read blank line    
       line = fInput.readline()
       dummy =(' '.join(line.split())).split(" ")   
#read data
       for line in fInput:
          rawData=(' '.join(line.split())).split(" ")
# check for explicit trajectory
# and don't use that data for now       
          if len(rawData)<inputNumVars : break
# store data in a list for now       
          for data in rawData:inputValues.append(float(data))
# done reading the file
   fInput.close()
   return (inputNames,inputValues)
######################################################################################################
def mash(file1Names,file2Names):
   """
   mash combines two lists adding non duplicates from the second list 
   to the end of the first list
   """
   for var in file2Names:
      add=True
      for var2 in file1Names:
         if var==var2:
           add=False
           break
      if add:file1Names.append(var)
   return (file1Names) 
######################################################################################################
def writeNames(names):
  """
  writeNames writes a formated list of variables
  I suspect there is a better way to do this -- please share with me
  """
  print(" Variables available for plotting")
  namesPerLine=8
  for i in range(len(names)):
     sys.stdout.write("{:20s} ".format(names[i]))
     if (i+1)%namesPerLine==0:sys.stdout.write("\n".format())
  if len(names)%namesPerLine !=0 :sys.stdout.write("\n".format())
  sys.stdout.flush()
  return
######################################################################################################
def verifyIndex(var,names):
   """
   verify that the selected variable is in the masterList
   """
   iVar=' Enter the '+var+' variable '
   iError=True
   while iError:
     sVar=input(iVar) 
     done(sVar)
     try:
       sIndex=names.index(sVar)
     except:
       print("")
       print(('   {} not in the list of variables, try again').format(sVar))
     else:
       iError=False
   return (sVar)
######################################################################################################
def findIndex(var,names,jFile):
  """
  find index find where var is located in the list names
  """
  try:
    sIndex=names.index(var)
  except:
    print("")
    print(('Warning {} not in the list of variables for file {}').format(var,jFile))
    sIndex=-99
  return sIndex
######################################################################################################
######################################################################################################
def setTitle(var,numPlots):
   """
   setTitles assigns the plot axis labels - long ones for 1-2 subplots(numPlots,level=1),
           short ones for 3-4 (level=0), variable names for 5 and above
   """
   plotTitles={
     "ACCA":["Axial Accel, g's","Axial Acceleration, aA, g's"],
     "ACCN":["Norm Accel, g's","Normal Acceleration, aN, g's"],
     "ACCT":["Total Accel, g's","Total Acceleration, aT, g's"],
     "ALPHAD":["Angle Attack,deg","Angle of Attack, alpha, degrees"],
     "ALT":["Altitude, ft","Altitude, h, feet"],
     "AZMD":["Azimuth Ang, deg","Azimuth Angle, azm, degrees"],
     "BETAD":["Sideslip Ang,deg","Sideslip Angle, beta, degrees"],
     "CD":["Drag Coef,CD","Drag Coefficient, CD"],
     "CDOT(1)":["Control Rate(1)","Control Rate(1)"],
     "CDOT(2)":["Control Rate(2)","Control Rate(2)"],
     "CDOT(3)":["Control Rate(3)","Control Rate(3)"],
     "CL":["Lift Coef, CL","Lift Coefficient, CL"],
     "DRAG":["Drag, lbs","Drag, D, lbs"],
     "DVATM":["Drag Loss, f/s","Drag Loss, DLoss,  f/s"],
     "DVG":["Gravity Loss, f/s","Gravity Loss, gLoss, f/s"],
     "DVI":["Ideal Vel, f/s","Ideal Velocity, dvi, f/s"],
     "DVTV":["Thr Vec Loss,f/s","Thrust Vector Loss, TVLoss, ft/sec"],
     "GAMD":["FltPathAngle,deg","Flight Path Angle, gamma, degrees"],
     "GCR":["Range, nm","Great Circle Range, R, n.miles"],
     "GDALT":["Geodetic Alt,ft","Geodetic Altitude, gdAlt, feet"],
     "GDLATD":["Geodetic Lat,deg","Geodetic Latitude, gdLat, degrees"],
     "HA":["Apogee Alt, nm","Apogee Altitude, Ha, n.miles"],
     "HP":["Perigee Alt, nm","Perigee Altitude, Hp, n.miles"],
     "INCD":["Inclination, deg","Inclination, inc, degrees"],
     "ISP(1)":["ISP(1), sec","Specific Impulse Engine 1, ISP(1), sec"],
     "ISP(2)":["ISP(2), sec","Specific Impulse Engine 2, ISP(2), sec"],
     "ISP(3)":["ISP(3), sec","Specific Impulse Engine 3, ISP(3), sec"],
     "LATD":["Latitude, deg","Latitude, LATD, degrees"],
     "LIFT":["Lift, lbs","Lift, L, lbs"],
     "LOND":["Longitude, deg","Longitude, lon, degrees"],
     "MACH":["Mach Number, M","Mach Number, M"],
     "MASS":["Mass, slugs","Mass, m, slugs"],
     "PHID":["Roll Ang, deg","Roll Angle, phi, degrees"],
     "PSID":["Yaw Angle, deg","Yaw Angle, psi, degrees"],
     "Q":["DynPres, psf","Dynamic Pressure, q, psf"],
     "QALPHA":["qAlpha, psf-deg","qAlpha, psf-degrees"],
     "QDOT(1)":["Heating Rate(1)","Heating Rate, QDOT, btu/ft^2"],
     "RAD":["Radius, ft","Radius, ft"],
     "RANC":["Crossrange, nm","Crossrange, CR, n.miles"],
     "RAND":["Downrange, nm","Downrange, DR, n.miles"],
     "SIGMAD":["Bank Angle, deg","Bank Angle, sigma, degrees"],
     "THETAD":["PitchAng, deg","Pitch Angle, theta, degrees"],
     "THRUST":["Thrust, lbs","Thrust, T, lbs"],
     "TIME":["Time, seconds","Time, t, seconds"],
     "TVAC(1)":["Tvac(1), lbs","Engine 1 Vacumn Thrust, Tvac(1), lbs"],
     "TVAC(2)":["Tvac(2), lbs","Engine 2 Vacumn Thrust, Tvac(2), lbs"],
     "TVAC(3)":["Tvac(3), lbs","Engine 3 Vacumn Thrust, Tvac(3), lbs"],
     "TWALL(1)":["Stagnation Temp","Stagnation Temperature, Twall"],
     "VEL":["Velocity, f/s","Velocity, V, f/s"],
     "WDOT":["Wdot, lbs/sec","Wdot, lbs/sec"],
     "WEIGHT":["Weight, lbs","Weight, W, lbs"]}        
   level=0
   if numPlots <= 2:level=1 
   if numPlots > 4:title=var;return title      
   title=plotTitles.get(var,["",""])[level]
   if title=="":title=var
   return title
######################################################################################################
# miloPlot 
######################################################################################################  
#
# define things so they are in "global" scope
nFiles=0
allData=[]
dataLegends=[]
allNames=[]
# check to see where the commands are coming from keyboard or file
kbInput=True
helpFlag=False
commands=[]
# check to see if calling arguments exist. 
# If they are check for file flag and read commands from that file
if len(sys.argv) > 1:
  file=str(sys.argv[1])
  if file.lower()[0:2] == "-f":
# read the commands into a string   
    try:
      kbInput=False
      file=str(sys.argv[2])
      commands=readCommands(file)
    except:
      print(("Problems with the command file {}").format(file))
      sys.exit()   
  if file.lower()[0:2] == "-h": 
    helpFlag=True
# set output file 
outputFile='miloPlot.pdf'
# write header to the display 
if kbInput:
  print("")
  print("*--* *- *-* ** ***     *- * *-* --- *** *--* *- -*-* * - * -*-")
  print( "                       miloPlot V0.92")
  print( "      Copyright (C) 2017  Paris Aerospace Technologies")
  print("*--* *- *-* ** ***     *- * *-* --- *** *--* *- -*-* * - * -*-")
# check if a help request was made  
# start reading data from the files
if helpFlag:
  print("######################################")
  print("# help function coming real soon now #")
  print("######################################")
  print("")
if kbInput:
  print("")
  print("enter quit at any prompt to terminate")
  print("")   
iFile=True
legendFlag=False
fileList=[]
while iFile:
  if kbInput:
    print("")
    file=input("Please enter a file name for the plot data\n        enter <CR> to move on to plotting:  ")
  else:
# get file names and legends from the command input file
    localCommand=[]
    if len(commands) > 0:
      localCommands=commands[0].split(" ")
    else:
       print("    blank command file?")
       sys.exit()
    if localCommands[0].lower()[0:9]=="inputfile":
      file=localCommands[1]
      legendIn=""
      if len(localCommands) >2 :legendIn=localCommands[2]
      del commands[0]
      if len(commands) ==0: 
        print("    no plots specified")
        sys.exit()
    elif localCommands[0].lower()[0:10]=="outputfile":
        if len(localCommands[1]) > 0:
          outputFile=localCommands[1]
          del commands[0]
          file=""
    elif localCommands[0].lower()[0:4]=="plot":
        file=""
    else: 
        print("\n  miloPlot terminating")
        print(("##### invalid key word "'"{}"'" in the command file").format(localCommands[0]))
        print("##### error is in the following line from the command file:")
        print(commands[0])
        print("")
        print("No plot files generated")
        print("")
        sys.exit()

# end of file input portion of the command input file    
  if(file==""):iFile=False
# just in case a user takes the prompt literally  
  if(file[:4]=="<CR>"):iFile=False 
  done(file)
  if iFile:
    try:
# clear out the temporary input variables/arrays
      data=np.array([])
      names=[]
# use readPlot to actually read the data      
      names,data=readPlotFile(file)
# if the data read was successful enter the legend and move the data to the "global" variables      
      if kbInput:legendIn=input(" Please enter a data legend for this file:  ")
      dataLegends.append(legendIn)
      if legendIn != "" :legendFlag=True
      allNames.append(names)
      allData.append(data)
      fileList.append(file)
      nFiles+=1
    except:
      print("")
      print((" problems with file {}. Try again ").format(file))
#
# this is where things end up after reading the data files
if kbInput==False:pdf = PdfPages(outputFile)
if kbInput:
  print("") 
  print("") 
# assemble a master list of available plot variables
masterList=[]
#
for j in range(0,nFiles):
  masterList=mash(masterList,allNames[j])
if kbInput:
  writeNames(masterList)
  print("")
makePlot=True

figureNum=1
while makePlot:
  numPlots=1
  yVar=[]
# make sure what we are wanting to plot is at least one of the plot files  
  if kbInput:
    print("")
    xVar=verifyIndex('x',masterList)
# set the y variable for the first plot
    yVar.append(verifyIndex('y',masterList))
#
    fig = plt.figure(figureNum,figsize=(14,9))
    ax=plt.gca()
    ax.set_xlabel(setTitle(xVar,1))
    ax.set_ylabel(setTitle(yVar[0],1))
    ax.get_yaxis().set_label_coords(-0.09,0.5)
    plt.grid(True)
    for j in range(0,nFiles):
      xIndx=findIndex(xVar,allNames[j],fileList[j])
      yIndx=findIndex(yVar[0],allNames[j],fileList[j])
      data=np.array(allData[j])        
      data=data.reshape((len(data)//len(allNames[j]),len(allNames[j])))
# these are usually time points  (data[0,0],data[1,0],data[322,0])   
      if xIndx >= 0 and yIndx >=0: 
        ax.plot(data[:,xIndx],data[:,yIndx],label=dataLegends[j])
        if legendFlag :plt.legend()
# 
  makePlot2=True 
  while makePlot2:
    if kbInput:
      nextStep=input('(a)dd Y,(n)ew plot,(s)how,(quit) ') 
      done(nextStep)
    else:
      nextStep='a'
#        
    if nextStep[0].lower()=='n':
      plt.close()
      break
    if nextStep[0].lower()=='a':      
      if kbInput:
        numPlots+=1
        plt.close()
# input the y for the next plot      
        yVar.append(verifyIndex('y',masterList))
      else:
# continue processing commands from the file  
        localCommands=[]
        localCommands=commands[0].split(" ")
        if localCommands[0].lower() != 'plot' :
          sys.exit()
        elif len(localCommands) < 3 :
          print("     no x y pairs specified")
          sys.exit()
        del commands[0]
        xVar=localCommands[1]
        numPlots=len(localCommands)-2
        for j in range(0,numPlots):
          yVar.append(localCommands[j+2])
        # done with file commands
# loop through the subplots, more than 4 get a bit crunched
      fig = plt.figure(figureNum,figsize=(14,9))

      nBinMax=24/numPlots
      fontSize=12
      for k in range(1,numPlots+1):          
          ax = fig.add_subplot(numPlots,1,k)
          if numPlots > 2: plt.locator_params(axis='y',nbins=nBinMax)
#         if numPlots > 3:fontSize=10
          if k == numPlots: ax.set_xlabel(setTitle(xVar,1),size=fontSize)
          ax.set_ylabel(setTitle(yVar[k-1],numPlots),size=fontSize)
          ax.get_yaxis().set_label_coords(-0.09,0.5)          
#         plt.tick_params(axis='x',labelbottom='off')
          plt.grid(True)
          if k==numPlots:
             ax.set_xlabel(setTitle(xVar,numPlots))
             plt.tick_params(axis='x',labelbottom='on')
#  roll through the files to generate the plot
          for j in range(0,nFiles):
            xIndx=findIndex(xVar,allNames[j],fileList[j])
            yIndx=findIndex(yVar[k-1],allNames[j],fileList[j])
            data=np.array(allData[j])        
            data=data.reshape((len(data)//len(allNames[j]),len(allNames[j])))    
            if xIndx >= 0 and yIndx >=0: 
               ax.plot(data[:,xIndx],data[:,yIndx],label=dataLegends[j])
            if k==1 and legendFlag :plt.legend()
      if kbInput==False:
         pdf.savefig(fig)     
         figureNum+=1
         makePlot2=False 
         if len(commands)==0 or commands[0]=='':# all done - yay!
#           plt.show()
           pdf.close()
           print(("  miloPlot successful exit, plots written to {}").format(outputFile))
           sys.exit()  
    if nextStep[0].lower()=='s':
#     plt.tight_layout()
      plt.show() 
        
######################################################################################################     
#*--* *- *-* ** ***     *- * *-* --- *** *--* *- -*-* *     - * -*-* **** -* --- *-** --- --* ** * ***
###################################################################################################### 
      