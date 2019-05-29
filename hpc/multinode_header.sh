#Name of job
#Dep name , project name
#PBS -P mausam.inlp.cs  
#PBS -q high
#PBS -j oe
#PBS -m bea
### Specify email address to use for notification.
#PBS -M $USER@iitd.ac.in
#PBS -l select=3:ngpus=2:ncpus=6
## SPECIFY JOB NOW

CURTIME=$(date +%Y%m%d%H%M%S)
module load apps/pythonpackages/3.6.0/pytorch/0.4.1/gpu
## Change to dir from where script was launched



