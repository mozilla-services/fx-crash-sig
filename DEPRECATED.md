This project is deprecated as of October 8th, 2024.

https://github.com/mozilla-services/fx-crash-sig/issues/111

The fx-crash-sig library was initially created as part of a summer internship
project to look at symbolicating and generating signatures for crash pings. It
evolved past that project in a few spurts as it was getting used in different
ways.

This project has become difficult to maintain. There isn't much of a test
suite. The API isn't conductive to symbolicating crash pings at scale. We don't
have time to improve these issues.

Given that, we're deprecating this library. We won't be maintaining it going forward.

If you use this library, we encourage you to replace fx-crash-sig code with:

1. symbolication calls:
   * https://symbolication.services.mozilla.com/
   * https://mozilla-eliot.readthedocs.io/en/latest/symbolication.html
2. signature generation:
   * use [socorro-siggen](https://github.com/willkg/socorro-siggen/)
   * use Crash Stat's [Crash Signature API](https://crash-stats.mozilla.org/api/#CrashSignature)
