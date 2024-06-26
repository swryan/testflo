
"""
This is meant to be executed using mpirun.  It is called as a subprocess
to run an MPI test.

"""

if __name__ == '__main__':
    try:
        import coverage
    except ImportError:
        pass
    else:
        coverage.process_startup()

    import sys
    import os
    import traceback

    # when testing OpenMDAO, make sure that MPI is active
    os.environ['OPENMDAO_USE_MPI'] = '1'

    from mpi4py import MPI
    from testflo.test import Test
    from testflo.qman import get_client_queue
    from testflo.options import get_options

    exitcode = 0  # use 0 for exit code of all ranks != 0 because otherwise,
                  # MPI will terminate other processes

    queue = get_client_queue()
    os.environ['TESTFLO_QUEUE'] = ''

    options = get_options()

    try:
        try:
            comm = MPI.COMM_WORLD
            test = Test(sys.argv[1], options)
            test.nocapture = True # so we don't lose stdout
            test.run()
        except:
            print(traceback.format_exc())
            test.status = 'FAIL'
            test.err_msg = traceback.format_exc()
        else:
            # collect results
            results = comm.gather(test, root=0)
            if comm.rank == 0:
                if not all([isinstance(r, Test) for r in results]):
                    print("\nNot all results gathered are Test objects.  "
                          "You may have out-of-sync collective MPI calls.\n")
                total_mem_usage = sum(r.memory_usage for r in results if isinstance(r, Test))
                test.memory_usage = total_mem_usage

                # check for errors and record error message
                for r in results:
                    if test.status != 'FAIL' and r.status in ('SKIP', 'FAIL'):
                        test.err_msg = r.err_msg
                        test.status = r.status
                        if r.status == 'FAIL':
                            break

    except Exception:
        test.err_msg = traceback.format_exc()
        test.status = 'FAIL'

    finally:
        sys.stdout.flush()
        sys.stderr.flush()

        if comm.rank == 0:
            queue.put(test)
