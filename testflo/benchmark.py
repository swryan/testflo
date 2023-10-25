import sys
import time

class BenchmarkWriter(object):
    """Writes benchmark data to a file for postprocessing.
       Data is written as comma separated values (CSV)
    """

    def __init__(self, stream=sys.stdout):
        self.timestamp = time.time()
        self.stream = stream

    def get_iter(self, input_iter):
        for tests in input_iter:
            first = True
            for result in tests:
                if first:
                    # There will only be multiple results if the test has subTests and
                    # one or more of them failed. CPU time and memory usage stats are
                    # for the test as a whole and all results will have the same stats,
                    # so just use the first one.
                    self._write_data(result)
                    first = False
                yield result

    def _write_data(self, result):
        stream = self.stream
        stream.write('%d,%s,%s,%f,%f,%f,%f,%f\n' % (
            self.timestamp,
            result.spec,
            result.status,
            result.elapsed(),
            result.memory_usage,
            result.load[0],
            result.load[1],
            result.load[2]
        ))
        stream.flush()
