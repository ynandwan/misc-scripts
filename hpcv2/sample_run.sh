python generate_jobs.py -num_task_per_process 1 -num_process_per_job 6 -template single_run.sh -multi_header multinode_header.sh -multi_template multinode_run.sh -single_job_file sj -multi_job_file mj -jobs_dir hpc_jobs/rrn_equal_abl_rep -job_name rrnabl -selectos :centos=skylake -global_time 5:00 -dump_dir sb3_trained_models/rrn_equal_abl_rep -config configs/sup_bl.yml -test_only 0 -split_into 2 -param_dump_dir 1 -prefix abl_1seed

