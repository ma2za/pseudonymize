window.BENCHMARK_DATA = {
  "lastUpdate": 1789710334241,
  "repoUrl": "https://github.com/ma2za/pseudonymize",
  "entries": {
    "Python Benchmark with pytest-benchmark": [
      {
        "commit": {
          "author": {
            "email": "mazzapaolo2019@gmail.com",
            "name": "Paolo Mazza",
            "username": "ma2za"
          },
          "committer": {
            "email": "mazzapaolo2019@gmail.com",
            "name": "Paolo Mazza",
            "username": "ma2za"
          },
          "distinct": true,
          "id": "4bc8b67627949d5ce9a80c024bc82f0c9e7be266",
          "message": "ci(benchmark): disable coverage checking for benchmark suite runs to prevent pipeline failure",
          "timestamp": "2026-09-18T07:39:28+02:00",
          "tree_id": "17a7df14cac5e54abea34a7b856236abfe647188",
          "url": "https://github.com/ma2za/pseudonymize/commit/4bc8b67627949d5ce9a80c024bc82f0c9e7be266"
        },
        "date": 1789710333798,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 610.228418831041,
            "unit": "iter/sec",
            "range": "stddev: 0.000020196832409145062",
            "extra": "mean: 1.6387306279763385 msec\nrounds: 336"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 607.6953906854794,
            "unit": "iter/sec",
            "range": "stddev: 0.00008857477512978643",
            "extra": "mean: 1.6455612718602353 msec\nrounds: 629"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 376.0192677913037,
            "unit": "iter/sec",
            "range": "stddev: 0.00011882739141613059",
            "extra": "mean: 2.659438187500048 msec\nrounds: 384"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 504.2205822851424,
            "unit": "iter/sec",
            "range": "stddev: 0.0001724900511776891",
            "extra": "mean: 1.983258984526119 msec\nrounds: 517"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 426.45885244539556,
            "unit": "iter/sec",
            "range": "stddev: 0.00036962475866354576",
            "extra": "mean: 2.3448921138951886 msec\nrounds: 439"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 312.867306096268,
            "unit": "iter/sec",
            "range": "stddev: 0.0003789099276301713",
            "extra": "mean: 3.1962432012384956 msec\nrounds: 323"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 76.36342384903293,
            "unit": "iter/sec",
            "range": "stddev: 0.000130371432014819",
            "extra": "mean: 13.095274538461702 msec\nrounds: 78"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 141.38784409122857,
            "unit": "iter/sec",
            "range": "stddev: 0.00003562241095774567",
            "extra": "mean: 7.072743816326697 msec\nrounds: 147"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 503.9037691483978,
            "unit": "iter/sec",
            "range": "stddev: 0.00024727936108238696",
            "extra": "mean: 1.9845058942305782 msec\nrounds: 520"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1835.6535083039498,
            "unit": "iter/sec",
            "range": "stddev: 0.000010659704213145507",
            "extra": "mean: 544.765117968232 usec\nrounds: 1831"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 184.90607618734813,
            "unit": "iter/sec",
            "range": "stddev: 0.000053756559044626237",
            "extra": "mean: 5.408151103627298 msec\nrounds: 193"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 80.68400030498135,
            "unit": "iter/sec",
            "range": "stddev: 0.00023943551626749092",
            "extra": "mean: 12.394030987804912 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 926.2271115868457,
            "unit": "iter/sec",
            "range": "stddev: 0.000016422116239399226",
            "extra": "mean: 1.0796488112799505 msec\nrounds: 922"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1161.2432198388221,
            "unit": "iter/sec",
            "range": "stddev: 0.00005885679366626724",
            "extra": "mean: 861.1460397924197 usec\nrounds: 1156"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 129.36379471832322,
            "unit": "iter/sec",
            "range": "stddev: 0.00004882225445592391",
            "extra": "mean: 7.730138113043147 msec\nrounds: 115"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.304750274526013,
            "unit": "iter/sec",
            "range": "stddev: 0.0021466318446796803",
            "extra": "mean: 120.41301266666613 msec\nrounds: 9"
          }
        ]
      }
    ]
  }
}