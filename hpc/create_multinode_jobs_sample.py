from __future__ import print_function
description_str = "Script to create multinode hpc jobs. \n \
exp_{i}.sh scripts are created in args.jobs_dir. Each exp_{i}.sh script is a process to be run on one node. It fires args.num_task_per_process tasks in parallel.\n \
These processes can be run either individually - via job_{i}.sh or through one of multi_job_{k}.sh. \n \
Each multi node job multi_job_{k}.sh will run args.num_process_per_job number of processes by doing an ssh on each of the node in $PBS_NODESFILE. Ensure that passwordless ssh is enabled and number of nodes selected in args.multi_template are in sync with args.num_process_per_job. By default, each multinode jobs runs 6 processes on total of 3 nodes with 2 gpus per node. \n \
args.single_job_file submits all single jobs  job_{i}.sh via qsub. \n \
args.multi_job_file submits all multi node jobs multi_job_{k}.sh via qsub. \n\n \
Each command in exp_{i} runs args.task_script with a combination of input arguments as hard-coded in this script. Different values of an input argument should be provided as a list and a separate list for each input arg should be provided. e.g. params1, params2 and params3 in the code below.  #Tasks = Cross product of params1, params2 and params3.\n \
Jobs are sorted in the decreasing order of time it takes to run them. \n \
Time of each job is decided by one of the arguments to the task script. 'timing_key' in the code below should be set to the argument name that decides the time. 'timing' list contains the time for each job. \n \
NOTE: you may have to modify the last multi node job manually if total number of tasks to be run is not a multiple of args.num_process_per_job*args.num_task_per_process.  \n\
"

import itertools
import argparse
import sys
import os
from time import sleep
import random
import stat
import copy 

parser = argparse.ArgumentParser(description = description_str)
parser.add_argument('-num_task_per_process',default=1,type=int, help='num tasks to run in parallel in each process', required=True)
parser.add_argument('-num_process_per_job',default=6,type=int, help='num processes to be run in each multinode job', required= True)
parser.add_argument('-task_script',required=True,type=str, help='path to the task script')

parser.add_argument('-template', default='single_run.sh', required=False, type=str)
parser.add_argument('-multi_header', default='multinode_header.sh', required=False, type=str)
parser.add_argument('-multi_template', default='multinode_run.sh', required=False, type=str)
parser.add_argument('-single_job_file',default='all_single_jobs.sh',type=str, required=False)
parser.add_argument('-multi_job_file',default='all_multi_jobs.sh',type=str, required = False)
parser.add_argument('-jobs_dir',default='multinodejobs',type=str,help='directory to be created where all generated files/scripts will reside')
parser.add_argument('-job_name',default='mnj',type=str)
parser.add_argument('-selectos',default=' ',type=str)
parser.add_argument('-global_time',required=True,type=int)

args = parser.parse_args(sys.argv[1:])

#test_file = '/home/cse/phd/csz178057/hpcscratch/nlm/data/nqueens_test_11_5_uniform.pkl'
test_file = '/home/cse/phd/csz178057/hpcscratch/nlm/data/nqueens_test_11_6_uniform.pkl' 
######################
#To be changed as per the input arguments of the task_script ####
# In the demo example, dummy_task_script.py takes three input arguments named input1, input2 and input3. Timing for each job has to be decided by timing_key parameter

#module_load_str = 'module load apps/pythonpackages/3.6.0/pytorch/0.4.1/gpu'
#module_load_str = 'module load apps/anaconda3/4.6.9' 
module_load_str = 'module load apps/anaconda/3' 

train_number = [10]
num_missing = [5]
epochs = [0]
warmup_epochs = [200]
depth = [30]
test_number = [11]
#regime = ['minloss','baseline']
#warmup_data_sampling = [] 

names = ['epochs','warmup-epochs','train-number','num-missing-queens','nlm-depth','test-number-begin','test-number-end']
short_names = ['e','we','trs','nm','d','tesb','tese']
all_params = [epochs,warmup_epochs,train_number,num_missing,depth,test_number,test_number]
assert len(names) == len(short_names)


