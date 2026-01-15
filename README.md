# 3-Body-Problem
3 body problem with modified mass of Jupiter


## Overview
This problem is aimed to predict the position of three different bodies of mass (in this case the Sun, Earth, and Jupiter) given an initial and final time. While we do have equations to fully predict the motion of two gravitating masses, analytical tools fall short when facing more populated syestems. It is not possible to derive a general formula for three or more gravitating objects due to the amount of unknown variables an n-body system contains.

## Physics / Math Background
Short description of the physical system or theory involved.

## Methods
- We begin by importing the packages needed for this simulation. I used math, numpy, and pylab. Forces between each body involved are defined and broken up into sin and cos components. Velocity and acceleration are also defined in order to be used for out ODE solvers.

  Using the Euler-Cromer and Runge-Kutta (RK4) methods, we are able to solve our ODEs with high accuracy. Masses, distance, time, and forces for our three bodies are defined and normalized. A initial and final time are selected for the simulation and vectors are defined for the postion of our masses. Plot commands are given such that the path taken by each body involved is traced.  



## Results
- An example output for this code is given below. The initial conditions of the simulations included a initial time of zero and a final time of 12 years with Jupiter having 500x it's original mass:

  <img width="637" height="475" alt="Screenshot 2026-01-14 at 5 37 08 PM" src="https://github.com/user-attachments/assets/4c6e43ab-95fc-47b9-80c9-49119f2468c0" />

  
- With this result, we can see that the earth still stays in orbit around the sun. The path taken is different than from one with the normal mass of Jupitr shown by the following result:

  <img width="638" height="474" alt="Screenshot 2026-01-15 at 1 05 57 PM" src="https://github.com/user-attachments/assets/33b000b7-6b7f-4283-aac1-5ef55f2b4320" />


## How to Run

- In order to run the code, numpy and matplotlib must be installed into the python IDE you are using. The code can be cloned into an editor and ran directly after packages are installed. Code given in the main script will produce an output for 12 years and Jupiter having 500x it's original mass.
  Modifications include the initial time, final time, and the mass factor amount for Jupiter (initially set to 500). Lines 152 and 153 define the initial and final time. Line 149 defines the mass factor of Jupiter, with 1 being the stnadard mass of Jupiter. 
