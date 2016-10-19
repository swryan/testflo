#!/bin/bash
#
# usage: qsubrun -n # python script testspec host port key
#

#
# process args
#
procs=$2
cmd=${@:3}
testspec=$5

if [ $procs -eq 0 ]; then
  procs=1
fi

#
# build job name from testspec
#
name=${testspec##*\.}
jobfile="$name-$BASHPID.job"

#
# build job script
#
echo "#!/bin/bash"         >$jobfile
echo "#$ -N $name"        >>$jobfile
echo "#$ -cwd"            >>$jobfile
echo "#$ -S /bin/bash"    >>$jobfile
echo "#$ -V"              >>$jobfile
if (( $procs > 1 )) ; then
    echo "#$ -pe ompi $procs" >>$jobfile
    echo "mpirun -n \$NSLOTS $cmd" >>$jobfile
else
    echo "$cmd" >>$jobfile
fi
  
cat $jobfile

#
# calculate required nodes, procs to allocate & queues
#
procs_per_node=20
nodes=$(($procs/$procs_per_node))
alloc_procs=$(($nodes * $procs_per_node))

if [ $alloc_procs -lt $procs ]; then
  nodes=$(($nodes + 1))
  alloc_procs=$(($nodes * $procs_per_node))
fi

queues="-q "
qprefix="mdao.q@mdao"
for i in $(seq 1 $nodes); do
  queues="$queues$qprefix$i"
  if [ $i -ne $nodes ]; then
    queues="$queues,"
  fi
done

#
# submit job using qsub
#

echo job requires $procs CPU\(s\), allocating $nodes node\(s\) with $alloc_procs CPUs
echo qsub command: qsub -pe ompi $alloc_procs $queues $jobfile
qsub -pe ompi $alloc_procs $queues $jobfile

#
# clean up
#
#rm -f $jobfile