timing_key = 'nlm-depth'
#timing = [args.global_time]*(len(param1)//2) + [args.global_time//2]*(len(param1)//2)
timing = [args.global_time]*len(depth)
#assert(len(globals()[timing_key]) == len(timing))
assert len(all_params[names.index(timing_key)]) == len(timing),'len of timing should be same as len of timing_key param'

timing_dict = dict(zip(all_params[names.index(timing_key)],timing))
jobs = list(itertools.product(*all_params))

additional_names = ['seed','regime','warmup-data-sampling']
additional_short_names = ['s','rg','wds']
additional_job_list = [
                [42,'min-loss','rs'],
                [42,'min-loss','ambiguous'],
                [42,'min-loss','one-one'],
                [42,'min-loss','two-one'],
                [42,'min-loss','three-one'],
                [42,'min-loss','four-one'],
                [42,'baseline','unique'],
                [42,'baseline','rs'],
                [42,'baseline','ambiguous'],
                [42,'baseline','one-one'],
                [42,'baseline','two-one'],
                [42,'baseline','three-one'],
                ]

names = names + additional_names
short_names = short_names + additional_short_names

assert len(names) == len(short_names)
name_to_short = dict(zip(names,short_names))

all_jobs = list(itertools.product(jobs,additional_job_list))
sorted_names = copy.deepcopy(names)
sorted_names.sort()


################################


time_header ='#PBS -l walltime={}:00:00'
#PBS -q workshop
working_dir = os.path.dirname(os.path.join(os.getenv('PWD'),args.task_script))
working_dir ='/home/cse/phd/csz178057/phd/neural-logic-machines' 
ack_dir = os.path.join(os.getenv('PWD'), args.jobs_dir)

if not os.path.exists(ack_dir):
    os.makedirs(ack_dir)

slurm_cmd = open(args.template).read()+'\n'

pid_closing = 'for pid in ${pids[*]}; do \n \
        wait $pid \n\
done\n'

