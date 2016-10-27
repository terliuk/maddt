#!/bin/zsh 

#$ -S /bin/zsh
#$ -l h_rss=2000M
#$ -l h_cpu=00:29:59
##$ -cwd
#$ -j y 
#$ -o /lustre/fs19/group/icecube/terliuk/LOGS/copy_md5_jobs/

#$ -P z_nuastr

MADDT=$HOME/scratch/venv/maddt
sha1_storage_path=$1

shift
export LD_LIBRARY_PATH=/opt/products/lib64:$LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH
touch $sha1_storage_path
for i in $*; do zsh -c "$MADDT/bin/md5dcap -t md5 -b 1000000 $i >> $sha1_storage_path"; done
