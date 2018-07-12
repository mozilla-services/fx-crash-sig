from siggen.generator import SignatureGenerator

from fx_crash_sig.symbolicate import Symbolicator


class CrashProcessor:
    def __init__(self, max_frames=40,
                 api_url='https://symbols.mozilla.org/symbolicate/v5'):
        self.symbolicator = Symbolicator(max_frames, api_url)
        self.sig_generator = SignatureGenerator()

    def get_signature(self, crash_data):
        symbolicated = self.symbolicator.symbolicate(crash_data)
        signature = self.sig_generator.generate(symbolicated)
        return signature

    def symbolicate(self, crash_data):
        return self.symbolicator.symbolicate(crash_data)

    def get_signature_from_symbolicated(self, symbolicated):
        return self.sig_generator.generate(symbolicated)