#hack_str = ". /etc/profile.d/modules.sh"
hack_str = " "
multi_header = open(args.multi_header).read()
multi_header = multi_header.replace('${selectos}',args.selectos)
multi_header = multi_header.replace('${num_nodes}',str(args.num_process_per_job//2))

multi_run_script = open(args.multi_template).read()
multi_run_script = multi_run_script.replace('${exp_dir}',ack_dir)

hpcpy  = 'jac-run'
base_cmd = '{} {} --test-file {} --task nqueens --save-interval 4 --nlm-residual 1 --use-gpu '.format(hpcpy, os.path.join(os.getenv('PWD'),args.task_script),test_file) 

# test mode only
# base_cmd+=' --test-only '

jobs_dict = {}
job_name_to_time = {}
for i, setting in enumerate(all_jobs):
    setting = list(itertools.chain(*setting))
    name_setting = {n: s for n, s in zip(names, setting)}
    log_str = '_'.join(['%s-%s' % (name_to_short[n].replace('_','.'), str(name_setting[n])) for n in sorted_names])
     
    setting_list = ['--%s %s' % (name, str(value)) for name, value in name_setting.items()]
    setting_str = ' '.join(setting_list)
    setting_str += ' --dump-dir models/hpc_exp_c/{}'.format(log_str) 
    # test mode only
    # setting_str += ' --load-checkpoint models/hpc_exp/{}/checkpoints/checkpoint_best.pth'.format(log_str)
    jobs_dict[log_str] = setting_str
    job_name_to_time[log_str] = timing_dict[name_setting[timing_key]]


sorted_job_names = list(job_name_to_time.keys())
sorted_job_names.sort(key=lambda x: job_name_to_time[x], reverse=True)

print('Running %d jobs' % (len(jobs_dict)))

hpcfile = os.path.join(args.jobs_dir, args.single_job_file)
fh = open(hpcfile,'w')
#fhdair = open(os.path.join(args.jobs_dir, args.single_job_file+'_dair.sh'),'w')
mode = stat.S_IROTH | stat.S_IRWXU | stat.S_IXOTH | stat.S_IRGRP | stat.S_IXGRP
log_str_single_job_file  = os.path.join(args.jobs_dir, args.single_job_file+'_logstr.txt')
log_str_file  = open(log_str_single_job_file,'w')
count = 0
jcount = 0
mjcount = 0
fhj = None
#for log_str, setting_str in jobs_dict.items():
for log_str in sorted_job_names:
    setting_str = jobs_dict[log_str]
    bash_cmd = '{} {}'.format(base_cmd, setting_str)
    if count % args.num_task_per_process == 0:
        if fhj is not None:
            print(pid_closing, file = fhexp)
            print('touch {}/JACK_{}'.format(ack_dir,jcount), file = fhexp)
            fhexp.close()
            print('bash {}'.format(os.path.basename(tfname)),file=fhj)
            fhj.close()
            os.chmod(tfname,mode)
            os.chmod(tfname_job,mode)
            print('qsub {}'.format(os.path.basename(tfname_job)), file = fh)
            jcount += 1
        
        if jcount % args.num_process_per_job == 0:
            print("Creating new multi job. count: {},  jcount: {}, mjcount: {}".format(count, jcount, mjcount))
            fhmjname = os.path.join(args.jobs_dir, 'multi_job_'+str(mjcount)+'.sh')
            fhmj = open(fhmjname, 'w')
            header = '#PBS -N {}_mn_{}_{}'.format(args.job_name,mjcount,log_str[:10])
            print(header, file = fhmj)
            print(time_header.format(job_name_to_time[log_str]),file=fhmj)
            print(multi_header,file = fhmj)
            print('count={}'.format(jcount),file = fhmj)
            print(multi_run_script, file = fhmj)
            fhmj.close()
            os.chmod(fhmjname, mode)

            mjcount += 1

        
        tfname = os.path.join(args.jobs_dir,'exp_'+str(jcount)+'.sh')
        tfname_job = os.path.join(args.jobs_dir,'job_'+str(jcount)+'.sh')
        fhj = open(tfname_job,'w')
        fhexp = open(tfname,'w') 
        this_time_header = time_header.format(job_name_to_time[log_str])
        header = '#PBS -N job_{}_{}\n{}\n{}\n'.format(jcount,log_str[:10],this_time_header,slurm_cmd)
        print(header, file = fhj)
        
        print(hack_str, file = fhexp)
        print(module_load_str, file = fhexp)
        print('cd {}'.format(working_dir), file= fhexp)
        print('rm {}/JACK_{}'.format(ack_dir,jcount), file = fhexp)
        print('export PATH="$(pwd)"/third_party/Jacinle/bin:$PATH',file = fhexp)

    #

    print("count: {},  jcount: {}, mjcount: {}".format(count, jcount, mjcount))
    print('{} &'.format(bash_cmd), file =fhexp)
    print("pids[{}]=$!".format(count%args.num_task_per_process),file = fhexp)
    print('{} {}'.format(count, log_str), file = log_str_file)
    count += 1


if fhj is not None:
    print("Closing last job")
    print(pid_closing, file = fhexp)
    print('touch {}/JACK_{}'.format(ack_dir,jcount), file = fhexp)
    fhexp.close()
    print('bash {}'.format(os.path.basename(tfname)),file=fhj)
    fhj.close()
    os.chmod(tfname,mode)
    os.chmod(tfname_job,mode)
    print('qsub {}'.format(os.path.basename(tfname_job)), file = fh)
    #jcount += 1
    if jcount % args.num_process_per_job == 0:
        print("Writing last multi job")
        fhmjname = os.path.join(args.jobs_dir, 'multi_job_'+str(mjcount)+'.sh')
        fhmj = open(fhmjname, 'w')
        header = '#PBS -N {}_mn_{}_{}\n{}\n'.format(args.job_name,mjcount,log_str[:10],slurm_cmd)
        print(header, file = fhmj)
        print(multi_header,file = fhmj)
        print('count={}'.format(jcount),file = fhmj)
        print(multi_run_script, file = fhmj)
        fhmj.close()
        os.chmod(fhmjname, mode)
        mjcount += 1
    

fh.close()
os.chmod(hpcfile,mode)
log_str_file.close()

all_multi_file_name = os.path.join(os.getenv('PWD'),args.jobs_dir, args.multi_job_file)
fh = open(all_multi_file_name,'w')
for i in range(mjcount):
    print('qsub multi_job_{}.sh'.format(i),file=fh)

fh.close()
os.chmod(all_multi_file_name, mode)

print("Finished")
