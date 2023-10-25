# Multi-board-simulation
A python based simulator of the workload of cpus inside different boards

### SOFTWARE DESCRIPTION 

#### COMPONENTS 

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

#### ENGINE ###

CLASS SIMULATION: 

	params:
		-SIM_TIME, global time of the simulation
		-DELTA_TIME, time interval between steps in the simulation
	
	functions:
		-running_simulation, update every components in the network for the time-interval chosen
		-interact_with_object, function to comunicate with the network (assign task/fault, reset component, get data status from cpus)

### RUNNING THE SIMULATION 

Running the main file script, the simulation will start with the following example:

Network components: 1 board with 4 cpus 

1 - assign tasks to the 4 cpus

2 - running the simulation for 30 [virtual] seconds

3 - remove task from cpu 0

4 - running the simulation for 40 [virtual] seconds

5 - set to status 3 all the cpus

6 - running the simulation for 0.5 [virtual] seconds

### If you want to use the code:

-Create a dictionary to specify the value of parameters inside the network.
```
    params = \
        {
            "delta_time": 0.5,  # Time interval between steps in the simulation
            "num_boards": 1,
            "num_cpus": 4,
            "cpu": {
                "time_change_status": 10.,  # Time interval to start to change statu when the cpu is running
                "status": 0,
                "temperature": 45.0,
                "power": 12.0
            },
            "task": {
                0: {
                    "base_execution_time": 10.0,
                    "std": 0.5,
                    "periodic": True
                },
                1: {
                    "base_execution_time": 7.0,
                    "std": 0.2,
                    "periodic": True
                },
                2: {
                    "base_execution_time": 5.0,
                    "std": 0.1,
                    "periodic": False
                },
                3: {
                    "base_execution_time": 3.0,
                    "std": 0.08,
                    "periodic": False
                }
            }
        }
```
-Set up the components of the network 
```
    # Create tasks
    task_params = _params.get("task")
    list_tasks = [Task(idx,
                       base_execution_time=task_params.get(idx)['base_execution_time'],
                       std=task_params.get(idx)['std'],
                       is_periodic=task_params.get(idx)['periodic']) for idx in task_params.keys()]

    # Create Network
    num_boards = _params.get("num_boards")
    num_cpus = _params.get("num_cpus")
    net = Network(num_boards=num_boards, num_cpus=num_cpus, _random=random, _params=_params)

    # Create Simulation
    sim = Simulation(_object=net, delta_time=_params.get('delta_time'))
```
-Use the function of the class SIMULATION to comunicate with the network:
- assign task/fail, get status data, reset
```
    sim.interact_with_object(data, is_assign_task=True)
    or
    network_status, debug_text = sim.interact_with_object(is_get_data=True)
    or
    sim.interact_with_object(data, is_assign_task=True, is_fault=True)
    or
    sim.interact_with_object(data, is_reset=True)
```
- running the simulation for how much do you need 
```
    sim.running_simulation(time_interval=TIME)
```