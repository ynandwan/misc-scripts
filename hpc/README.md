


**`create_multinode_jobs.py`** is used to create multinode jobs to be run on hpc.

**Use case:** when you want to run a particular task, `args.task_script`, with different combinations of input arguments, hard coded in `create_multinode_jobs.py` as `params1`, `params2` etc.

**Assumption:** 
* `args.task_script` is a python script, run using `$HOME/anaconda3/bin/python`. You can change this at line 74-75.
* Password less ssh is setup properly. Follow http://supercomputing.iitd.ac.in/?FAQ#sshkeys
* Headers are specified properly in `single_run.sh` and `multinode_header.sh`
* `module_load_str` is appropriately set at line 42

**Usage:** 
  
  To print the help string:
  ```python
  python create_multinode_jobs.py -h
  ```

  **To create jobs:**

```python
  python create_multinode_jobs.py -num_task_per_process 3 -num_process_per_job 6 -task_script test_dummy_task/dummy_task_script.py -jobs_dir multinodejobs -multi_job_file all_multi_jobs.sh
  ```
  Creates a directory `jobs_dir` with all the multinode and single node jobs. All jobs are scheduled in one shot via `args.multi_job_file` shell script generated in `args.jobs_dir`

**Update**
To specify the os at the run time, a new argument (selectos) is added. `create_multinode_jobs_sample.py` is a sample that I use to schedule my jobs for a specific task. It might not be generic and you may have to adapt it to your needs.

```python create_multinode_jobs_sample.py -num_task_per_process 2 -num_process_per_job 6 -task_script <task_script> -template single_run.sh -multi_header multinode_header_os.sh -multi_template multinode_run.sh -single_job_file sj -multi_job_file mj -jobs_dir rl -job_name rl -selectos :centos=haswell -global_time 12 ```

---------------------


**Detailed Description:**

`exp_{i}.sh` scripts are created in `args.jobs_dir`. Each `exp_{i}.sh` script is a *process* to be run on one node. It fires `args.num_task_per_process` *tasks* in parallel.

These *processes* can be run either individually - via `job_{i}.sh` or through one of `multi_job_{k}.sh`

Each multi node job `multi_job_{k}.sh` runs `args.num_process_per_job` number of `processes` by doing an `ssh` on each of the node in `$PBS_NODESFILE`. **Ensure that passwordless ssh is enabled and number of nodes selected in `args.multi_template` file are in sync with `args.num_process_per_job`**. By default, each multinode jobs runs 6 `processes` on total of 3 nodes with 2 gpus per node.

`args.single_job_file` submits all single jobs job_{i}.sh via qsub.

`args.multi_job_file` submits all multi node jobs multi_job_{k}.sh via qsub.

Each command in `exp_{i}.sh` runs `args.task_script` with a combination of input arguments as hard-coded in `create_multinode_jobs.py`
Different values of an input argument should be provided as a list and a separate list for each input arg should be provided. 
e.g. `params1`, `params2` and `params3` in `create_multinode_jobs.py`.  
#Tasks = Cross product of `params1`, `params2` and `params3`.

Jobs are sorted in the decreasing order of time it takes to run them.

Time of each job is decided by one of the arguments to the task script. 
`timing_key` in `create_multinode_jobs.py` should be set to the argument name that decides the time. 
`timing` list contains the time for each job.

NOTE: you may have to modify the last multi node job manually if total number of tasks to be run is not a multiple of `args.num_process_per_job*args.num_task_per_process`



