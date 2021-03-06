
"""
This is meant to be executed using mpirun.  It is called as a subprocess
to run an MPI test.

"""

if __name__ == '__main__':
    import sys
    import os
    import traceback

    from mpi4py import MPI
    from testflo.test import Test
    from testflo.cover import save_coverage
    from testflo.qman import get_client_manager
    from testflo.util import get_addr_auth_from_args

    exitcode = 0  # use 0 for exit code of all ranks != 0 because otherwise,
                  # MPI will terminate other processes

    address, authkey = get_addr_auth_from_args(sys.argv[2:])

    manager = get_client_manager(address, authkey)

    try:
        try:
            comm = MPI.COMM_WORLD
            test = Test(sys.argv[1])
            test.nocapture = True # so we don't lose stdout
            test.run()
        except:
            print(traceback.format_exc())
            test.status = 'FAIL'
            test.err_msg = traceback.format_exc()

        # collect results
        results = comm.gather(test, root=0)
        if comm.rank == 0:
            total_mem_usage = sum(r.memory_usage for r in results)
            test.memory_usage = total_mem_usage

            # check for errors and record error message
            for r in results:
                if test.status != 'FAIL' and r.status in ('SKIP', 'FAIL'):
                    test.err_msg = r.err_msg
                    test.status = r.status
                    if r.status == 'FAIL':
                        break

        save_coverage()

    except Exception:
        test.err_msg = traceback.format_exc()
        test.status = 'FAIL'

    finally:
        sys.stdout.flush()
        sys.stderr.flush()

        if comm.rank == 0:
            manager.get_queue().put(test)
