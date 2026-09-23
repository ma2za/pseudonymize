window.BENCHMARK_DATA = {
  "lastUpdate": 1790141757109,
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
          "id": "2ec8c08862646c4c0f03f226d90cac3ff684be0e",
          "message": "chore(release): bump development version to 1.22.0 and prepare ROADMAP.md/CHANGELOG.md",
          "timestamp": "2026-09-18T08:10:02+02:00",
          "tree_id": "b37060ac4eb9eda29a8dd50a2574e91f17dbf1e9",
          "url": "https://github.com/ma2za/pseudonymize/commit/2ec8c08862646c4c0f03f226d90cac3ff684be0e"
        },
        "date": 1789711834468,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 607.2160792189369,
            "unit": "iter/sec",
            "range": "stddev: 0.00002122845616187514",
            "extra": "mean: 1.6468602104316832 msec\nrounds: 556"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 619.6172976021331,
            "unit": "iter/sec",
            "range": "stddev: 0.00014962915315208964",
            "extra": "mean: 1.613899424483332 msec\nrounds: 629"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 384.54559616309524,
            "unit": "iter/sec",
            "range": "stddev: 0.00002392534847727375",
            "extra": "mean: 2.600471855555655 msec\nrounds: 270"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 523.0915877016375,
            "unit": "iter/sec",
            "range": "stddev: 0.000026394078684531494",
            "extra": "mean: 1.9117111104650046 msec\nrounds: 516"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 418.6678119893656,
            "unit": "iter/sec",
            "range": "stddev: 0.0002941872199829278",
            "extra": "mean: 2.3885284976849395 msec\nrounds: 432"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 308.06515770196853,
            "unit": "iter/sec",
            "range": "stddev: 0.00021437891088015064",
            "extra": "mean: 3.246066538194592 msec\nrounds: 288"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 78.85681294051399,
            "unit": "iter/sec",
            "range": "stddev: 0.00010433561675268612",
            "extra": "mean: 12.681212475000159 msec\nrounds: 80"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 141.8064453836758,
            "unit": "iter/sec",
            "range": "stddev: 0.000755472195342865",
            "extra": "mean: 7.0518656418921575 msec\nrounds: 148"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 534.3862791682162,
            "unit": "iter/sec",
            "range": "stddev: 0.00004243402584969183",
            "extra": "mean: 1.871305531190886 msec\nrounds: 529"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1825.291102065322,
            "unit": "iter/sec",
            "range": "stddev: 0.00003995158108415566",
            "extra": "mean: 547.8578177850629 usec\nrounds: 1833"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 188.23674485333618,
            "unit": "iter/sec",
            "range": "stddev: 0.00003089544126055472",
            "extra": "mean: 5.312459056700887 msec\nrounds: 194"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 80.84640491200959,
            "unit": "iter/sec",
            "range": "stddev: 0.00015764428215032513",
            "extra": "mean: 12.369133804878093 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 911.2687389567694,
            "unit": "iter/sec",
            "range": "stddev: 0.00004049886677364656",
            "extra": "mean: 1.097371123632323 msec\nrounds: 914"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1177.2874075007715,
            "unit": "iter/sec",
            "range": "stddev: 0.000013050089746438426",
            "extra": "mean: 849.4102575367475 usec\nrounds: 1161"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 129.31735927646454,
            "unit": "iter/sec",
            "range": "stddev: 0.00005984418622478104",
            "extra": "mean: 7.732913860869394 msec\nrounds: 115"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.332977800662956,
            "unit": "iter/sec",
            "range": "stddev: 0.0006805690771278723",
            "extra": "mean: 120.00511988888798 msec\nrounds: 9"
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
          "id": "9ff20595ea6ab1fc78bd0c0dcb6fc1e45ab40be6",
          "message": "feat(ml): implement EnsembleMode (union/intersection) for CompositeBackend with high-precision metrics confirmation",
          "timestamp": "2026-09-18T08:50:47+02:00",
          "tree_id": "57ea004f6d6f976c9bb811d5b30ac3faae444dd9",
          "url": "https://github.com/ma2za/pseudonymize/commit/9ff20595ea6ab1fc78bd0c0dcb6fc1e45ab40be6"
        },
        "date": 1789714279287,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 604.3032425874021,
            "unit": "iter/sec",
            "range": "stddev: 0.000047285820470823056",
            "extra": "mean: 1.6547983355481783 msec\nrounds: 301"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 630.8292819461751,
            "unit": "iter/sec",
            "range": "stddev: 0.00006933094462316353",
            "extra": "mean: 1.5852149363055787 msec\nrounds: 628"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 362.15249089241655,
            "unit": "iter/sec",
            "range": "stddev: 0.00010568174995809134",
            "extra": "mean: 2.761267767441828 msec\nrounds: 387"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 523.6927111372258,
            "unit": "iter/sec",
            "range": "stddev: 0.00003255200905707682",
            "extra": "mean: 1.9095167428021833 msec\nrounds: 521"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 401.8855568252337,
            "unit": "iter/sec",
            "range": "stddev: 0.0003547064920394391",
            "extra": "mean: 2.488270561150984 msec\nrounds: 417"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 301.3312198388488,
            "unit": "iter/sec",
            "range": "stddev: 0.00038881882583653786",
            "extra": "mean: 3.318607346874969 msec\nrounds: 320"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 79.30656423741304,
            "unit": "iter/sec",
            "range": "stddev: 0.0002425947888820274",
            "extra": "mean: 12.609296716049741 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 142.06610970774582,
            "unit": "iter/sec",
            "range": "stddev: 0.00015998730864192427",
            "extra": "mean: 7.038976445945977 msec\nrounds: 148"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 527.0075166331765,
            "unit": "iter/sec",
            "range": "stddev: 0.000032149477130525024",
            "extra": "mean: 1.897506142585154 msec\nrounds: 526"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1836.0477358773835,
            "unit": "iter/sec",
            "range": "stddev: 0.000007255595130648249",
            "extra": "mean: 544.6481485527034 usec\nrounds: 1831"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 187.90175870610452,
            "unit": "iter/sec",
            "range": "stddev: 0.000058239962997822675",
            "extra": "mean: 5.321929964285705 msec\nrounds: 196"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 79.6638258054176,
            "unit": "iter/sec",
            "range": "stddev: 0.0001509918716253865",
            "extra": "mean: 12.552748878048412 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 809.947626455811,
            "unit": "iter/sec",
            "range": "stddev: 0.0002138869719974827",
            "extra": "mean: 1.2346477319475888 msec\nrounds: 914"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1138.5335545018963,
            "unit": "iter/sec",
            "range": "stddev: 0.00004386853667266927",
            "extra": "mean: 878.3228180196198 usec\nrounds: 1121"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 129.15531171969562,
            "unit": "iter/sec",
            "range": "stddev: 0.000048574587824989",
            "extra": "mean: 7.742616131578772 msec\nrounds: 114"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.347751655015193,
            "unit": "iter/sec",
            "range": "stddev: 0.0018647392942015158",
            "extra": "mean: 119.7927347777789 msec\nrounds: 9"
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
          "id": "6e1126fac5f60354ed58737faf7ca2e90c9e901b",
          "message": "Revert \"feat(ml): implement EnsembleMode (union/intersection) for CompositeBackend with high-precision metrics confirmation\"\n\nThis reverts commit 9ff20595ea6ab1fc78bd0c0dcb6fc1e45ab40be6.",
          "timestamp": "2026-09-18T08:56:55+02:00",
          "tree_id": "b37060ac4eb9eda29a8dd50a2574e91f17dbf1e9",
          "url": "https://github.com/ma2za/pseudonymize/commit/6e1126fac5f60354ed58737faf7ca2e90c9e901b"
        },
        "date": 1789714650140,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 752.4732235950635,
            "unit": "iter/sec",
            "range": "stddev: 0.000039688184341010674",
            "extra": "mean: 1.3289509428951332 msec\nrounds: 753"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 759.7931904513863,
            "unit": "iter/sec",
            "range": "stddev: 0.00005212577833015587",
            "extra": "mean: 1.3161476209149874 msec\nrounds: 765"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 541.1928426337272,
            "unit": "iter/sec",
            "range": "stddev: 0.00008934850950028403",
            "extra": "mean: 1.8477701869327712 msec\nrounds: 551"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 710.6414416452375,
            "unit": "iter/sec",
            "range": "stddev: 0.00006731449408842143",
            "extra": "mean: 1.4071794035608953 msec\nrounds: 674"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 654.3228491860971,
            "unit": "iter/sec",
            "range": "stddev: 0.00004496189905064147",
            "extra": "mean: 1.5282975388126607 msec\nrounds: 657"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 467.51486163844015,
            "unit": "iter/sec",
            "range": "stddev: 0.00006011230768798548",
            "extra": "mean: 2.138969436170278 msec\nrounds: 470"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 108.87943779852635,
            "unit": "iter/sec",
            "range": "stddev: 0.0006117100360028758",
            "extra": "mean: 9.184470642201779 msec\nrounds: 109"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 196.298329220744,
            "unit": "iter/sec",
            "range": "stddev: 0.00017554176862205392",
            "extra": "mean: 5.094286864130498 msec\nrounds: 184"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 664.962971233832,
            "unit": "iter/sec",
            "range": "stddev: 0.00011991876039578796",
            "extra": "mean: 1.5038431360238151 msec\nrounds: 669"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 2437.381194769499,
            "unit": "iter/sec",
            "range": "stddev: 0.000034970423918259015",
            "extra": "mean: 410.2764073777016 usec\nrounds: 2494"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 265.21841293266147,
            "unit": "iter/sec",
            "range": "stddev: 0.00015019074269173444",
            "extra": "mean: 3.770477279244931 msec\nrounds: 265"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 106.86323599571381,
            "unit": "iter/sec",
            "range": "stddev: 0.0002906016178604449",
            "extra": "mean: 9.357755178217783 msec\nrounds: 101"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1130.8538410927695,
            "unit": "iter/sec",
            "range": "stddev: 0.000031386055219542854",
            "extra": "mean: 884.2875742754497 usec\nrounds: 1104"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1497.4568486277615,
            "unit": "iter/sec",
            "range": "stddev: 0.00001830235170522096",
            "extra": "mean: 667.7988757514978 usec\nrounds: 1497"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 173.57613721025146,
            "unit": "iter/sec",
            "range": "stddev: 0.0001755575367261835",
            "extra": "mean: 5.761160583892402 msec\nrounds: 149"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 11.173477693961145,
            "unit": "iter/sec",
            "range": "stddev: 0.005178716081264887",
            "extra": "mean: 89.49765036363418 msec\nrounds: 11"
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
          "id": "1769522f8478525c9f84bb2a550c54bdf6a9ca4e",
          "message": "feat(mcp): implement Schema-Preserving Agent de-identification to prevent breaking LLM schemas",
          "timestamp": "2026-09-18T09:50:01+02:00",
          "tree_id": "5743c9b31b802cf22eeaa463825370204697a6b7",
          "url": "https://github.com/ma2za/pseudonymize/commit/1769522f8478525c9f84bb2a550c54bdf6a9ca4e"
        },
        "date": 1789717833715,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 610.4984588895277,
            "unit": "iter/sec",
            "range": "stddev: 0.00001830435877423036",
            "extra": "mean: 1.6380057728875517 msec\nrounds: 568"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 638.9504544836011,
            "unit": "iter/sec",
            "range": "stddev: 0.000017258609324440726",
            "extra": "mean: 1.5650665759494586 msec\nrounds: 632"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 374.52335407096996,
            "unit": "iter/sec",
            "range": "stddev: 0.0001258646400922714",
            "extra": "mean: 2.670060462532614 msec\nrounds: 387"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 514.4079496843918,
            "unit": "iter/sec",
            "range": "stddev: 0.000023861509920806213",
            "extra": "mean: 1.9439823988208904 msec\nrounds: 509"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 433.0122990864691,
            "unit": "iter/sec",
            "range": "stddev: 0.00003099254586419099",
            "extra": "mean: 2.309403225057836 msec\nrounds: 431"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 301.6638255301903,
            "unit": "iter/sec",
            "range": "stddev: 0.00011564944035691086",
            "extra": "mean: 3.314948347692822 msec\nrounds: 325"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 76.97315331819847,
            "unit": "iter/sec",
            "range": "stddev: 0.0001433505681976568",
            "extra": "mean: 12.991542594937107 msec\nrounds: 79"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 141.48898439101026,
            "unit": "iter/sec",
            "range": "stddev: 0.00041779295207036493",
            "extra": "mean: 7.067688020407733 msec\nrounds: 147"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 505.10608734776866,
            "unit": "iter/sec",
            "range": "stddev: 0.000023675289475494305",
            "extra": "mean: 1.9797821191402387 msec\nrounds: 512"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1820.5028495783176,
            "unit": "iter/sec",
            "range": "stddev: 0.00003907131896421242",
            "extra": "mean: 549.2987831530336 usec\nrounds: 1757"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 183.11200179806576,
            "unit": "iter/sec",
            "range": "stddev: 0.00005434423316350581",
            "extra": "mean: 5.461138484536862 msec\nrounds: 194"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 80.96694566097946,
            "unit": "iter/sec",
            "range": "stddev: 0.00026607142645317507",
            "extra": "mean: 12.35071907228843 msec\nrounds: 83"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 920.9852294513556,
            "unit": "iter/sec",
            "range": "stddev: 0.00001463770125893345",
            "extra": "mean: 1.0857937435063043 msec\nrounds: 924"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1174.9123005399913,
            "unit": "iter/sec",
            "range": "stddev: 0.000027390287262656252",
            "extra": "mean: 851.1273560932153 usec\nrounds: 1157"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 130.14980909620715,
            "unit": "iter/sec",
            "range": "stddev: 0.00007341736027217813",
            "extra": "mean: 7.683453452173694 msec\nrounds: 115"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.248294773658213,
            "unit": "iter/sec",
            "range": "stddev: 0.0032076682010255546",
            "extra": "mean: 121.23718022222046 msec\nrounds: 9"
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
          "id": "226744d6559b03173359053fd9a27477c593af05",
          "message": "chore(release): bump development version to 1.23.0 and prepare CHANGELOG.md",
          "timestamp": "2026-09-18T10:38:56+02:00",
          "tree_id": "28369d7c70b538fa8c597bfe3c1967f12c043221",
          "url": "https://github.com/ma2za/pseudonymize/commit/226744d6559b03173359053fd9a27477c593af05"
        },
        "date": 1789720782484,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 595.3148868451975,
            "unit": "iter/sec",
            "range": "stddev: 0.00017474009348962432",
            "extra": "mean: 1.679783291325679 msec\nrounds: 611"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 628.7692414730913,
            "unit": "iter/sec",
            "range": "stddev: 0.000028287269343875435",
            "extra": "mean: 1.5904085855999939 msec\nrounds: 625"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 364.1389446905345,
            "unit": "iter/sec",
            "range": "stddev: 0.0005129461744884022",
            "extra": "mean: 2.7462044765628004 msec\nrounds: 384"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 497.96756727337555,
            "unit": "iter/sec",
            "range": "stddev: 0.00029521896352240084",
            "extra": "mean: 2.00816291204567 msec\nrounds: 523"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 431.5272643335007,
            "unit": "iter/sec",
            "range": "stddev: 0.00016635820014893673",
            "extra": "mean: 2.3173506812935973 msec\nrounds: 433"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 307.4952931343342,
            "unit": "iter/sec",
            "range": "stddev: 0.00013392778670641425",
            "extra": "mean: 3.2520822995594085 msec\nrounds: 227"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 78.44646651366449,
            "unit": "iter/sec",
            "range": "stddev: 0.0001552334652323869",
            "extra": "mean: 12.747546759493767 msec\nrounds: 79"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 141.9054779716669,
            "unit": "iter/sec",
            "range": "stddev: 0.00010975777199897229",
            "extra": "mean: 7.046944306122289 msec\nrounds: 147"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 524.2220484197657,
            "unit": "iter/sec",
            "range": "stddev: 0.00007333823256212572",
            "extra": "mean: 1.9075885934489727 msec\nrounds: 519"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1811.1390335524775,
            "unit": "iter/sec",
            "range": "stddev: 0.00004196755031837544",
            "extra": "mean: 552.138726776011 usec\nrounds: 1830"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 187.18551375799706,
            "unit": "iter/sec",
            "range": "stddev: 0.00006808534731282167",
            "extra": "mean: 5.342293748718455 msec\nrounds: 195"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 80.35219805064257,
            "unit": "iter/sec",
            "range": "stddev: 0.00015198716537289162",
            "extra": "mean: 12.445210265060112 msec\nrounds: 83"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 912.7562373679793,
            "unit": "iter/sec",
            "range": "stddev: 0.00002007033308542694",
            "extra": "mean: 1.095582762472921 msec\nrounds: 922"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1172.1445385375646,
            "unit": "iter/sec",
            "range": "stddev: 0.00004692959791220054",
            "extra": "mean: 853.1371064934176 usec\nrounds: 1155"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 128.80407152177796,
            "unit": "iter/sec",
            "range": "stddev: 0.00006278049083629527",
            "extra": "mean: 7.763729734513259 msec\nrounds: 113"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.125919119890197,
            "unit": "iter/sec",
            "range": "stddev: 0.0005159537926449789",
            "extra": "mean: 123.06300188888821 msec\nrounds: 9"
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
          "id": "6b932cb69e8fd5a31b68461792afe72ec9781bbb",
          "message": "feat(detectors): implement mathematically verified German Steuer-IdNr and Spanish NIF/NIE/CIF detectors",
          "timestamp": "2026-09-18T11:11:42+02:00",
          "tree_id": "6a1f195d9a8c53c3b05c35e0e309414e18f41962",
          "url": "https://github.com/ma2za/pseudonymize/commit/6b932cb69e8fd5a31b68461792afe72ec9781bbb"
        },
        "date": 1789722747218,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 609.7800303530412,
            "unit": "iter/sec",
            "range": "stddev: 0.000017471443218689786",
            "extra": "mean: 1.6399356328888555 msec\nrounds: 602"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 640.338362155604,
            "unit": "iter/sec",
            "range": "stddev: 0.00002791819678266749",
            "extra": "mean: 1.5616743570284441 msec\nrounds: 619"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 357.4612187135383,
            "unit": "iter/sec",
            "range": "stddev: 0.00013492119298090885",
            "extra": "mean: 2.7975062682292773 msec\nrounds: 384"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 507.4706232659686,
            "unit": "iter/sec",
            "range": "stddev: 0.00003701063953646256",
            "extra": "mean: 1.9705574158445298 msec\nrounds: 505"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 437.3699944121831,
            "unit": "iter/sec",
            "range": "stddev: 0.000027634101575432446",
            "extra": "mean: 2.286393700473168 msec\nrounds: 424"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 314.89190973409217,
            "unit": "iter/sec",
            "range": "stddev: 0.00005480981409697431",
            "extra": "mean: 3.1756928936168656 msec\nrounds: 329"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 276.11034468008756,
            "unit": "iter/sec",
            "range": "stddev: 0.00003736409919278294",
            "extra": "mean: 3.6217404355444915 msec\nrounds: 287"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 579.1096267572707,
            "unit": "iter/sec",
            "range": "stddev: 0.00005951891766322827",
            "extra": "mean: 1.7267887698560782 msec\nrounds: 617"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 77.10986799918817,
            "unit": "iter/sec",
            "range": "stddev: 0.00019895956707405383",
            "extra": "mean: 12.968508777767955 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 142.32491847881138,
            "unit": "iter/sec",
            "range": "stddev: 0.00004897379387401691",
            "extra": "mean: 7.026176517001659 msec\nrounds: 147"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 515.1168754140593,
            "unit": "iter/sec",
            "range": "stddev: 0.00003832986368853936",
            "extra": "mean: 1.941307007649834 msec\nrounds: 523"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1836.6727556247463,
            "unit": "iter/sec",
            "range": "stddev: 0.000007370455032083654",
            "extra": "mean: 544.4628047851937 usec\nrounds: 1839"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 188.5400317748435,
            "unit": "iter/sec",
            "range": "stddev: 0.00003171292108084263",
            "extra": "mean: 5.303913394871019 msec\nrounds: 195"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 76.9995413211381,
            "unit": "iter/sec",
            "range": "stddev: 0.001554807695657353",
            "extra": "mean: 12.98709034940027 msec\nrounds: 83"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 924.3148275405401,
            "unit": "iter/sec",
            "range": "stddev: 0.000012236282804401729",
            "extra": "mean: 1.0818824606123074 msec\nrounds: 914"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1178.5878567235536,
            "unit": "iter/sec",
            "range": "stddev: 0.000007187392267608624",
            "extra": "mean: 848.4730215870171 usec\nrounds: 1158"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 123.02673553138025,
            "unit": "iter/sec",
            "range": "stddev: 0.00006197000714587371",
            "extra": "mean: 8.12831451375812 msec\nrounds: 109"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.841349734666092,
            "unit": "iter/sec",
            "range": "stddev: 0.004860658044599149",
            "extra": "mean: 127.5290650000045 msec\nrounds: 8"
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
          "id": "81f407529613b179a6300f81f74cd3c5758e7938",
          "message": "style: satisfy pre-commit formatting for policy and tests",
          "timestamp": "2026-09-18T12:03:13+02:00",
          "tree_id": "ab1111363d5ab823529f578d4f127595d08c7e76",
          "url": "https://github.com/ma2za/pseudonymize/commit/81f407529613b179a6300f81f74cd3c5758e7938"
        },
        "date": 1789725833080,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 604.6497995337994,
            "unit": "iter/sec",
            "range": "stddev: 0.00008880217369411503",
            "extra": "mean: 1.653849882644509 msec\nrounds: 605"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 633.766663115499,
            "unit": "iter/sec",
            "range": "stddev: 0.000026138031225037875",
            "extra": "mean: 1.5778677835217059 msec\nrounds: 619"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 376.4036699361698,
            "unit": "iter/sec",
            "range": "stddev: 0.00007796128889647266",
            "extra": "mean: 2.6567222369791956 msec\nrounds: 384"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 517.3609063258165,
            "unit": "iter/sec",
            "range": "stddev: 0.00004545294193523568",
            "extra": "mean: 1.9328866711282464 msec\nrounds: 523"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 432.36986663918947,
            "unit": "iter/sec",
            "range": "stddev: 0.0001279853152433885",
            "extra": "mean: 2.312834628770499 msec\nrounds: 431"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 291.8025868717218,
            "unit": "iter/sec",
            "range": "stddev: 0.000431301384067474",
            "extra": "mean: 3.426974416918401 msec\nrounds: 331"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 269.70373601866527,
            "unit": "iter/sec",
            "range": "stddev: 0.0005361441603621574",
            "extra": "mean: 3.7077721456954285 msec\nrounds: 302"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 589.6654591794427,
            "unit": "iter/sec",
            "range": "stddev: 0.000042765478453010536",
            "extra": "mean: 1.6958768475120862 msec\nrounds: 623"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 79.38615340969324,
            "unit": "iter/sec",
            "range": "stddev: 0.00009392797126457267",
            "extra": "mean: 12.596655172838965 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 141.46530558051276,
            "unit": "iter/sec",
            "range": "stddev: 0.00005096579183167948",
            "extra": "mean: 7.068871027397354 msec\nrounds: 146"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 515.5723728319657,
            "unit": "iter/sec",
            "range": "stddev: 0.00009111826790282096",
            "extra": "mean: 1.9395919034744669 msec\nrounds: 518"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1829.594449126497,
            "unit": "iter/sec",
            "range": "stddev: 0.000009074361455664183",
            "extra": "mean: 546.5692140011847 usec\nrounds: 1757"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 187.15119447645534,
            "unit": "iter/sec",
            "range": "stddev: 0.00006142471748888275",
            "extra": "mean: 5.3432734041449335 msec\nrounds: 193"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 79.2460018927945,
            "unit": "iter/sec",
            "range": "stddev: 0.0006950730480857971",
            "extra": "mean: 12.618933146341176 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 916.2275987476146,
            "unit": "iter/sec",
            "range": "stddev: 0.000021199191771427573",
            "extra": "mean: 1.0914318684210051 msec\nrounds: 912"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1176.3125292146226,
            "unit": "iter/sec",
            "range": "stddev: 0.000009981558173808643",
            "extra": "mean: 850.114212986969 usec\nrounds: 1155"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 123.44311980363403,
            "unit": "iter/sec",
            "range": "stddev: 0.00006381143478498627",
            "extra": "mean: 8.100897009009012 msec\nrounds: 111"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.038381382079695,
            "unit": "iter/sec",
            "range": "stddev: 0.0006711839531757071",
            "extra": "mean: 124.40315437500172 msec\nrounds: 8"
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
          "id": "d92084e73c16ff8ad2893f0ef42a385700bd2708",
          "message": "chore(release): prepare and publish release v1.23.0",
          "timestamp": "2026-09-18T12:09:02+02:00",
          "tree_id": "562b6ed545d88523bd3ba1612bb0821c1b54f5e0",
          "url": "https://github.com/ma2za/pseudonymize/commit/d92084e73c16ff8ad2893f0ef42a385700bd2708"
        },
        "date": 1789726177669,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 611.0714270677901,
            "unit": "iter/sec",
            "range": "stddev: 0.000019591035059338742",
            "extra": "mean: 1.6364699046696936 msec\nrounds: 514"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 633.9966323504495,
            "unit": "iter/sec",
            "range": "stddev: 0.000022259484138209436",
            "extra": "mean: 1.5772954444452594 msec\nrounds: 621"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 346.6979062755086,
            "unit": "iter/sec",
            "range": "stddev: 0.0002714487269044393",
            "extra": "mean: 2.8843554630679984 msec\nrounds: 352"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 503.8999758545523,
            "unit": "iter/sec",
            "range": "stddev: 0.00002019121447688882",
            "extra": "mean: 1.984520833334281 msec\nrounds: 498"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 429.41729734053064,
            "unit": "iter/sec",
            "range": "stddev: 0.000021378359960104903",
            "extra": "mean: 2.32873711933172 msec\nrounds: 419"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 308.61828329327216,
            "unit": "iter/sec",
            "range": "stddev: 0.00011164130439139367",
            "extra": "mean: 3.240248728393467 msec\nrounds: 324"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 283.747943624943,
            "unit": "iter/sec",
            "range": "stddev: 0.00005459820709602857",
            "extra": "mean: 3.5242546156450616 msec\nrounds: 294"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 607.0657003321089,
            "unit": "iter/sec",
            "range": "stddev: 0.000052458910161327204",
            "extra": "mean: 1.6472681613422198 msec\nrounds: 626"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 78.5286346191787,
            "unit": "iter/sec",
            "range": "stddev: 0.00006344004976751533",
            "extra": "mean: 12.734208417725048 msec\nrounds: 79"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 142.3715460280541,
            "unit": "iter/sec",
            "range": "stddev: 0.00008238516241629907",
            "extra": "mean: 7.023875401359704 msec\nrounds: 147"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 518.967705767413,
            "unit": "iter/sec",
            "range": "stddev: 0.00006229093382088031",
            "extra": "mean: 1.9269021730769744 msec\nrounds: 520"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1825.034140713869,
            "unit": "iter/sec",
            "range": "stddev: 0.000009698310747081847",
            "extra": "mean: 547.9349551284812 usec\nrounds: 1716"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 183.20282628554392,
            "unit": "iter/sec",
            "range": "stddev: 0.00004058759156708113",
            "extra": "mean: 5.458431074864414 msec\nrounds: 187"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 80.29461716410214,
            "unit": "iter/sec",
            "range": "stddev: 0.00018818447609552332",
            "extra": "mean: 12.454134975900686 msec\nrounds: 83"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 896.7943042011334,
            "unit": "iter/sec",
            "range": "stddev: 0.00004191785556738126",
            "extra": "mean: 1.1150829073237731 msec\nrounds: 874"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1176.7928413145833,
            "unit": "iter/sec",
            "range": "stddev: 0.000011618773638083638",
            "extra": "mean: 849.7672359078174 usec\nrounds: 1153"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 122.1029360626977,
            "unit": "iter/sec",
            "range": "stddev: 0.00016877713196150653",
            "extra": "mean: 8.189811254714774 msec\nrounds: 106"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.890936836877463,
            "unit": "iter/sec",
            "range": "stddev: 0.0005136112435222711",
            "extra": "mean: 126.72766500000421 msec\nrounds: 8"
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
          "id": "ed0e8e92d76b01d16b9e9d8da5e4266fb90ee093",
          "message": "chore(release): bump development version to 1.24.0 and prepare CHANGELOG.md",
          "timestamp": "2026-09-18T12:10:26+02:00",
          "tree_id": "1e60346f44e4222699ce72697571324699729ac0",
          "url": "https://github.com/ma2za/pseudonymize/commit/ed0e8e92d76b01d16b9e9d8da5e4266fb90ee093"
        },
        "date": 1789726260723,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 608.6175615533622,
            "unit": "iter/sec",
            "range": "stddev: 0.000022248749639409034",
            "extra": "mean: 1.643067934891199 msec\nrounds: 599"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 622.8294530150688,
            "unit": "iter/sec",
            "range": "stddev: 0.00008226346852185012",
            "extra": "mean: 1.6055759649115469 msec\nrounds: 627"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 379.38969865362156,
            "unit": "iter/sec",
            "range": "stddev: 0.00003370874019506487",
            "extra": "mean: 2.635812209843337 msec\nrounds: 386"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 516.6245666376423,
            "unit": "iter/sec",
            "range": "stddev: 0.00007248028312428141",
            "extra": "mean: 1.935641594646417 msec\nrounds: 523"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 421.60911420217604,
            "unit": "iter/sec",
            "range": "stddev: 0.0002038380875162212",
            "extra": "mean: 2.3718652332560004 msec\nrounds: 433"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 319.18775373678045,
            "unit": "iter/sec",
            "range": "stddev: 0.00005380250677606483",
            "extra": "mean: 3.1329522774381067 msec\nrounds: 328"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 291.2494174594026,
            "unit": "iter/sec",
            "range": "stddev: 0.00013703437419864672",
            "extra": "mean: 3.433483262294904 msec\nrounds: 305"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 586.7026126434628,
            "unit": "iter/sec",
            "range": "stddev: 0.0001437912309327755",
            "extra": "mean: 1.7044410207999137 msec\nrounds: 625"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 79.95578070225133,
            "unit": "iter/sec",
            "range": "stddev: 0.0007676360992025237",
            "extra": "mean: 12.506913086421065 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 144.27194027513528,
            "unit": "iter/sec",
            "range": "stddev: 0.00006221573018799099",
            "extra": "mean: 6.931354760273826 msec\nrounds: 146"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 511.87469092542636,
            "unit": "iter/sec",
            "range": "stddev: 0.000034956967119349606",
            "extra": "mean: 1.9536031332045038 msec\nrounds: 518"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1823.962493797153,
            "unit": "iter/sec",
            "range": "stddev: 0.000023145977538158712",
            "extra": "mean: 548.2568876283112 usec\nrounds: 1762"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 183.51829270190288,
            "unit": "iter/sec",
            "range": "stddev: 0.00011710653054485612",
            "extra": "mean: 5.449048077318077 msec\nrounds: 194"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 78.14078969899583,
            "unit": "iter/sec",
            "range": "stddev: 0.00010204189181116968",
            "extra": "mean: 12.797413538461473 msec\nrounds: 78"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 918.5278038296613,
            "unit": "iter/sec",
            "range": "stddev: 0.000013605353555163893",
            "extra": "mean: 1.0886986717556648 msec\nrounds: 917"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1175.6708772820082,
            "unit": "iter/sec",
            "range": "stddev: 0.00001011314648120399",
            "extra": "mean: 850.5781841869423 usec\nrounds: 1151"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 122.92455437018731,
            "unit": "iter/sec",
            "range": "stddev: 0.00007004768102501352",
            "extra": "mean: 8.13507118348788 msec\nrounds: 109"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.912197795125939,
            "unit": "iter/sec",
            "range": "stddev: 0.0006154286057738824",
            "extra": "mean: 126.38713362499843 msec\nrounds: 8"
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
          "id": "878c6dbe91f5dae7c605e3e9ca42a92649c1e755",
          "message": "style: finalize public API exports and stabilize property tests invariants",
          "timestamp": "2026-09-18T12:30:51+02:00",
          "tree_id": "9fc8cb616fafbc751f89d7ddaa436bf743f27cc0",
          "url": "https://github.com/ma2za/pseudonymize/commit/878c6dbe91f5dae7c605e3e9ca42a92649c1e755"
        },
        "date": 1789727490874,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 610.1491202495336,
            "unit": "iter/sec",
            "range": "stddev: 0.00001671840531595519",
            "extra": "mean: 1.6389436070825254 msec\nrounds: 593"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 619.8135989404843,
            "unit": "iter/sec",
            "range": "stddev: 0.00004379784761771134",
            "extra": "mean: 1.6133882859450164 msec\nrounds: 619"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 384.9527576902048,
            "unit": "iter/sec",
            "range": "stddev: 0.00007068837987107654",
            "extra": "mean: 2.5977213567716837 msec\nrounds: 384"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 500.7064701645487,
            "unit": "iter/sec",
            "range": "stddev: 0.00013027357227699468",
            "extra": "mean: 1.997178106508923 msec\nrounds: 507"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 431.39407591107766,
            "unit": "iter/sec",
            "range": "stddev: 0.00004346223525778785",
            "extra": "mean: 2.318066139151451 msec\nrounds: 424"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 321.34469524971354,
            "unit": "iter/sec",
            "range": "stddev: 0.00004722756402551946",
            "extra": "mean: 3.111923161584823 msec\nrounds: 328"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 293.27347881461117,
            "unit": "iter/sec",
            "range": "stddev: 0.00008264795162430667",
            "extra": "mean: 3.4097866743420613 msec\nrounds: 304"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 585.7758600219868,
            "unit": "iter/sec",
            "range": "stddev: 0.000013027231956674899",
            "extra": "mean: 1.707137607142885 msec\nrounds: 616"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 79.38830974110151,
            "unit": "iter/sec",
            "range": "stddev: 0.00010725841398233348",
            "extra": "mean: 12.59631302469049 msec\nrounds: 81"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 147.29512580373583,
            "unit": "iter/sec",
            "range": "stddev: 0.000027536937901783363",
            "extra": "mean: 6.789090912162669 msec\nrounds: 148"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 499.38535391829606,
            "unit": "iter/sec",
            "range": "stddev: 0.00004556711665958096",
            "extra": "mean: 2.002461610365147 msec\nrounds: 521"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1833.1706079930111,
            "unit": "iter/sec",
            "range": "stddev: 0.000008808306681112772",
            "extra": "mean: 545.5029639029716 usec\nrounds: 1773"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 188.61330782262235,
            "unit": "iter/sec",
            "range": "stddev: 0.00009686404905936856",
            "extra": "mean: 5.301852830768603 msec\nrounds: 195"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 79.85133403275702,
            "unit": "iter/sec",
            "range": "stddev: 0.00015453932329995642",
            "extra": "mean: 12.52327230487815 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 918.4625689995983,
            "unit": "iter/sec",
            "range": "stddev: 0.00006038790917641929",
            "extra": "mean: 1.0887759977951126 msec\nrounds: 907"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1178.6006617322587,
            "unit": "iter/sec",
            "range": "stddev: 0.000012140803291984622",
            "extra": "mean: 848.4638032785772 usec\nrounds: 1159"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 122.91400114218074,
            "unit": "iter/sec",
            "range": "stddev: 0.00006319362835801135",
            "extra": "mean: 8.1357696495719 msec\nrounds: 117"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.921974571174873,
            "unit": "iter/sec",
            "range": "stddev: 0.0012219322298136401",
            "extra": "mean: 126.23115499999571 msec\nrounds: 8"
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
          "id": "c68cdb096f1b0027cbd02d6c93c5f87edc2883ed",
          "message": "chore(release): prepare and publish release v1.25.0",
          "timestamp": "2026-09-18T13:32:42+02:00",
          "tree_id": "916148458ab42b22e2b9803d4631b7dcb9a0b537",
          "url": "https://github.com/ma2za/pseudonymize/commit/c68cdb096f1b0027cbd02d6c93c5f87edc2883ed"
        },
        "date": 1789731198619,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 651.6408742618116,
            "unit": "iter/sec",
            "range": "stddev: 0.00001833494563970759",
            "extra": "mean: 1.534587591873844 msec\nrounds: 566"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 680.1420787653088,
            "unit": "iter/sec",
            "range": "stddev: 0.00019994525732302745",
            "extra": "mean: 1.4702810357143952 msec\nrounds: 700"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 349.5231893773979,
            "unit": "iter/sec",
            "range": "stddev: 0.000029430500261268812",
            "extra": "mean: 2.861040498575473 msec\nrounds: 351"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 574.9289224336819,
            "unit": "iter/sec",
            "range": "stddev: 0.00002579190434829175",
            "extra": "mean: 1.7393454407668105 msec\nrounds: 574"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 517.9148332871016,
            "unit": "iter/sec",
            "range": "stddev: 0.00003883966532075268",
            "extra": "mean: 1.9308193852128166 msec\nrounds: 514"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 345.9929840514723,
            "unit": "iter/sec",
            "range": "stddev: 0.0001427945923945068",
            "extra": "mean: 2.890232016529078 msec\nrounds: 363"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 320.38643889486195,
            "unit": "iter/sec",
            "range": "stddev: 0.00011213719194843807",
            "extra": "mean: 3.1212307345135795 msec\nrounds: 339"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 673.211921111311,
            "unit": "iter/sec",
            "range": "stddev: 0.00024458949977988043",
            "extra": "mean: 1.4854163579712618 msec\nrounds: 690"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 84.35093787693982,
            "unit": "iter/sec",
            "range": "stddev: 0.00013006396962433723",
            "extra": "mean: 11.855232735632494 msec\nrounds: 87"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 151.06132515773552,
            "unit": "iter/sec",
            "range": "stddev: 0.00005308959803159022",
            "extra": "mean: 6.619828066222893 msec\nrounds: 151"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 520.5483641466662,
            "unit": "iter/sec",
            "range": "stddev: 0.00003373735685807176",
            "extra": "mean: 1.9210510855015321 msec\nrounds: 538"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1883.7948746981276,
            "unit": "iter/sec",
            "range": "stddev: 0.000011472676680048884",
            "extra": "mean: 530.8433595564628 usec\nrounds: 1805"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 192.62345163140944,
            "unit": "iter/sec",
            "range": "stddev: 0.00007312446492541304",
            "extra": "mean: 5.191475864078736 msec\nrounds: 206"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 86.36998138125678,
            "unit": "iter/sec",
            "range": "stddev: 0.00015759594810606947",
            "extra": "mean: 11.578096741572425 msec\nrounds: 89"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1026.5426033646395,
            "unit": "iter/sec",
            "range": "stddev: 0.00002874369474486144",
            "extra": "mean: 974.1436904054032 usec\nrounds: 1011"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1269.0761167577787,
            "unit": "iter/sec",
            "range": "stddev: 0.00008413231139604879",
            "extra": "mean: 787.974800561836 usec\nrounds: 1068"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 125.74598646625356,
            "unit": "iter/sec",
            "range": "stddev: 0.0001514541792979496",
            "extra": "mean: 7.952540101694378 msec\nrounds: 118"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.199202794973932,
            "unit": "iter/sec",
            "range": "stddev: 0.0009157735805709391",
            "extra": "mean: 121.96307677778071 msec\nrounds: 9"
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
          "id": "ab0a0f47b6a65e84e9a28bc23d249e4ad0098f93",
          "message": "chore(release): bump version to 1.25.0 in configuration",
          "timestamp": "2026-09-18T13:34:55+02:00",
          "tree_id": "26c075faa2ec31e22f6e080cfc1d41924696c71b",
          "url": "https://github.com/ma2za/pseudonymize/commit/ab0a0f47b6a65e84e9a28bc23d249e4ad0098f93"
        },
        "date": 1789731334110,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 651.7270101135668,
            "unit": "iter/sec",
            "range": "stddev: 0.00001837874506573593",
            "extra": "mean: 1.534384772277191 msec\nrounds: 606"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 703.6043842609126,
            "unit": "iter/sec",
            "range": "stddev: 0.0000169384478337467",
            "extra": "mean: 1.4212532246376355 msec\nrounds: 690"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 385.3100108822856,
            "unit": "iter/sec",
            "range": "stddev: 0.000017836580315840812",
            "extra": "mean: 2.5953127916666188 msec\nrounds: 384"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 573.6175585986067,
            "unit": "iter/sec",
            "range": "stddev: 0.000028792207636710873",
            "extra": "mean: 1.743321809121533 msec\nrounds: 592"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 515.5509815063294,
            "unit": "iter/sec",
            "range": "stddev: 0.00001922950193196916",
            "extra": "mean: 1.9396723813389212 msec\nrounds: 493"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 350.6950464736956,
            "unit": "iter/sec",
            "range": "stddev: 0.000037615092070566914",
            "extra": "mean: 2.851480253442948 msec\nrounds: 363"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 319.1153602374503,
            "unit": "iter/sec",
            "range": "stddev: 0.0002747569047577777",
            "extra": "mean: 3.133663009063276 msec\nrounds: 331"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 706.7842995814077,
            "unit": "iter/sec",
            "range": "stddev: 0.000019695191611648874",
            "extra": "mean: 1.4148588198581222 msec\nrounds: 705"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 81.39176057399436,
            "unit": "iter/sec",
            "range": "stddev: 0.00003882362565402474",
            "extra": "mean: 12.286255917647662 msec\nrounds: 85"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 151.11644458976733,
            "unit": "iter/sec",
            "range": "stddev: 0.00003444048075748183",
            "extra": "mean: 6.617413496689121 msec\nrounds: 151"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 539.5315180051706,
            "unit": "iter/sec",
            "range": "stddev: 0.000022263345509898117",
            "extra": "mean: 1.8534598380782945 msec\nrounds: 562"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1882.365082874678,
            "unit": "iter/sec",
            "range": "stddev: 0.00001152589741797501",
            "extra": "mean: 531.2465733123552 usec\nrounds: 1896"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 208.1863707379306,
            "unit": "iter/sec",
            "range": "stddev: 0.0000369613391247627",
            "extra": "mean: 4.8033884084507195 msec\nrounds: 213"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 84.25021792372051,
            "unit": "iter/sec",
            "range": "stddev: 0.00012124319268133869",
            "extra": "mean: 11.86940549999992 msec\nrounds: 84"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 953.7153912193404,
            "unit": "iter/sec",
            "range": "stddev: 0.000010901070965112202",
            "extra": "mean: 1.048530839710455 msec\nrounds: 967"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1293.812731899516,
            "unit": "iter/sec",
            "range": "stddev: 0.000009315933521218165",
            "extra": "mean: 772.9093827449404 usec\nrounds: 1275"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 127.0106818868164,
            "unit": "iter/sec",
            "range": "stddev: 0.00010858741322960671",
            "extra": "mean: 7.8733535254234335 msec\nrounds: 118"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.132360249683602,
            "unit": "iter/sec",
            "range": "stddev: 0.005076284822990846",
            "extra": "mean: 122.96553144444209 msec\nrounds: 9"
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
          "id": "c2fd7fc015ccae5aee7c6e6039460e43d4cf6086",
          "message": "chore(release): bump development version to 1.26.0 and prepare CHANGELOG.md",
          "timestamp": "2026-09-18T13:36:08+02:00",
          "tree_id": "92285f969332d6d83d0edb469283de1c48f56995",
          "url": "https://github.com/ma2za/pseudonymize/commit/c2fd7fc015ccae5aee7c6e6039460e43d4cf6086"
        },
        "date": 1789731401695,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 601.4668802452883,
            "unit": "iter/sec",
            "range": "stddev: 0.00014355638539382008",
            "extra": "mean: 1.6626019367719518 msec\nrounds: 601"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 633.0989108189622,
            "unit": "iter/sec",
            "range": "stddev: 0.000028997231094027154",
            "extra": "mean: 1.579532017684919 msec\nrounds: 622"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 385.9637483549242,
            "unit": "iter/sec",
            "range": "stddev: 0.0000763935933797538",
            "extra": "mean: 2.5909169041451556 msec\nrounds: 386"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 504.3892438865414,
            "unit": "iter/sec",
            "range": "stddev: 0.00013263129579300502",
            "extra": "mean: 1.9825958069497265 msec\nrounds: 518"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 425.7238366253491,
            "unit": "iter/sec",
            "range": "stddev: 0.000044114473298986874",
            "extra": "mean: 2.3489405900474223 msec\nrounds: 422"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 320.0716391455248,
            "unit": "iter/sec",
            "range": "stddev: 0.00015047984530251374",
            "extra": "mean: 3.1243005555557417 msec\nrounds: 324"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 290.847093804622,
            "unit": "iter/sec",
            "range": "stddev: 0.00014013640007258548",
            "extra": "mean: 3.4382327391304623 msec\nrounds: 299"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 614.21171589549,
            "unit": "iter/sec",
            "range": "stddev: 0.00024880801789402816",
            "extra": "mean: 1.6281031021071455 msec\nrounds: 617"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 81.50650278542139,
            "unit": "iter/sec",
            "range": "stddev: 0.00024165603584176698",
            "extra": "mean: 12.268959725000794 msec\nrounds: 80"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 143.59889839269206,
            "unit": "iter/sec",
            "range": "stddev: 0.0001672064366486403",
            "extra": "mean: 6.963841722973074 msec\nrounds: 148"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 496.14264492806694,
            "unit": "iter/sec",
            "range": "stddev: 0.00003322633222291455",
            "extra": "mean: 2.0155493792414974 msec\nrounds: 501"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1835.20476776989,
            "unit": "iter/sec",
            "range": "stddev: 0.000013340147346244881",
            "extra": "mean: 544.8983228259499 usec\nrounds: 1840"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 190.68992263331944,
            "unit": "iter/sec",
            "range": "stddev: 0.00003330582158618814",
            "extra": "mean: 5.244115610256527 msec\nrounds: 195"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 80.19091024882637,
            "unit": "iter/sec",
            "range": "stddev: 0.00007548035571033188",
            "extra": "mean: 12.470241289157027 msec\nrounds: 83"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 923.9570387351365,
            "unit": "iter/sec",
            "range": "stddev: 0.000012187645143196847",
            "extra": "mean: 1.0823014037199863 msec\nrounds: 914"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1177.9477747690114,
            "unit": "iter/sec",
            "range": "stddev: 0.000011923697205108631",
            "extra": "mean: 848.93407111881 usec\nrounds: 1153"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 121.63001902388407,
            "unit": "iter/sec",
            "range": "stddev: 0.000525944834026508",
            "extra": "mean: 8.221654555555347 msec\nrounds: 117"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.920991390173468,
            "unit": "iter/sec",
            "range": "stddev: 0.0008605372680376972",
            "extra": "mean: 126.2468232499998 msec\nrounds: 8"
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
          "id": "de4b930d1ca0e6519ca120825106fa7530fe8229",
          "message": "refactor: remove FastAPI server and associated endpoints, dependencies, and integration tests",
          "timestamp": "2026-09-22T08:50:12+02:00",
          "tree_id": "4091474d7166b5211af86c0024e5f385378bd5a3",
          "url": "https://github.com/ma2za/pseudonymize/commit/de4b930d1ca0e6519ca120825106fa7530fe8229"
        },
        "date": 1790059872286,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 588.0154879395188,
            "unit": "iter/sec",
            "range": "stddev: 0.00021822457274558606",
            "extra": "mean: 1.700635477313918 msec\nrounds: 551"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 619.5606309376248,
            "unit": "iter/sec",
            "range": "stddev: 0.00017731109140993988",
            "extra": "mean: 1.6140470360207193 msec\nrounds: 583"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 334.0044148091128,
            "unit": "iter/sec",
            "range": "stddev: 0.0005993415460574675",
            "extra": "mean: 2.993972401746579 msec\nrounds: 229"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 521.7791525493279,
            "unit": "iter/sec",
            "range": "stddev: 0.00004461504050806809",
            "extra": "mean: 1.9165196522593189 msec\nrounds: 509"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 436.1119278328319,
            "unit": "iter/sec",
            "range": "stddev: 0.000023131428778947955",
            "extra": "mean: 2.2929893364056637 msec\nrounds: 434"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 317.47788700496795,
            "unit": "iter/sec",
            "range": "stddev: 0.0000613694500640823",
            "extra": "mean: 3.1498256758410137 msec\nrounds: 327"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 292.92750098325763,
            "unit": "iter/sec",
            "range": "stddev: 0.0000678801896624828",
            "extra": "mean: 3.413813986885292 msec\nrounds: 305"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 596.4662750298979,
            "unit": "iter/sec",
            "range": "stddev: 0.00011808853045137191",
            "extra": "mean: 1.6765407230272573 msec\nrounds: 621"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 77.75950248241244,
            "unit": "iter/sec",
            "range": "stddev: 0.0006145500156880003",
            "extra": "mean: 12.860164585365998 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 142.96915989337964,
            "unit": "iter/sec",
            "range": "stddev: 0.00016096403917893666",
            "extra": "mean: 6.994515465753299 msec\nrounds: 146"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 510.2372346163236,
            "unit": "iter/sec",
            "range": "stddev: 0.0000673583300995966",
            "extra": "mean: 1.9598726477732595 msec\nrounds: 494"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1780.7699975229716,
            "unit": "iter/sec",
            "range": "stddev: 0.00007629273225293408",
            "extra": "mean: 561.5548338027861 usec\nrounds: 1775"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 186.13518878488824,
            "unit": "iter/sec",
            "range": "stddev: 0.00005790886812473448",
            "extra": "mean: 5.372439282051471 msec\nrounds: 195"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 79.6478047770954,
            "unit": "iter/sec",
            "range": "stddev: 0.0001420466372536726",
            "extra": "mean: 12.55527384337369 msec\nrounds: 83"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 900.0670879058575,
            "unit": "iter/sec",
            "range": "stddev: 0.00004384545050764754",
            "extra": "mean: 1.1110282927094375 msec\nrounds: 919"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1173.7913818534364,
            "unit": "iter/sec",
            "range": "stddev: 0.000032072737193646894",
            "extra": "mean: 851.9401449523194 usec\nrounds: 1159"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 121.57666896422164,
            "unit": "iter/sec",
            "range": "stddev: 0.0007141897736680624",
            "extra": "mean: 8.225262367521243 msec\nrounds: 117"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.98289697850527,
            "unit": "iter/sec",
            "range": "stddev: 0.000688244027520969",
            "extra": "mean: 125.26780724999931 msec\nrounds: 8"
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
          "id": "8ec7e1118e8122ce85b28ef6fe755ed4a9b93301",
          "message": "chore: restore dependency-free base release contract",
          "timestamp": "2026-09-22T16:44:30+02:00",
          "tree_id": "154f7f58f904ad7b5daf64b5d7047f163b68fa96",
          "url": "https://github.com/ma2za/pseudonymize/commit/8ec7e1118e8122ce85b28ef6fe755ed4a9b93301"
        },
        "date": 1790088340604,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 610.8316263420174,
            "unit": "iter/sec",
            "range": "stddev: 0.00016914851976838498",
            "extra": "mean: 1.6371123512194816 msec\nrounds: 615"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 640.7100697276258,
            "unit": "iter/sec",
            "range": "stddev: 0.000031961420223528976",
            "extra": "mean: 1.5607683525640748 msec\nrounds: 624"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 438.1003127048109,
            "unit": "iter/sec",
            "range": "stddev: 0.00008350914158552748",
            "extra": "mean: 2.282582255707709 msec\nrounds: 438"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 589.143794093271,
            "unit": "iter/sec",
            "range": "stddev: 0.000063804503793919",
            "extra": "mean: 1.6973784838709236 msec\nrounds: 589"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 540.7372141837318,
            "unit": "iter/sec",
            "range": "stddev: 0.00006188757194108913",
            "extra": "mean: 1.84932712927766 msec\nrounds: 526"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 383.40179949178633,
            "unit": "iter/sec",
            "range": "stddev: 0.0001536003311994495",
            "extra": "mean: 2.6082298031087436 msec\nrounds: 386"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 361.2739513717544,
            "unit": "iter/sec",
            "range": "stddev: 0.0001420193024801682",
            "extra": "mean: 2.76798256891483 msec\nrounds: 341"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 618.0021993540142,
            "unit": "iter/sec",
            "range": "stddev: 0.0003128435754554022",
            "extra": "mean: 1.6181172187498372 msec\nrounds: 640"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 94.76943354973253,
            "unit": "iter/sec",
            "range": "stddev: 0.000050775587191337255",
            "extra": "mean: 10.551925473683728 msec\nrounds: 95"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 151.72587859651173,
            "unit": "iter/sec",
            "range": "stddev: 0.00005721365380414035",
            "extra": "mean: 6.590833477124387 msec\nrounds: 153"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 567.5683765949158,
            "unit": "iter/sec",
            "range": "stddev: 0.000040861547703321784",
            "extra": "mean: 1.7619022504379571 msec\nrounds: 571"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1948.802275092606,
            "unit": "iter/sec",
            "range": "stddev: 0.000015862643421088454",
            "extra": "mean: 513.1356899470371 usec\nrounds: 1890"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 226.3966090508282,
            "unit": "iter/sec",
            "range": "stddev: 0.000051585449396659806",
            "extra": "mean: 4.417027287610525 msec\nrounds: 226"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 98.34849169529666,
            "unit": "iter/sec",
            "range": "stddev: 0.000050514475070429994",
            "extra": "mean: 10.16792411111093 msec\nrounds: 99"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1018.959525908577,
            "unit": "iter/sec",
            "range": "stddev: 0.000019069649630543366",
            "extra": "mean: 981.3932492640752 usec\nrounds: 1019"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1303.5214156481834,
            "unit": "iter/sec",
            "range": "stddev: 0.000022451201657222685",
            "extra": "mean: 767.1527203124195 usec\nrounds: 1280"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 140.99320454407186,
            "unit": "iter/sec",
            "range": "stddev: 0.0001294952971978343",
            "extra": "mean: 7.092540404579701 msec\nrounds: 131"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.948539535260538,
            "unit": "iter/sec",
            "range": "stddev: 0.0005224299140476973",
            "extra": "mean: 111.75007900000129 msec\nrounds: 9"
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
          "id": "27e2be880389ad7a870b8330568c77aa9c21dd2b",
          "message": "fix: harden optional remote and benchmark paths",
          "timestamp": "2026-09-23T07:35:00+02:00",
          "tree_id": "68c422d37d593d171c690fc1df9300b379d4cee7",
          "url": "https://github.com/ma2za/pseudonymize/commit/27e2be880389ad7a870b8330568c77aa9c21dd2b"
        },
        "date": 1790141756286,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 892.0566644635734,
            "unit": "iter/sec",
            "range": "stddev: 0.00003266272863157888",
            "extra": "mean: 1.121005021134321 msec\nrounds: 899"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 933.6467729037072,
            "unit": "iter/sec",
            "range": "stddev: 0.000018526064078959985",
            "extra": "mean: 1.0710688763909393 msec\nrounds: 898"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 666.5612378903606,
            "unit": "iter/sec",
            "range": "stddev: 0.000041419509646196655",
            "extra": "mean: 1.5002372522665128 msec\nrounds: 662"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 846.9720375450794,
            "unit": "iter/sec",
            "range": "stddev: 0.000018774413039301194",
            "extra": "mean: 1.180676522566751 msec\nrounds: 842"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 789.704756473033,
            "unit": "iter/sec",
            "range": "stddev: 0.00014222027646545833",
            "extra": "mean: 1.266296032540293 msec\nrounds: 799"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 561.6851346017451,
            "unit": "iter/sec",
            "range": "stddev: 0.00002610510188527053",
            "extra": "mean: 1.7803568910703609 msec\nrounds: 560"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 518.4918915212261,
            "unit": "iter/sec",
            "range": "stddev: 0.000047154729339275344",
            "extra": "mean: 1.9286704697850843 msec\nrounds: 513"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 903.5074044133049,
            "unit": "iter/sec",
            "range": "stddev: 0.0000738943449640863",
            "extra": "mean: 1.1067977917119038 msec\nrounds: 917"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 122.47497715644215,
            "unit": "iter/sec",
            "range": "stddev: 0.00030639655353776116",
            "extra": "mean: 8.16493314158908 msec\nrounds: 113"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 241.94425832493198,
            "unit": "iter/sec",
            "range": "stddev: 0.00003496561034716069",
            "extra": "mean: 4.1331834320986305 msec\nrounds: 243"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 751.7162102536582,
            "unit": "iter/sec",
            "range": "stddev: 0.0000814212890217947",
            "extra": "mean: 1.3302892585787944 msec\nrounds: 816"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 2564.78080432008,
            "unit": "iter/sec",
            "range": "stddev: 0.000024941920890678174",
            "extra": "mean: 389.89686694302077 usec\nrounds: 2653"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 301.5660166304117,
            "unit": "iter/sec",
            "range": "stddev: 0.00010604102584248788",
            "extra": "mean: 3.316023506805024 msec\nrounds: 294"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 113.54020415124364,
            "unit": "iter/sec",
            "range": "stddev: 0.00033985319407866925",
            "extra": "mean: 8.807452897195153 msec\nrounds: 107"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1327.2963126011243,
            "unit": "iter/sec",
            "range": "stddev: 0.000042603944532399124",
            "extra": "mean: 753.4112695907996 usec\nrounds: 1391"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1806.686621647983,
            "unit": "iter/sec",
            "range": "stddev: 0.000010244137692471581",
            "extra": "mean: 553.4994215476297 usec\nrounds: 1810"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 198.14007845238135,
            "unit": "iter/sec",
            "range": "stddev: 0.00007921991517660786",
            "extra": "mean: 5.046934511234325 msec\nrounds: 178"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 12.256701066102913,
            "unit": "iter/sec",
            "range": "stddev: 0.006217245187891606",
            "extra": "mean: 81.5880223076988 msec\nrounds: 13"
          }
        ]
      }
    ]
  }
}