# Multi-board-simulation
A python based simulator of the workload of cpus inside different boards

############ SOFTWARE DESCRIPTION ############

CLASSES:

### COMPONENTS ###

 CLASS CPU:
	params:
		-temperature of the cpu
		-power consumption
		-task to execute
		-status of the cpu [0->3 from 'healthy' to 'broken']
	
	functions:
		-assign_task
		-set_status
		-reset, reset cpu to default parameters
		-execute_task, compute time when the task will be completed

CLASS BOARD
	params:
		-cpus, list of cpus inside the board

	functions:
		-assign task/fault cpus
		-self_report, collect data from cpus

CLASS NETWORK
	params:
		-boards, list of boards inside the network
	functions:
		-assign list of tasks/faults to board
		-reset components
		-update components (simulate a step in time)
CLASS TASK
	params:
		-base execution time	
		-standard deviation execution time
		-is_periodic, a periodic task restart after completion
	function:
		-execute, compute the time that cpu has to spent to complete the task 

### ENGINE ###

CLASS SIMULATION: 
	params:
		-SIM_TIME, global time of the simulation
		-DELTA_TIME, time interval between steps in the simulation
	functions:
		-running_simulation, update every components in the network for the time-interval chosen
		-interact_with_object, function to comunicate with the network (assign task/fault, reset component, get data status from cpus)

############ RUNNING THE SIMULATION ############

Running the main file script, the simulation will start with the following example:

Network components: 1 board with 4 cpus 

1 - assign tasks to the 4 cpus
2 - running the simulation for 30 [virtual] seconds
3 - remove task from cpu 0
4 - running the simulation for 40 [virtual] seconds
5 - set to status 3 all the cpus
6 - running the simulation for 0.5 [virtual] seconds

If you want to use the code:

-Create a dictionary to specify the value of parameters inside the network "variabile params in the main file",
-Set up the components of the network 
-Use the function of the class SIMULATION to comunicate with the network:
	assign task/fail, get status data, reset
	running the simulation for how much do you need 