
import sys
import time

from testflo.util import elapsed_str

class ResultSummary(object):
    """Writes a test summary after all tests are run."""

    def __init__(self, options, stream=sys.stdout):
        self.stream = stream
        self.options = options
        self._start_time = time.time()

    def get_iter(self, input_iter):
        oks = 0
        total = 0
        fails = []
        skips = []
        test_sum_time = 0.

        write = self.stream.write

        for test in input_iter:
            total += 1

            if test.status == 'OK':
                oks += 1
                test_sum_time += (test.end_time-test.start_time)
            elif test.status == 'FAIL':
                fails.append(test.short_name())
                test_sum_time += (test.end_time-test.start_time)
            elif test.status == 'SKIP':
                skips.append(test.short_name())
            yield test

        # now summarize the run
        if skips:
            write("\n\nThe following tests were skipped:\n")
            for s in sorted(skips):
                write(s)
                write('\n')

        if fails:
            write("\n\nThe following tests failed:\n")
            for f in sorted(fails):
                write(f)
                write('\n')
        else:
            write("\n\nOK")

        write("\n\nPassed:  %d\nFailed:  %d\nSkipped: %d\n" %
                            (oks, len(fails), len(skips)))

        wallclock = time.time() - self._start_time

        s = "" if total == 1 else "s"
        if self.options.isolated:
            procstr = " in isolated processes"
        else:
            procstr = " using %d processes" % self.options.num_procs
        write("\n\nRan %d test%s%s\nSum of test times: %s\n"
              "Wall clock time:   %s\nSpeedup: %f\n\n" %
                      (total, s, procstr,
                       elapsed_str(test_sum_time), elapsed_str(wallclock),
                       test_sum_time/wallclock))
