window.BENCHMARK_DATA = {
  "lastUpdate": 1789711100453,
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
      },
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
          "id": "0012f5cde98d4a7b66c4264ca7458cff4d0fb296",
          "message": "chore: clean comments in ignore file",
          "timestamp": "2026-09-18T07:50:53+02:00",
          "tree_id": "c9148cc49669703acf47351f6a499eb7a7a4ad4a",
          "url": "https://github.com/ma2za/pseudonymize/commit/0012f5cde98d4a7b66c4264ca7458cff4d0fb296"
        },
        "date": 1789711100003,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 608.4435033747257,
            "unit": "iter/sec",
            "range": "stddev: 0.000020155970883113043",
            "extra": "mean: 1.6435379693488554 msec\nrounds: 522"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 630.0871150316929,
            "unit": "iter/sec",
            "range": "stddev: 0.000020698343150612293",
            "extra": "mean: 1.587082129031794 msec\nrounds: 620"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 355.5036302334333,
            "unit": "iter/sec",
            "range": "stddev: 0.00020784864676440227",
            "extra": "mean: 2.8129107974041583 msec\nrounds: 385"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 511.10888139430983,
            "unit": "iter/sec",
            "range": "stddev: 0.00004852640141776427",
            "extra": "mean: 1.9565302744730058 msec\nrounds: 521"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 431.34572627283916,
            "unit": "iter/sec",
            "range": "stddev: 0.00003281352747383657",
            "extra": "mean: 2.3183259716997173 msec\nrounds: 424"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 311.7713460402077,
            "unit": "iter/sec",
            "range": "stddev: 0.00005910038706015804",
            "extra": "mean: 3.207478854939526 msec\nrounds: 324"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 78.23443848876958,
            "unit": "iter/sec",
            "range": "stddev: 0.00020075344045027542",
            "extra": "mean: 12.782094679998863 msec\nrounds: 75"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 141.27297566723416,
            "unit": "iter/sec",
            "range": "stddev: 0.00004158811894853347",
            "extra": "mean: 7.078494632657 msec\nrounds: 147"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 518.1464145424227,
            "unit": "iter/sec",
            "range": "stddev: 0.000044696515359320174",
            "extra": "mean: 1.9299564214549363 msec\nrounds: 522"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1791.767360387636,
            "unit": "iter/sec",
            "range": "stddev: 0.00007230732527117658",
            "extra": "mean: 558.1081685647276 usec\nrounds: 1756"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 188.04750041869025,
            "unit": "iter/sec",
            "range": "stddev: 0.0000674555779737667",
            "extra": "mean: 5.317805329895302 msec\nrounds: 194"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 79.5673795445071,
            "unit": "iter/sec",
            "range": "stddev: 0.00008992019618200142",
            "extra": "mean: 12.567964481482468 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 879.1765093900317,
            "unit": "iter/sec",
            "range": "stddev: 0.000040927313338195935",
            "extra": "mean: 1.137428024201642 msec\nrounds: 909"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1174.0213259737973,
            "unit": "iter/sec",
            "range": "stddev: 0.00004697954804791342",
            "extra": "mean: 851.7732837353235 usec\nrounds: 1156"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 129.50306072045828,
            "unit": "iter/sec",
            "range": "stddev: 0.00006897768087012059",
            "extra": "mean: 7.721825217386733 msec\nrounds: 115"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.31994437810255,
            "unit": "iter/sec",
            "range": "stddev: 0.0006853542442339004",
            "extra": "mean: 120.19311122222437 msec\nrounds: 9"
          }
        ]
      }
    ]
  }
}