from __future__ import with_statement
from __future__ import absolute_import
from subprocess import check_output
import re
import sys
import os
from io import open



def submitJob_local(index, commandExecutable):
    """
    This routine is to submit job locally
    One needs to do a little edit based on your own case.

    Step 1: to prepare the job script which is required by your supercomputer
    Step 2: to submit the job with the command like qsub, bsub, llsubmit, .etc.
    Step 3: to get the jobID from the screen message
    :return: job ID
    """

    RUN_FILENAME = 'myrun'
    JOB_NAME = 'USPEX-{}'.format(index)

    # Step 1
    myrun_content = '''
#!/bin/bash -l
module load compiler/2022.0.1 intel-mpi/2021.5.0 intel-mkl/2022.0.1
export I_MPI_PMI_LIBRARY=/opt/sw/slurm/x86_64/alma8.5/22-05-2-1/lib/libpmi.so
export LANG=C
export LC_ALL=C
export LANG=C
export LC_ALL=C
export SLURM_STEP_GRES=none
echo "I will now run qe!" > script_report
    '''
    myrun_content += commandExecutable 
    myrun_content += "  \n"
    myrun_content += "wait \n"
    myrun_content += "exit \n"

    with open(RUN_FILENAME, 'w') as fp:
        fp.write(myrun_content)
    os.system("while [ ! -f ./myrun ]; do sleep 0.2; done; chmod +x myrun")
    # Step 2
    # It will output some message on the screen like '2350873.nano.cfn.bnl.local'
    output = check_output('screen -S ' + JOB_NAME + ' -p 0 -dm bash -lc \'echo "$STY" > jobID; ./myrun ; \'', shell=True, universal_newlines=True)
    os.system("while [ ! -f ./jobID ]; do sleep 0.2; done")
    # Step 3
    # Here we parse job ID from the output of previous command
    with open("jobID", "r") as output:
        line = (output.readline()).strip()
        line = line.replace("USPEX-","")
        with open("../log_jobid", "a") as logfile:
            logfile.write(line + "    " + str(line.split('.')[0]) + "   " + str(line.split('.')[1]) + "   \n")
        jobNumber = int(line.split('.')[0])
    os.remove("./jobID")
    print(str(jobNumber))
    return jobNumber


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='index', type=int)
    parser.add_argument('-c', dest='commandExecutable', type=str)
    args = parser.parse_args()

    jobNumber = submitJob_local(index=args.index, commandExecutable=args.commandExecutable)
    print('<CALLRESULT>')
    print(int(jobNumber))
