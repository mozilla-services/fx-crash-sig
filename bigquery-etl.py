import sys
from google.cloud import bigquery
from fx_crash_sig.crash_processor import CrashProcessor

QUERY_TEMPLATE = """
SELECT
  document_id, payload
FROM
  `moz-fx-data-shared-prod`.telemetry.crash
WHERE
  normalized_channel="nightly"
  AND DATE(submission_timestamp)="{date}"
  AND application.build_id > FORMAT_DATE("%Y%m%d", DATE_SUB(DATE "{date}", INTERVAL 1 WEEK))
"""

if len(sys.argv) != 2:
    print("USAGE: %s <date in YYYY-MM-DD format>" % sys.argv[0])
    sys.exit(1)

proc = CrashProcessor(windows=True)

client = bigquery.Client()
query_job = client.query(QUERY_TEMPLATE.format(date=sys.argv[1]))
result = query_job.result()
for (document_id, payload) in result:
    if payload:
        symbolicated = proc.symbolicate(payload)
        sig = proc.get_signature_from_symbolicated(symbolicated).signature
        print(f"{document_id},{sig}")