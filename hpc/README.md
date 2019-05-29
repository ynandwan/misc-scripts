Script to create multinode hpc jobs.

Usage - 
python create_multinode_jobs.py -num_task_per_process 3 -num_process_per_job 6 -task_script test_dummy_task/dummy_task_script.py

exp_{i}.sh scripts are created in args.jobs_dir. Each exp_{i}.sh script is a process to be run on one node. It fires args.num_task_per_process tasks in parallel.

These processes can be run either individually - via job_{i}.sh or through one of multi_job_{k}.sh.

Each multi node job multi_job_{k}.sh will run args.num_process_per_job number of processes by doing an ssh on each of the node in $PBS_NODESFILE. Ensure that passwordless ssh is enabled and number of nodes selected in args.multi_template are in sync with args.num_process_per_job. By default, each multinode jobs runs 6 processes on total of 3 nodes with 2 gpus per node.

args.single_job_file submits all single jobs  job_{i}.sh via qsub.

args.multi_job_file submits all multi node jobs multi_job_{k}.sh via qsub.

Each command in exp_{i} runs args.task_script with a combination of input arguments as hard-coded in this script. 
Different values of an input argument should be provided as a list and a separate list for each input arg should be provided. 
e.g. params1, params2 and params3 in the create_multinode_jobs.py.  
#Tasks = Cross product of params1, params2 and params3.

Jobs are sorted in the decreasing order of time it takes to run them.

Time of each job is decided by one of the arguments to the task script. 
'timing_key' in the create_multinode_jobs.py should be set to the argument name that decides the time. 
'timing' list contains the time for each job.

NOTE: you may have to modify the last multi node job manually if total number of tasks to be run is not a multiple of args.num_process_per_job*args.num_task_per_process



