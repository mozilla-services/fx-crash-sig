import unittest

from fx_crash_sig import sample_traces
from fx_crash_sig.symbolicate import Symbolicator


class TestSymbolicator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.symbolicator = Symbolicator()

    def is_valid_symbolication(self, symbolicated):
        self.assertTrue(isinstance(symbolicated, dict))
        self.assertTrue('crashing_thread' in symbolicated)
        self.assertTrue('threads' in symbolicated)

    def test_symbolicate_single(self):
        symbolicated = self.symbolicator.symbolicate(sample_traces.trace1)
        self.is_valid_symbolication(symbolicated)

    def test_symbolicate_single2(self):
        symbolicated = self.symbolicator.symbolicate(sample_traces.trace2)
        self.is_valid_symbolication(symbolicated)

    def test_symbolicate_none(self):
        symbolicated = self.symbolicator.symbolicate(None)
        self.assertEquals(symbolicated, {})

    def test_symbolicate_multi(self):
        symbolicated = self.symbolicator.symbolicate_multi([
            sample_traces.trace1,
            sample_traces.trace2
        ])
        for s in symbolicated:
            self.is_valid_symbolication(s)


if __name__ == '__main__':
    unittest.main()
