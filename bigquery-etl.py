import math
import sys
from google.cloud import bigquery
from fx_crash_sig.crash_processor import CrashProcessor
from multiprocessing.dummy import Pool as ThreadPool

QUERY_TEMPLATE = """
SELECT
  document_id, payload
FROM
  `moz-fx-data-shared-prod`.telemetry.crash
WHERE
  normalized_channel="nightly"
  AND DATE(submission_timestamp)="{date}"
  AND application.build_id > FORMAT_DATE("%Y%m%d", DATE_SUB(DATE "{date}", INTERVAL 1 WEEK))
  AND payload IS NOT NULL
  AND payload.stack_traces IS NOT NULL
  AND payload.stack_traces.crash_info IS NOT NULL
"""

if len(sys.argv) != 2:
    print("USAGE: %s <date in YYYY-MM-DD format>" % sys.argv[0])
    sys.exit(1)

proc = CrashProcessor(verbose=True,windows=True)

client = bigquery.Client()
query_job = client.query(QUERY_TEMPLATE.format(date=sys.argv[1]))
result = query_job.result()

CHUNK_SIZE = 10
chunk_count = math.ceil(result.total_rows / CHUNK_SIZE)
print(f"Rows: {result.total_rows}, Chunks: {chunk_count}", file=sys.stderr)

def get_sigs(chunk):
    (doc_ids, payloads) = chunk
    sigs = proc.get_signatures_multi(doc_ids, payloads)
    return (doc_ids, sigs)

class GeneratorLen(object):
    """
    Helper wrapper around a generator whose length we know, to pass to pool.map.
    If we don't use this pool.map will turn the generator into a list which
    basically reads all the result data from BigQuery in one go, which is heavy
    on memory.
    """
    def __init__(self, gen, length):
        self.gen = gen
        self.length = length

    def __len__(self):
        return self.length

    def __iter__(self):
        return self.gen

    @staticmethod
    def get_chunks(result):
        """
        Generator that yields a tuple of two arrays. The first array holds document
        IDs, the second array holds the corresponding payloads. The length of the
        two arrays are always the same.
        """
        doc_ids = []
        payloads = []
        # there's probably a more pythonic way to do this...
        for (document_id, payload) in result:
            doc_ids.append(document_id)
            payloads.append(payload)
            if len(doc_ids) < CHUNK_SIZE:
                continue
            yield (doc_ids, payloads)
            doc_ids = []
            payloads = []
        if len(doc_ids) > 0:
            yield (doc_ids, payloads)


pool = ThreadPool(10)
chunks = GeneratorLen(GeneratorLen.get_chunks(result), chunk_count)
all_sigs = pool.map(get_sigs, chunks)

for (chunk_doc_ids, chunk_sigs) in all_sigs:
    for (doc_id, sig) in zip(chunk_doc_ids, chunk_sigs):
        if sig is None or len(sig.signature) == 0:
            print(f"Error computing signature for {doc_id}", file=sys.stderr)
            continue
        print(f'{doc_id},"{sig.signature}"')
