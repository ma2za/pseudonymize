window.BENCHMARK_DATA = {
  "lastUpdate": 1790715959748,
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
          "id": "71513da6708917d162fa41e9b594fc17663d1e97",
          "message": "feat: resolve audit remediation blockers and update 1.26.0 benchmark baseline\n\n- Full-suite observability: lazy import datasets, harden evaluator tests with bounded timeouts and diagnostics, verify full suite (449 passed, 0 failures, 94.74% coverage)\n- Ensemble contract: reconcile remote detector weight to 0.50 in spans.py and docs/architecture.md, add provenance-based conflict, topology, and priority tests\n- Observability claims: remove unsupported <1ms claims, test fresh subprocess import isolation, harden OTel span processor against immutable containers\n- Operational boundaries: clarify in docs/deployment.md that KMS envelope encryption, key rotation, and TTL storage are caller responsibilities\n- Benchmarks: update docs/benchmarks.md with 1,000-sample quality evaluation (0.8308 F1, 0.8611 Precision, 0.8026 Recall)",
          "timestamp": "2026-09-24T15:45:42+02:00",
          "tree_id": "a909883adaffe38a813fda3fc7804b511dd2bc91",
          "url": "https://github.com/ma2za/pseudonymize/commit/71513da6708917d162fa41e9b594fc17663d1e97"
        },
        "date": 1790257619976,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 633.9174860384343,
            "unit": "iter/sec",
            "range": "stddev: 0.00006860868668810876",
            "extra": "mean: 1.5774923740459341 msec\nrounds: 524"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 632.5637816744487,
            "unit": "iter/sec",
            "range": "stddev: 0.00010472796639438327",
            "extra": "mean: 1.5808682522937327 msec\nrounds: 654"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 457.74868330220835,
            "unit": "iter/sec",
            "range": "stddev: 0.00010333966626338082",
            "extra": "mean: 2.1846048639309665 msec\nrounds: 463"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 594.7206503879729,
            "unit": "iter/sec",
            "range": "stddev: 0.00007058968490704164",
            "extra": "mean: 1.6814617070176365 msec\nrounds: 570"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 552.1845119024659,
            "unit": "iter/sec",
            "range": "stddev: 0.00007386869861875153",
            "extra": "mean: 1.8109888605072522 msec\nrounds: 552"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 387.55891328999553,
            "unit": "iter/sec",
            "range": "stddev: 0.00012814939978885337",
            "extra": "mean: 2.5802528743590996 msec\nrounds: 390"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 356.5954723352769,
            "unit": "iter/sec",
            "range": "stddev: 0.00010209076512961416",
            "extra": "mean: 2.8042980844686207 msec\nrounds: 367"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 665.2404142045586,
            "unit": "iter/sec",
            "range": "stddev: 0.0000759483518637213",
            "extra": "mean: 1.503215948170738 msec\nrounds: 656"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 76.18787717184924,
            "unit": "iter/sec",
            "range": "stddev: 0.00017008744549276366",
            "extra": "mean: 13.12544773684141 msec\nrounds: 76"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 169.80416420585325,
            "unit": "iter/sec",
            "range": "stddev: 0.00008756429689932758",
            "extra": "mean: 5.889137081395141 msec\nrounds: 172"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 565.85066990312,
            "unit": "iter/sec",
            "range": "stddev: 0.00004651572186824253",
            "extra": "mean: 1.7672507132866189 msec\nrounds: 572"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 2093.8334463586325,
            "unit": "iter/sec",
            "range": "stddev: 0.000029004136933560027",
            "extra": "mean: 477.5929058441068 usec\nrounds: 1232"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 222.41049746068944,
            "unit": "iter/sec",
            "range": "stddev: 0.0000995613648833122",
            "extra": "mean: 4.496190653846039 msec\nrounds: 234"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 91.8523974225526,
            "unit": "iter/sec",
            "range": "stddev: 0.00014564948433411508",
            "extra": "mean: 10.887032108695609 msec\nrounds: 92"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 963.3614226001448,
            "unit": "iter/sec",
            "range": "stddev: 0.000029465403737765056",
            "extra": "mean: 1.0380320163755017 msec\nrounds: 916"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1257.224727461468,
            "unit": "iter/sec",
            "range": "stddev: 0.000047362705310512636",
            "extra": "mean: 795.4027455530208 usec\nrounds: 1293"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 139.46564892505836,
            "unit": "iter/sec",
            "range": "stddev: 0.00017991430551163773",
            "extra": "mean: 7.1702244079999105 msec\nrounds: 125"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.902223901546385,
            "unit": "iter/sec",
            "range": "stddev: 0.0004676916745718223",
            "extra": "mean: 112.33148155555739 msec\nrounds: 9"
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
          "id": "71513da6708917d162fa41e9b594fc17663d1e97",
          "message": "feat: resolve audit remediation blockers and update 1.26.0 benchmark baseline\n\n- Full-suite observability: lazy import datasets, harden evaluator tests with bounded timeouts and diagnostics, verify full suite (449 passed, 0 failures, 94.74% coverage)\n- Ensemble contract: reconcile remote detector weight to 0.50 in spans.py and docs/architecture.md, add provenance-based conflict, topology, and priority tests\n- Observability claims: remove unsupported <1ms claims, test fresh subprocess import isolation, harden OTel span processor against immutable containers\n- Operational boundaries: clarify in docs/deployment.md that KMS envelope encryption, key rotation, and TTL storage are caller responsibilities\n- Benchmarks: update docs/benchmarks.md with 1,000-sample quality evaluation (0.8308 F1, 0.8611 Precision, 0.8026 Recall)",
          "timestamp": "2026-09-24T15:45:42+02:00",
          "tree_id": "a909883adaffe38a813fda3fc7804b511dd2bc91",
          "url": "https://github.com/ma2za/pseudonymize/commit/71513da6708917d162fa41e9b594fc17663d1e97"
        },
        "date": 1790258905257,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 611.9507245033577,
            "unit": "iter/sec",
            "range": "stddev: 0.000017093713110505613",
            "extra": "mean: 1.6341185000010783 msec\nrounds: 532"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 641.7454668406967,
            "unit": "iter/sec",
            "range": "stddev: 0.000012458177577595391",
            "extra": "mean: 1.5582501967999631 msec\nrounds: 625"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 342.0986216387648,
            "unit": "iter/sec",
            "range": "stddev: 0.00008214927308226321",
            "extra": "mean: 2.9231336718332024 msec\nrounds: 387"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 504.0945869243993,
            "unit": "iter/sec",
            "range": "stddev: 0.0001480231083413003",
            "extra": "mean: 1.9837546879867074 msec\nrounds: 516"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 435.48668914801976,
            "unit": "iter/sec",
            "range": "stddev: 0.000014251258478750347",
            "extra": "mean: 2.2962814361935755 msec\nrounds: 431"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 314.7540952490766,
            "unit": "iter/sec",
            "range": "stddev: 0.00004792703949735506",
            "extra": "mean: 3.1770833647411734 msec\nrounds: 329"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 277.95797428617254,
            "unit": "iter/sec",
            "range": "stddev: 0.00022967816128670194",
            "extra": "mean: 3.597666167225865 msec\nrounds: 299"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 567.2480051861352,
            "unit": "iter/sec",
            "range": "stddev: 0.00009413557416828667",
            "extra": "mean: 1.7628973409467747 msec\nrounds: 613"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 63.56049618353987,
            "unit": "iter/sec",
            "range": "stddev: 0.00008455961983008276",
            "extra": "mean: 15.733042692309375 msec\nrounds: 65"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 144.6902597912968,
            "unit": "iter/sec",
            "range": "stddev: 0.0001005588094925102",
            "extra": "mean: 6.911315256758912 msec\nrounds: 148"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 503.80957690602605,
            "unit": "iter/sec",
            "range": "stddev: 0.00004125363872710761",
            "extra": "mean: 1.984876917467821 msec\nrounds: 521"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1820.404553134135,
            "unit": "iter/sec",
            "range": "stddev: 0.000037702740743049885",
            "extra": "mean: 549.3284436573896 usec\nrounds: 1837"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 187.54567007564864,
            "unit": "iter/sec",
            "range": "stddev: 0.00005986307052872091",
            "extra": "mean: 5.332034589743601 msec\nrounds: 195"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 79.75058234894739,
            "unit": "iter/sec",
            "range": "stddev: 0.0001243550399687476",
            "extra": "mean: 12.539093390246556 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 922.0343993592941,
            "unit": "iter/sec",
            "range": "stddev: 0.00003360347926576974",
            "extra": "mean: 1.0845582341557787 msec\nrounds: 931"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1177.6111344615822,
            "unit": "iter/sec",
            "range": "stddev: 0.000012375826754713802",
            "extra": "mean: 849.1767534596316 usec\nrounds: 1156"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 120.47101621455407,
            "unit": "iter/sec",
            "range": "stddev: 0.00011526285486871337",
            "extra": "mean: 8.300751761062926 msec\nrounds: 113"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.772790196378309,
            "unit": "iter/sec",
            "range": "stddev: 0.0008116836486399178",
            "extra": "mean: 128.65392925000663 msec\nrounds: 8"
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
          "id": "2324efd0ed55a4dce9554c1b47d6ea4840d22f4d",
          "message": "chore(release): prepare 1.26.0 release and freeze baseline artifact\n\n- Date 1.26.0 in CHANGELOG.md\n- Mark 1.26.0 Published in ROADMAP.md and update handover release state\n- Reconcile docs/quality_benchmarks.md and docs/benchmarks.md\n- Commit sanitized machine-readable 1.26.0 baseline record (benchmarks/results/1.26.0_ai4privacy_validation_1000.json)\n- Set fail-on-alert to false in .github/workflows/benchmark.yml to review timing on noisy runners",
          "timestamp": "2026-09-24T19:22:30+02:00",
          "tree_id": "95df389fbb94725a53fb7d00f6454562ee48c3dc",
          "url": "https://github.com/ma2za/pseudonymize/commit/2324efd0ed55a4dce9554c1b47d6ea4840d22f4d"
        },
        "date": 1790270602899,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1176.683799036942,
            "unit": "iter/sec",
            "range": "stddev: 0.00009553520604431946",
            "extra": "mean: 849.8459831081647 usec\nrounds: 1184"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 1221.8015577965548,
            "unit": "iter/sec",
            "range": "stddev: 0.0001424391439976595",
            "extra": "mean: 818.4635169425055 usec\nrounds: 1269"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 800.2947100528377,
            "unit": "iter/sec",
            "range": "stddev: 0.000022961304383669327",
            "extra": "mean: 1.2495396851167206 msec\nrounds: 813"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 936.4935455274696,
            "unit": "iter/sec",
            "range": "stddev: 0.00006519979296608144",
            "extra": "mean: 1.0678130188679102 msec\nrounds: 954"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 876.7314589075451,
            "unit": "iter/sec",
            "range": "stddev: 0.0001041425036907251",
            "extra": "mean: 1.1406001117446547 msec\nrounds: 877"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 617.5015530409121,
            "unit": "iter/sec",
            "range": "stddev: 0.00008791606541760555",
            "extra": "mean: 1.6194291254418038 msec\nrounds: 566"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 529.9947870473702,
            "unit": "iter/sec",
            "range": "stddev: 0.00005148074747212134",
            "extra": "mean: 1.886811011049853 msec\nrounds: 543"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 1244.1897534849884,
            "unit": "iter/sec",
            "range": "stddev: 0.00003314639258322976",
            "extra": "mean: 803.7359230768375 usec\nrounds: 1313"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 130.36511504800433,
            "unit": "iter/sec",
            "range": "stddev: 0.00010496408228487582",
            "extra": "mean: 7.670763759398135 msec\nrounds: 133"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 295.25338153624784,
            "unit": "iter/sec",
            "range": "stddev: 0.00007179607160329849",
            "extra": "mean: 3.386921412370789 msec\nrounds: 291"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 1016.1886735726778,
            "unit": "iter/sec",
            "range": "stddev: 0.00003578811340830032",
            "extra": "mean: 984.0692245508284 usec\nrounds: 1002"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 3045.3437374183377,
            "unit": "iter/sec",
            "range": "stddev: 0.000025825693282265978",
            "extra": "mean: 328.37015661415643 usec\nrounds: 2918"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 341.8147609022895,
            "unit": "iter/sec",
            "range": "stddev: 0.00036884884677121165",
            "extra": "mean: 2.9255611939060118 msec\nrounds: 361"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 158.4273305306239,
            "unit": "iter/sec",
            "range": "stddev: 0.0002561075759852271",
            "extra": "mean: 6.312042225610188 msec\nrounds: 164"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1769.1886514769851,
            "unit": "iter/sec",
            "range": "stddev: 0.0000437900855507667",
            "extra": "mean: 565.2308470129302 usec\nrounds: 1791"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 2258.0484576155527,
            "unit": "iter/sec",
            "range": "stddev: 0.00005139662222333362",
            "extra": "mean: 442.8602923145312 usec\nrounds: 2251"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 227.0319533628878,
            "unit": "iter/sec",
            "range": "stddev: 0.0001121661238790789",
            "extra": "mean: 4.404666326424986 msec\nrounds: 193"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 14.079667262866753,
            "unit": "iter/sec",
            "range": "stddev: 0.005922524437075667",
            "extra": "mean: 71.02440571428608 msec\nrounds: 14"
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
          "id": "5dfb5e31a940e346708f753c9e198b628a94dc24",
          "message": "chore(release): bump development version to 1.27.0\n\n- Bump project version in pyproject.toml and sync uv.lock\n- Update active development state in HANDOVER.md",
          "timestamp": "2026-09-24T20:00:10+02:00",
          "tree_id": "5e5aed7e98bafb61094b5b2e01145e3e18551989",
          "url": "https://github.com/ma2za/pseudonymize/commit/5dfb5e31a940e346708f753c9e198b628a94dc24"
        },
        "date": 1790272864922,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 604.8643188518215,
            "unit": "iter/sec",
            "range": "stddev: 0.00007822119254159415",
            "extra": "mean: 1.6532633333343938 msec\nrounds: 300"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 624.6294219182378,
            "unit": "iter/sec",
            "range": "stddev: 0.00002862514604784606",
            "extra": "mean: 1.6009492427189849 msec\nrounds: 618"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 365.3045657945247,
            "unit": "iter/sec",
            "range": "stddev: 0.00003595985480329234",
            "extra": "mean: 2.7374418324748686 msec\nrounds: 388"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 504.2713416475843,
            "unit": "iter/sec",
            "range": "stddev: 0.00002472139822047193",
            "extra": "mean: 1.9830593520003392 msec\nrounds: 500"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 430.1095822188248,
            "unit": "iter/sec",
            "range": "stddev: 0.000022533023431624014",
            "extra": "mean: 2.3249888896714577 msec\nrounds: 426"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 313.0824042642776,
            "unit": "iter/sec",
            "range": "stddev: 0.00010559628762622214",
            "extra": "mean: 3.1940472743906896 msec\nrounds: 328"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 289.1196839096517,
            "unit": "iter/sec",
            "range": "stddev: 0.00020452753198686984",
            "extra": "mean: 3.4587752258075044 msec\nrounds: 310"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 613.2575869056609,
            "unit": "iter/sec",
            "range": "stddev: 0.00006455696337660844",
            "extra": "mean: 1.6306361655397388 msec\nrounds: 592"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 64.6087534237214,
            "unit": "iter/sec",
            "range": "stddev: 0.0000984497072207291",
            "extra": "mean: 15.47777889230789 msec\nrounds: 65"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 145.05129970511612,
            "unit": "iter/sec",
            "range": "stddev: 0.00041331716429896605",
            "extra": "mean: 6.894112648648875 msec\nrounds: 148"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 498.6110715610868,
            "unit": "iter/sec",
            "range": "stddev: 0.000037393223854594325",
            "extra": "mean: 2.005571189723343 msec\nrounds: 506"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1815.0316650278687,
            "unit": "iter/sec",
            "range": "stddev: 0.000021248921882161633",
            "extra": "mean: 550.9545752110312 usec\nrounds: 1775"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 189.7905412595071,
            "unit": "iter/sec",
            "range": "stddev: 0.00020320384719027873",
            "extra": "mean: 5.268966479381423 msec\nrounds: 194"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 81.66268951003562,
            "unit": "iter/sec",
            "range": "stddev: 0.00013158627933304232",
            "extra": "mean: 12.245494313251939 msec\nrounds: 83"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 926.1318507037236,
            "unit": "iter/sec",
            "range": "stddev: 0.000016756322756097517",
            "extra": "mean: 1.0797598627454044 msec\nrounds: 918"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1177.710393686561,
            "unit": "iter/sec",
            "range": "stddev: 0.000015219784527218234",
            "extra": "mean: 849.1051835500253 usec\nrounds: 1155"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 120.84019111219003,
            "unit": "iter/sec",
            "range": "stddev: 0.00008378967440580092",
            "extra": "mean: 8.275392407080716 msec\nrounds: 113"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.805843505967538,
            "unit": "iter/sec",
            "range": "stddev: 0.0005905759122391512",
            "extra": "mean: 128.10915299999337 msec\nrounds: 8"
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
          "id": "830e15de482c80ec4ee6840e3edecee04fd06e5d",
          "message": "feat(benchmarks): implement 1.31.0 benchmark integrity and causal error atlas\n\n- benchmarks/evaluate_quality.py: instrument per-row sufficient statistics, exact boundary metrics, character-level masking recall, macro F1, and causal error categorization (missing_candidate, threshold_suppression, label_confusion, boundary_mismatch, conflict_loss) with --manifest support\n- benchmarks/compare_quality.py: deterministic artifact comparator with paired document-level bootstrap resampling (95% CI on delta F1/exact F1), per-entity shifts, and error category shifts\n- benchmarks/build_manifests.py: template-grouped partition builder preventing near-duplicate leakage across development, calibration, and test splits\n- tests/unit: unit test coverage for comparator, evaluator, and manifest builder",
          "timestamp": "2026-09-24T21:15:57+02:00",
          "tree_id": "07ee27459409091e44805ffef0767a8e4078b55e",
          "url": "https://github.com/ma2za/pseudonymize/commit/830e15de482c80ec4ee6840e3edecee04fd06e5d"
        },
        "date": 1790277412236,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 611.0304054343723,
            "unit": "iter/sec",
            "range": "stddev: 0.00001967091053986708",
            "extra": "mean: 1.6365797693637114 msec\nrounds: 581"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 630.243819235309,
            "unit": "iter/sec",
            "range": "stddev: 0.00002031555160979563",
            "extra": "mean: 1.5866875159733032 msec\nrounds: 626"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 343.83630384958303,
            "unit": "iter/sec",
            "range": "stddev: 0.00004926172653351434",
            "extra": "mean: 2.908360719342385 msec\nrounds: 367"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 517.3654220263863,
            "unit": "iter/sec",
            "range": "stddev: 0.000035384983690043855",
            "extra": "mean: 1.9328698003883966 msec\nrounds: 516"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 440.91104666186556,
            "unit": "iter/sec",
            "range": "stddev: 0.000021238249998778144",
            "extra": "mean: 2.268031176744137 msec\nrounds: 430"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 320.1224394938512,
            "unit": "iter/sec",
            "range": "stddev: 0.00005466795332402775",
            "extra": "mean: 3.1238047591450013 msec\nrounds: 328"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 295.162889198552,
            "unit": "iter/sec",
            "range": "stddev: 0.0000965469328902978",
            "extra": "mean: 3.387959789644537 msec\nrounds: 309"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 594.132440417019,
            "unit": "iter/sec",
            "range": "stddev: 0.00004872543862216178",
            "extra": "mean: 1.6831264074691905 msec\nrounds: 616"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 65.31416358139906,
            "unit": "iter/sec",
            "range": "stddev: 0.00030410444432801804",
            "extra": "mean: 15.310614806445932 msec\nrounds: 62"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 141.32120823965005,
            "unit": "iter/sec",
            "range": "stddev: 0.000053455534188970635",
            "extra": "mean: 7.076078760268009 msec\nrounds: 146"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 511.53354537163756,
            "unit": "iter/sec",
            "range": "stddev: 0.000024683296299373072",
            "extra": "mean: 1.9549060057703223 msec\nrounds: 520"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1837.4044350059692,
            "unit": "iter/sec",
            "range": "stddev: 0.000006998750206750061",
            "extra": "mean: 544.2459923074864 usec\nrounds: 1820"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 189.4846798453198,
            "unit": "iter/sec",
            "range": "stddev: 0.0000892193118684521",
            "extra": "mean: 5.277471512822674 msec\nrounds: 195"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 80.22648892710669,
            "unit": "iter/sec",
            "range": "stddev: 0.0001550474383214078",
            "extra": "mean: 12.464711012201894 msec\nrounds: 82"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 923.2546245586282,
            "unit": "iter/sec",
            "range": "stddev: 0.000013330588455592249",
            "extra": "mean: 1.083124821040632 msec\nrounds: 922"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1178.2227738187396,
            "unit": "iter/sec",
            "range": "stddev: 0.000007905461662838602",
            "extra": "mean: 848.7359285705355 usec\nrounds: 1148"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 121.04296367038944,
            "unit": "iter/sec",
            "range": "stddev: 0.000056820977754602754",
            "extra": "mean: 8.261529375000164 msec\nrounds: 112"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 7.779974381145606,
            "unit": "iter/sec",
            "range": "stddev: 0.0005314511882179172",
            "extra": "mean: 128.53512762502817 msec\nrounds: 8"
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
          "id": "c62a1fdfe2ec029439a3ca90b563cb4d37cee372",
          "message": "feat(benchmarks): implement contamination audit and development ablation runner\n\n- benchmarks/audit_contamination.py: audit pairwise row hash and template collisions across partitions and verify isolation from validation data\n- benchmarks/run_ablations.py: execute component ablations on identical development rows with paired statistical delta and error category reporting\n- tests/unit: unit tests for contamination auditor and ablation suite",
          "timestamp": "2026-09-24T23:28:11+02:00",
          "tree_id": "f8c95c77a9f527c731b88cb51ce4b4102c719f80",
          "url": "https://github.com/ma2za/pseudonymize/commit/c62a1fdfe2ec029439a3ca90b563cb4d37cee372"
        },
        "date": 1790285337786,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 632.6216215968234,
            "unit": "iter/sec",
            "range": "stddev: 0.00005362189240925481",
            "extra": "mean: 1.5807237151899163 msec\nrounds: 632"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 648.1000984906494,
            "unit": "iter/sec",
            "range": "stddev: 0.000033914728678501586",
            "extra": "mean: 1.5429715291339794 msec\nrounds: 635"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 460.694983682082,
            "unit": "iter/sec",
            "range": "stddev: 0.0000975176225123691",
            "extra": "mean: 2.1706335762711135 msec\nrounds: 472"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 594.7128275694739,
            "unit": "iter/sec",
            "range": "stddev: 0.00009835229283549143",
            "extra": "mean: 1.681483824868702 msec\nrounds: 571"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 550.4438619810105,
            "unit": "iter/sec",
            "range": "stddev: 0.00010670090994728482",
            "extra": "mean: 1.8167156890460494 msec\nrounds: 566"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 393.5593527247396,
            "unit": "iter/sec",
            "range": "stddev: 0.00010165543925960665",
            "extra": "mean: 2.540912807881897 msec\nrounds: 406"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 364.8848252867948,
            "unit": "iter/sec",
            "range": "stddev: 0.00006771945483816486",
            "extra": "mean: 2.7405908130435757 msec\nrounds: 230"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 669.1270996099695,
            "unit": "iter/sec",
            "range": "stddev: 0.00005171209167798391",
            "extra": "mean: 1.494484382089583 msec\nrounds: 670"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 77.21270579355671,
            "unit": "iter/sec",
            "range": "stddev: 0.00015402692645509066",
            "extra": "mean: 12.951236324675577 msec\nrounds: 77"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 168.21420819191925,
            "unit": "iter/sec",
            "range": "stddev: 0.000433750863918349",
            "extra": "mean: 5.944801041176487 msec\nrounds: 170"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 578.1290783840642,
            "unit": "iter/sec",
            "range": "stddev: 0.00004029890287806898",
            "extra": "mean: 1.7297175274336873 msec\nrounds: 565"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 2135.276744820214,
            "unit": "iter/sec",
            "range": "stddev: 0.000012812413966157608",
            "extra": "mean: 468.3233695237935 usec\nrounds: 2100"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 225.5319873062703,
            "unit": "iter/sec",
            "range": "stddev: 0.00008191348516703598",
            "extra": "mean: 4.43396084051709 msec\nrounds: 232"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 91.90037758086777,
            "unit": "iter/sec",
            "range": "stddev: 0.00012685838526568438",
            "extra": "mean: 10.8813481111114 msec\nrounds: 90"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 972.5816533465866,
            "unit": "iter/sec",
            "range": "stddev: 0.000027551356626597388",
            "extra": "mean: 1.0281913056441778 msec\nrounds: 939"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1280.242628279101,
            "unit": "iter/sec",
            "range": "stddev: 0.0000208301154076429",
            "extra": "mean: 781.1019395161038 usec\nrounds: 1240"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 140.11802352953663,
            "unit": "iter/sec",
            "range": "stddev: 0.00010955865027571326",
            "extra": "mean: 7.136840606299315 msec\nrounds: 127"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 9.03289828526568,
            "unit": "iter/sec",
            "range": "stddev: 0.0005196986115927611",
            "extra": "mean: 110.70643866666627 msec\nrounds: 9"
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
          "id": "6867b075b1dcc9b112f3017533a456d92ff0522e",
          "message": "feat(benchmarks): implement 1.32-1.34 calibration, constrained decoding, and quality gate",
          "timestamp": "2026-09-27T13:25:25+02:00",
          "tree_id": "3dcea4f78700237528fba3a0d059d4a7e2892299",
          "url": "https://github.com/ma2za/pseudonymize/commit/6867b075b1dcc9b112f3017533a456d92ff0522e"
        },
        "date": 1790508416659,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 836.7857576375495,
            "unit": "iter/sec",
            "range": "stddev: 0.000053719063576511885",
            "extra": "mean: 1.1950490204604391 msec\nrounds: 782"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 819.95427166658,
            "unit": "iter/sec",
            "range": "stddev: 0.00004821049680022251",
            "extra": "mean: 1.2195802065491679 msec\nrounds: 794"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 611.2569884189791,
            "unit": "iter/sec",
            "range": "stddev: 0.00009375377219295782",
            "extra": "mean: 1.635973115966343 msec\nrounds: 595"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 747.9792454607725,
            "unit": "iter/sec",
            "range": "stddev: 0.00006923305488036598",
            "extra": "mean: 1.336935491283554 msec\nrounds: 631"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 707.2875465946402,
            "unit": "iter/sec",
            "range": "stddev: 0.0000643087754377589",
            "extra": "mean: 1.4138521239553492 msec\nrounds: 718"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 459.94206037247375,
            "unit": "iter/sec",
            "range": "stddev: 0.0001405305011853066",
            "extra": "mean: 2.174186894736638 msec\nrounds: 437"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 408.35911752577306,
            "unit": "iter/sec",
            "range": "stddev: 0.00009051316311236508",
            "extra": "mean: 2.448824960879896 msec\nrounds: 409"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 928.5340356873146,
            "unit": "iter/sec",
            "range": "stddev: 0.00004236320141007132",
            "extra": "mean: 1.0769664455646857 msec\nrounds: 992"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 89.46715851237138,
            "unit": "iter/sec",
            "range": "stddev: 0.0002455391840775905",
            "extra": "mean: 11.177285795454445 msec\nrounds: 88"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 222.6388764299001,
            "unit": "iter/sec",
            "range": "stddev: 0.0001640918249262165",
            "extra": "mean: 4.491578542056015 msec\nrounds: 214"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 751.0711597009939,
            "unit": "iter/sec",
            "range": "stddev: 0.00005465149654159208",
            "extra": "mean: 1.331431765264567 msec\nrounds: 737"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 2510.3652865375457,
            "unit": "iter/sec",
            "range": "stddev: 0.000011720521419092698",
            "extra": "mean: 398.34840186914124 usec\nrounds: 2461"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 291.6537218089955,
            "unit": "iter/sec",
            "range": "stddev: 0.00019570469852813293",
            "extra": "mean: 3.4287236034481388 msec\nrounds: 290"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 110.77729371071487,
            "unit": "iter/sec",
            "range": "stddev: 0.00021236284113199856",
            "extra": "mean: 9.027120689655154 msec\nrounds: 116"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1297.1191899964006,
            "unit": "iter/sec",
            "range": "stddev: 0.00003694653096709692",
            "extra": "mean: 770.939176378059 usec\nrounds: 1270"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1771.680348285274,
            "unit": "iter/sec",
            "range": "stddev: 0.000043821223894064156",
            "extra": "mean: 564.4359045737867 usec\nrounds: 1771"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 163.88729807650327,
            "unit": "iter/sec",
            "range": "stddev: 0.0003534808053922047",
            "extra": "mean: 6.1017541428573425 msec\nrounds: 161"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 10.23512787070956,
            "unit": "iter/sec",
            "range": "stddev: 0.005332733775287178",
            "extra": "mean: 97.70273636363217 msec\nrounds: 11"
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
          "id": "5ff11c8e4453ef2292d741480a45998ec6f9adc2",
          "message": "chore(release): prepare 1.27.0 release and update changelog",
          "timestamp": "2026-09-27T13:49:21+02:00",
          "tree_id": "b6c1d09b8ed83003131519c1bcbefa0326e6c8ec",
          "url": "https://github.com/ma2za/pseudonymize/commit/5ff11c8e4453ef2292d741480a45998ec6f9adc2"
        },
        "date": 1790509806477,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 658.6404176560974,
            "unit": "iter/sec",
            "range": "stddev: 0.000023244962010246887",
            "extra": "mean: 1.5182791295418803 msec\nrounds: 633"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 666.6183909520562,
            "unit": "iter/sec",
            "range": "stddev: 0.00001650241024778542",
            "extra": "mean: 1.5001086282240315 msec\nrounds: 659"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 463.88626049416393,
            "unit": "iter/sec",
            "range": "stddev: 0.000022488536084619613",
            "extra": "mean: 2.1557008369567368 msec\nrounds: 460"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 587.8946391748359,
            "unit": "iter/sec",
            "range": "stddev: 0.00001787061357210873",
            "extra": "mean: 1.7009850632480539 msec\nrounds: 585"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 528.2590588703947,
            "unit": "iter/sec",
            "range": "stddev: 0.000025500005102830796",
            "extra": "mean: 1.8930106038093408 msec\nrounds: 525"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 349.59356459866285,
            "unit": "iter/sec",
            "range": "stddev: 0.000040591241032245396",
            "extra": "mean: 2.8604645544548584 msec\nrounds: 303"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 335.73973683986344,
            "unit": "iter/sec",
            "range": "stddev: 0.000025808904943122015",
            "extra": "mean: 2.9784975988021527 msec\nrounds: 334"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 722.0212802505984,
            "unit": "iter/sec",
            "range": "stddev: 0.00001556067370157668",
            "extra": "mean: 1.3850007296916802 msec\nrounds: 714"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 79.46696752755021,
            "unit": "iter/sec",
            "range": "stddev: 0.000045505366365558034",
            "extra": "mean: 12.583844974999359 msec\nrounds: 80"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 167.596331378114,
            "unit": "iter/sec",
            "range": "stddev: 0.00004592227012153961",
            "extra": "mean: 5.966717718563304 msec\nrounds: 167"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 598.6838782735388,
            "unit": "iter/sec",
            "range": "stddev: 0.00001766547388200907",
            "extra": "mean: 1.670330597315834 msec\nrounds: 596"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 1939.3779812874766,
            "unit": "iter/sec",
            "range": "stddev: 0.000013263438425565477",
            "extra": "mean: 515.6292428029627 usec\nrounds: 1841"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 229.01985961011934,
            "unit": "iter/sec",
            "range": "stddev: 0.00018844696402047645",
            "extra": "mean: 4.3664335560347824 msec\nrounds: 232"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 97.00473906952656,
            "unit": "iter/sec",
            "range": "stddev: 0.00002956883445286271",
            "extra": "mean: 10.308774701030497 msec\nrounds: 97"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1053.1999726174954,
            "unit": "iter/sec",
            "range": "stddev: 0.000014770177092318617",
            "extra": "mean: 949.487301556533 usec\nrounds: 1028"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1336.0620321573574,
            "unit": "iter/sec",
            "range": "stddev: 0.00001648127679810379",
            "extra": "mean: 748.4682416918072 usec\nrounds: 1324"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 136.2405549654013,
            "unit": "iter/sec",
            "range": "stddev: 0.00017516552657458997",
            "extra": "mean: 7.339958357142285 msec\nrounds: 126"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.648170775143903,
            "unit": "iter/sec",
            "range": "stddev: 0.00029412091289308636",
            "extra": "mean: 115.63138911111064 msec\nrounds: 9"
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
          "id": "e9903617652a2eeb94f30417654145bc6ac9f846",
          "message": "chore(release): bump development version to 1.28.0",
          "timestamp": "2026-09-27T14:06:15+02:00",
          "tree_id": "6c86542e9594c92d568dc2c62df865c0d66e1774",
          "url": "https://github.com/ma2za/pseudonymize/commit/e9903617652a2eeb94f30417654145bc6ac9f846"
        },
        "date": 1790510828740,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 897.7186959601172,
            "unit": "iter/sec",
            "range": "stddev: 0.00005979317145682736",
            "extra": "mean: 1.1139346930170504 msec\nrounds: 759"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 902.3858402434512,
            "unit": "iter/sec",
            "range": "stddev: 0.000025833195915175628",
            "extra": "mean: 1.1081734169612123 msec\nrounds: 849"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 679.3110429027502,
            "unit": "iter/sec",
            "range": "stddev: 0.000031369822309266514",
            "extra": "mean: 1.4720797055306512 msec\nrounds: 669"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 790.9137583040406,
            "unit": "iter/sec",
            "range": "stddev: 0.000030614372815556884",
            "extra": "mean: 1.2643603547171867 msec\nrounds: 795"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 743.0044026758532,
            "unit": "iter/sec",
            "range": "stddev: 0.000033443369522551126",
            "extra": "mean: 1.3458870450815688 msec\nrounds: 732"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 498.4349465637521,
            "unit": "iter/sec",
            "range": "stddev: 0.00007270075979135516",
            "extra": "mean: 2.006279870410522 msec\nrounds: 463"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 461.4721184236906,
            "unit": "iter/sec",
            "range": "stddev: 0.000032889627276375383",
            "extra": "mean: 2.1669781555077003 msec\nrounds: 463"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 997.7373331499906,
            "unit": "iter/sec",
            "range": "stddev: 0.00009165614473685407",
            "extra": "mean: 1.0022677981216417 msec\nrounds: 1065"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 100.19505205934995,
            "unit": "iter/sec",
            "range": "stddev: 0.00013895173966758194",
            "extra": "mean: 9.980532765307172 msec\nrounds: 98"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 250.83873433918026,
            "unit": "iter/sec",
            "range": "stddev: 0.00004059500318344409",
            "extra": "mean: 3.9866251224494516 msec\nrounds: 245"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 810.345058202739,
            "unit": "iter/sec",
            "range": "stddev: 0.000034289400976051966",
            "extra": "mean: 1.2340422019946613 msec\nrounds: 802"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 2787.858299043284,
            "unit": "iter/sec",
            "range": "stddev: 0.000007221681875204916",
            "extra": "mean: 358.6982883395373 usec\nrounds: 2667"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 318.83740931219387,
            "unit": "iter/sec",
            "range": "stddev: 0.00009543404235192212",
            "extra": "mean: 3.1363948231709435 msec\nrounds: 328"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 118.74214774711028,
            "unit": "iter/sec",
            "range": "stddev: 0.0005924157162059743",
            "extra": "mean: 8.421609504063701 msec\nrounds: 123"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1424.8436288036994,
            "unit": "iter/sec",
            "range": "stddev: 0.00002268831500362454",
            "extra": "mean: 701.83140085316 usec\nrounds: 1407"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1911.6421772236044,
            "unit": "iter/sec",
            "range": "stddev: 0.000030027097892347137",
            "extra": "mean: 523.1104502268105 usec\nrounds: 1979"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 182.80514890685873,
            "unit": "iter/sec",
            "range": "stddev: 0.00009978548415818047",
            "extra": "mean: 5.470305437126999 msec\nrounds: 167"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 11.546437873256387,
            "unit": "iter/sec",
            "range": "stddev: 0.004836132441998663",
            "extra": "mean: 86.60679691666455 msec\nrounds: 12"
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
          "id": "f2eedaeb91818ce203bd86a4b401f7e67e56975c",
          "message": "docs: reconcile roadmap milestone status and integrated commit history",
          "timestamp": "2026-09-27T14:07:55+02:00",
          "tree_id": "8e8adb703a5225c2096152ba387c319a34a73c7e",
          "url": "https://github.com/ma2za/pseudonymize/commit/f2eedaeb91818ce203bd86a4b401f7e67e56975c"
        },
        "date": 1790510920692,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 636.9038978312769,
            "unit": "iter/sec",
            "range": "stddev: 0.00005028706429177964",
            "extra": "mean: 1.570095588055125 msec\nrounds: 653"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 624.0834686676245,
            "unit": "iter/sec",
            "range": "stddev: 0.000024365889613292023",
            "extra": "mean: 1.6023497660255792 msec\nrounds: 624"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 459.71548331459144,
            "unit": "iter/sec",
            "range": "stddev: 0.00011234020910664888",
            "extra": "mean: 2.175258472457588 msec\nrounds: 472"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 552.8711021271873,
            "unit": "iter/sec",
            "range": "stddev: 0.0001285640452199661",
            "extra": "mean: 1.8087398602539932 msec\nrounds: 551"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 515.1322334183199,
            "unit": "iter/sec",
            "range": "stddev: 0.00014086001074519044",
            "extra": "mean: 1.9412491300810075 msec\nrounds: 369"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 347.18138040825335,
            "unit": "iter/sec",
            "range": "stddev: 0.0002043601252428739",
            "extra": "mean: 2.8803387981927258 msec\nrounds: 332"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 318.7426036158403,
            "unit": "iter/sec",
            "range": "stddev: 0.00008371047949287255",
            "extra": "mean: 3.1373277015871865 msec\nrounds: 315"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 726.6645914424829,
            "unit": "iter/sec",
            "range": "stddev: 0.00003982596060084855",
            "extra": "mean: 1.3761507190200724 msec\nrounds: 694"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 79.05251028805836,
            "unit": "iter/sec",
            "range": "stddev: 0.00028870299494649244",
            "extra": "mean: 12.64981967499974 msec\nrounds: 80"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 171.15707802435165,
            "unit": "iter/sec",
            "range": "stddev: 0.000059921792673448775",
            "extra": "mean: 5.842586304597485 msec\nrounds: 174"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 563.184001614821,
            "unit": "iter/sec",
            "range": "stddev: 0.00002751752811113998",
            "extra": "mean: 1.7756186204378919 msec\nrounds: 548"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 2043.9531499455927,
            "unit": "iter/sec",
            "range": "stddev: 0.000010665979364832634",
            "extra": "mean: 489.248004547765 usec\nrounds: 1979"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 220.75835562377313,
            "unit": "iter/sec",
            "range": "stddev: 0.00007784970902473014",
            "extra": "mean: 4.529839865741016 msec\nrounds: 216"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 98.98748444118945,
            "unit": "iter/sec",
            "range": "stddev: 0.00006457954921425305",
            "extra": "mean: 10.102287229999476 msec\nrounds: 100"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 978.4121391761068,
            "unit": "iter/sec",
            "range": "stddev: 0.00006630239707278634",
            "extra": "mean: 1.0220641792548402 msec\nrounds: 993"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1277.3967868216935,
            "unit": "iter/sec",
            "range": "stddev: 0.00004940951575325506",
            "extra": "mean: 782.8421132075275 usec\nrounds: 1007"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 132.4633759856386,
            "unit": "iter/sec",
            "range": "stddev: 0.00019330442633366747",
            "extra": "mean: 7.549256483606592 msec\nrounds: 122"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 8.567943939668694,
            "unit": "iter/sec",
            "range": "stddev: 0.0005517002467430037",
            "extra": "mean: 116.71411566666576 msec\nrounds: 9"
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
          "id": "96e44ae255d8c564f7a4e95f8d9df5bc16c23040",
          "message": "perf(engine): optimize detector pre-filters, bloom hashing, alias memoization, and local processing path",
          "timestamp": "2026-09-27T15:55:47+02:00",
          "tree_id": "14e7eef972f954169725d39bc8ceef870d6f6489",
          "url": "https://github.com/ma2za/pseudonymize/commit/96e44ae255d8c564f7a4e95f8d9df5bc16c23040"
        },
        "date": 1790517424130,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1040857.722502401,
            "unit": "iter/sec",
            "range": "stddev: 1.7833549640081884e-7",
            "extra": "mean: 960.7461023547271 nsec\nrounds: 195695"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 644.0253702506947,
            "unit": "iter/sec",
            "range": "stddev: 0.000015342891256744547",
            "extra": "mean: 1.552733861417195 msec\nrounds: 635"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2603.363599532211,
            "unit": "iter/sec",
            "range": "stddev: 0.0000092434456136566",
            "extra": "mean: 384.11845359583515 usec\nrounds: 2489"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2600.8998110696275,
            "unit": "iter/sec",
            "range": "stddev: 0.000009396653151220363",
            "extra": "mean: 384.4823225192774 usec\nrounds: 2620"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 431.5075762298211,
            "unit": "iter/sec",
            "range": "stddev: 0.00004425195484748734",
            "extra": "mean: 2.317456413482297 msec\nrounds: 445"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2597.2157547179513,
            "unit": "iter/sec",
            "range": "stddev: 0.000017949201497007434",
            "extra": "mean: 385.02769674928163 usec\nrounds: 2615"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2602.2193603882183,
            "unit": "iter/sec",
            "range": "stddev: 0.000010150167291019438",
            "extra": "mean: 384.2873568701804 usec\nrounds: 2620"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2604.378317399079,
            "unit": "iter/sec",
            "range": "stddev: 0.000008474455329665225",
            "extra": "mean: 383.9687933658857 usec\nrounds: 2623"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2602.339009727211,
            "unit": "iter/sec",
            "range": "stddev: 0.0000088922995403531",
            "extra": "mean: 384.2696882543465 usec\nrounds: 2486"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2586.0874149319648,
            "unit": "iter/sec",
            "range": "stddev: 0.000014244458573756297",
            "extra": "mean: 386.6845313217334 usec\nrounds: 2618"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2586.5837152853064,
            "unit": "iter/sec",
            "range": "stddev: 0.000011447965369012526",
            "extra": "mean: 386.6103362866404 usec\nrounds: 2483"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16165.076819146147,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022291541068117917",
            "extra": "mean: 61.861753654989485 usec\nrounds: 16006"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4927.34534253229,
            "unit": "iter/sec",
            "range": "stddev: 0.0000039405710460982205",
            "extra": "mean: 202.94903857623143 usec\nrounds: 5029"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2601.2373623926433,
            "unit": "iter/sec",
            "range": "stddev: 0.000011241602803287502",
            "extra": "mean: 384.4324299110445 usec\nrounds: 2240"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1193.3867174988263,
            "unit": "iter/sec",
            "range": "stddev: 0.000016066768363560492",
            "extra": "mean: 837.9513407823591 usec\nrounds: 1253"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1260.2425260564544,
            "unit": "iter/sec",
            "range": "stddev: 0.000031924089661090904",
            "extra": "mean: 793.4980603528718 usec\nrounds: 1077"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 175.05237359011602,
            "unit": "iter/sec",
            "range": "stddev: 0.000060978777571767565",
            "extra": "mean: 5.712576067900076 msec\nrounds: 162"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 11.437970455519833,
            "unit": "iter/sec",
            "range": "stddev: 0.0010659187850128801",
            "extra": "mean: 87.42809783333645 msec\nrounds: 12"
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
          "id": "a7eef99528ce367df5c5b185147bad1b1fd15bed",
          "message": "feat(accuracy): improve tax id disambiguation, location precision, and multilingual person recall",
          "timestamp": "2026-09-27T18:13:52+02:00",
          "tree_id": "75b4d66663d217e393bc5a2c2f96468b7535d564",
          "url": "https://github.com/ma2za/pseudonymize/commit/a7eef99528ce367df5c5b185147bad1b1fd15bed"
        },
        "date": 1790525710253,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1064584.5461053182,
            "unit": "iter/sec",
            "range": "stddev: 9.883330782335946e-8",
            "extra": "mean: 939.3335678771641 nsec\nrounds: 99911"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 650.8790195914976,
            "unit": "iter/sec",
            "range": "stddev: 0.000025775581427002315",
            "extra": "mean: 1.5363838284841576 msec\nrounds: 653"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2605.2757494213524,
            "unit": "iter/sec",
            "range": "stddev: 0.000007739581438180307",
            "extra": "mean: 383.8365287137479 usec\nrounds: 2612"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2603.3218736599774,
            "unit": "iter/sec",
            "range": "stddev: 0.000008818616952627116",
            "extra": "mean: 384.12461022121425 usec\nrounds: 2622"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 431.45567004180043,
            "unit": "iter/sec",
            "range": "stddev: 0.00004014637028339463",
            "extra": "mean: 2.31773521461224 msec\nrounds: 438"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2603.7081435211603,
            "unit": "iter/sec",
            "range": "stddev: 0.000009009065991209557",
            "extra": "mean: 384.06762389567837 usec\nrounds: 2603"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2604.002977737505,
            "unit": "iter/sec",
            "range": "stddev: 0.000008201971813640096",
            "extra": "mean: 384.0241384319971 usec\nrounds: 2615"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2606.5486986196106,
            "unit": "iter/sec",
            "range": "stddev: 0.000007121059866821027",
            "extra": "mean: 383.64907608654505 usec\nrounds: 2484"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2600.1286945888173,
            "unit": "iter/sec",
            "range": "stddev: 0.000010445355116423083",
            "extra": "mean: 384.596347896595 usec\nrounds: 2472"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2596.337616662935,
            "unit": "iter/sec",
            "range": "stddev: 0.000012867266780511613",
            "extra": "mean: 385.157921520737 usec\nrounds: 2472"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2603.6197507853135,
            "unit": "iter/sec",
            "range": "stddev: 0.000008378123835049897",
            "extra": "mean: 384.0806629686905 usec\nrounds: 2614"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16160.325378543306,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024642241164168167",
            "extra": "mean: 61.879942177880835 usec\nrounds: 16032"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4923.9613199389505,
            "unit": "iter/sec",
            "range": "stddev: 0.000004078748310283097",
            "extra": "mean: 203.08851654675436 usec\nrounds: 5016"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2604.1485831952887,
            "unit": "iter/sec",
            "range": "stddev: 0.000008141460233720331",
            "extra": "mean: 384.00266653487205 usec\nrounds: 2531"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1195.2714860799779,
            "unit": "iter/sec",
            "range": "stddev: 0.0000056058981287086845",
            "extra": "mean: 836.630013888818 usec\nrounds: 1224"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1261.221322585723,
            "unit": "iter/sec",
            "range": "stddev: 0.000011479712949144427",
            "extra": "mean: 792.882250000203 usec\nrounds: 1244"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 165.5793015926189,
            "unit": "iter/sec",
            "range": "stddev: 0.0003956988878990091",
            "extra": "mean: 6.039402210188919 msec\nrounds: 157"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 11.061024045735222,
            "unit": "iter/sec",
            "range": "stddev: 0.001138605900730574",
            "extra": "mean: 90.40754236363568 msec\nrounds: 11"
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
          "id": "5e4d78f89b173e2121136c07cb3f10401766b192",
          "message": "fix(accuracy): preserve address numbers with contextual validation and calibrate gazetteer sub-part confidence",
          "timestamp": "2026-09-27T19:04:53+02:00",
          "tree_id": "3828ee6e5c24df7fbbe93ae0df73c734275916ad",
          "url": "https://github.com/ma2za/pseudonymize/commit/5e4d78f89b173e2121136c07cb3f10401766b192"
        },
        "date": 1790528768476,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1221955.8236894587,
            "unit": "iter/sec",
            "range": "stddev: 1.2767003887526536e-7",
            "extra": "mean: 818.3601899622639 nsec\nrounds: 164528"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 805.6236572179467,
            "unit": "iter/sec",
            "range": "stddev: 0.000050375600646474484",
            "extra": "mean: 1.241274373015921 msec\nrounds: 756"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 3794.3678940263803,
            "unit": "iter/sec",
            "range": "stddev: 0.000016786630589658495",
            "extra": "mean: 263.5485087184979 usec\nrounds: 3613"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 4089.967029571863,
            "unit": "iter/sec",
            "range": "stddev: 0.000013228765612421726",
            "extra": "mean: 244.50074848272797 usec\nrounds: 4119"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 647.5794507606846,
            "unit": "iter/sec",
            "range": "stddev: 0.00009776364532547004",
            "extra": "mean: 1.5442120635936514 msec\nrounds: 629"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 3937.982039141154,
            "unit": "iter/sec",
            "range": "stddev: 0.000017915389935742363",
            "extra": "mean: 253.9371663102082 usec\nrounds: 3740"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 4100.036857519693,
            "unit": "iter/sec",
            "range": "stddev: 0.00001166489058057703",
            "extra": "mean: 243.900246449235 usec\nrounds: 4013"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 3855.169826764514,
            "unit": "iter/sec",
            "range": "stddev: 0.00001897323303876739",
            "extra": "mean: 259.3919450856615 usec\nrounds: 3551"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 4038.303574915051,
            "unit": "iter/sec",
            "range": "stddev: 0.000014664415186737277",
            "extra": "mean: 247.62873356321063 usec\nrounds: 4061"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 4150.447225134884,
            "unit": "iter/sec",
            "range": "stddev: 0.000006893822904002976",
            "extra": "mean: 240.93789072754714 usec\nrounds: 4109"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 4161.143989663767,
            "unit": "iter/sec",
            "range": "stddev: 0.000007138133726091534",
            "extra": "mean: 240.3185283864217 usec\nrounds: 4016"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 22059.8234526451,
            "unit": "iter/sec",
            "range": "stddev: 0.000002825508238863433",
            "extra": "mean: 45.331278473132755 usec\nrounds: 22530"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 7574.72061074253,
            "unit": "iter/sec",
            "range": "stddev: 0.0000033802943664502714",
            "extra": "mean: 132.01807055190815 usec\nrounds: 7413"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 3885.0571712200285,
            "unit": "iter/sec",
            "range": "stddev: 0.000013906813571996949",
            "extra": "mean: 257.39646958296083 usec\nrounds: 3978"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1717.4423775837972,
            "unit": "iter/sec",
            "range": "stddev: 0.00001853204742127755",
            "extra": "mean: 582.2611652373811 usec\nrounds: 1749"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1763.8568186228697,
            "unit": "iter/sec",
            "range": "stddev: 0.00004070432693980387",
            "extra": "mean: 566.9394417063567 usec\nrounds: 1664"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 250.7461070636621,
            "unit": "iter/sec",
            "range": "stddev: 0.00014222550723601537",
            "extra": "mean: 3.9880978082188507 msec\nrounds: 219"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 15.639660501680241,
            "unit": "iter/sec",
            "range": "stddev: 0.005991596693199776",
            "extra": "mean: 63.94000687499357 msec\nrounds: 16"
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
          "id": "65eb8649e6057022154f63e1541e66a4aaccd270",
          "message": "docs(handover): document 1.28.0 performance and contextual precision enhancements",
          "timestamp": "2026-09-27T19:25:42+02:00",
          "tree_id": "bd97afc445ca1d6a9879c84a5ea5db8d2276f95e",
          "url": "https://github.com/ma2za/pseudonymize/commit/65eb8649e6057022154f63e1541e66a4aaccd270"
        },
        "date": 1790529991397,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1059742.9727661144,
            "unit": "iter/sec",
            "range": "stddev: 1.274240600820619e-7",
            "extra": "mean: 943.62503521946 nsec\nrounds: 175132"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 647.058972639858,
            "unit": "iter/sec",
            "range": "stddev: 0.00003866988266730613",
            "extra": "mean: 1.5454541893148015 msec\nrounds: 655"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2604.402274973535,
            "unit": "iter/sec",
            "range": "stddev: 0.000013452864018618412",
            "extra": "mean: 383.96526128443867 usec\nrounds: 2614"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2602.420146270211,
            "unit": "iter/sec",
            "range": "stddev: 0.000013786069850578141",
            "extra": "mean: 384.2577077468449 usec\nrounds: 2621"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 434.3950003691157,
            "unit": "iter/sec",
            "range": "stddev: 0.00015995479824883923",
            "extra": "mean: 2.302052277651162 msec\nrounds: 443"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2563.1653666906022,
            "unit": "iter/sec",
            "range": "stddev: 0.00004742723077944939",
            "extra": "mean: 390.14259984760054 usec\nrounds: 2619"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2606.5239776183703,
            "unit": "iter/sec",
            "range": "stddev: 0.000009175301269083368",
            "extra": "mean: 383.6527147215115 usec\nrounds: 2622"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2606.3185534642353,
            "unit": "iter/sec",
            "range": "stddev: 0.000010012656999294415",
            "extra": "mean: 383.68295336379043 usec\nrounds: 2616"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2606.6922845983954,
            "unit": "iter/sec",
            "range": "stddev: 0.000008362860460648893",
            "extra": "mean: 383.6279433167029 usec\nrounds: 2611"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2604.337700014602,
            "unit": "iter/sec",
            "range": "stddev: 0.000010048263366342714",
            "extra": "mean: 383.97478176290014 usec\nrounds: 2621"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2608.131474047972,
            "unit": "iter/sec",
            "range": "stddev: 0.000009146231550135413",
            "extra": "mean: 383.41625410775083 usec\nrounds: 2495"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16163.717206794605,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024741964374423944",
            "extra": "mean: 61.86695716129199 usec\nrounds: 16037"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4923.869640087986,
            "unit": "iter/sec",
            "range": "stddev: 0.0000040399117956121005",
            "extra": "mean: 203.0922979476221 usec\nrounds: 5021"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2604.948950716277,
            "unit": "iter/sec",
            "range": "stddev: 0.000008697285710154945",
            "extra": "mean: 383.8846821643212 usec\nrounds: 2108"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1196.105406915709,
            "unit": "iter/sec",
            "range": "stddev: 0.000004764378246744799",
            "extra": "mean: 836.0467181388399 usec\nrounds: 1224"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1264.3521007122697,
            "unit": "iter/sec",
            "range": "stddev: 0.000051105367328097064",
            "extra": "mean: 790.9189215857294 usec\nrounds: 1135"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 169.05470620371656,
            "unit": "iter/sec",
            "range": "stddev: 0.00007662202114798259",
            "extra": "mean: 5.915244966886439 msec\nrounds: 151"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 11.052805774339463,
            "unit": "iter/sec",
            "range": "stddev: 0.0010866654811467363",
            "extra": "mean: 90.47476454545424 msec\nrounds: 11"
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
          "id": "4e2f9fc47e0d859bac10d47a6fa1f48b20d29a9d",
          "message": "docs(changelog): document unreleased performance and contextual precision enhancements",
          "timestamp": "2026-09-27T19:59:09+02:00",
          "tree_id": "dc65c1ff4059b1ceb33c72a344f7064bb7bd63d4",
          "url": "https://github.com/ma2za/pseudonymize/commit/4e2f9fc47e0d859bac10d47a6fa1f48b20d29a9d"
        },
        "date": 1790531995086,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1042733.2134735776,
            "unit": "iter/sec",
            "range": "stddev: 1.6552896526718098e-7",
            "extra": "mean: 959.0180758401051 nsec\nrounds: 196851"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 651.4383158871179,
            "unit": "iter/sec",
            "range": "stddev: 0.000020531011002404097",
            "extra": "mean: 1.5350647568806517 msec\nrounds: 654"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2598.13170643459,
            "unit": "iter/sec",
            "range": "stddev: 0.000008665552648297223",
            "extra": "mean: 384.8919581418363 usec\nrounds: 2604"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2597.844229246357,
            "unit": "iter/sec",
            "range": "stddev: 0.00001002290729290433",
            "extra": "mean: 384.93455024826613 usec\nrounds: 2617"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 440.9962256806062,
            "unit": "iter/sec",
            "range": "stddev: 0.000030248632723215932",
            "extra": "mean: 2.2675931034481356 msec\nrounds: 435"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2598.1028342569643,
            "unit": "iter/sec",
            "range": "stddev: 0.000008904903162613565",
            "extra": "mean: 384.89623536629244 usec\nrounds: 2460"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2592.4235642461244,
            "unit": "iter/sec",
            "range": "stddev: 0.000015162132208023802",
            "extra": "mean: 385.7394346323956 usec\nrounds: 2616"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2593.8153530680206,
            "unit": "iter/sec",
            "range": "stddev: 0.000011184514306038592",
            "extra": "mean: 385.5324546588015 usec\nrounds: 2415"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2577.5320329478755,
            "unit": "iter/sec",
            "range": "stddev: 0.000014879079695893625",
            "extra": "mean: 387.9680202679455 usec\nrounds: 2467"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2580.2809094417344,
            "unit": "iter/sec",
            "range": "stddev: 0.000012825841063834663",
            "extra": "mean: 387.5547024127534 usec\nrounds: 2611"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2598.878234348159,
            "unit": "iter/sec",
            "range": "stddev: 0.000009963850643953635",
            "extra": "mean: 384.7813979060148 usec\nrounds: 2483"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16159.198809203277,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022906275241531004",
            "extra": "mean: 61.88425625597613 usec\nrounds: 15945"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4929.736390761745,
            "unit": "iter/sec",
            "range": "stddev: 0.000004073868444491086",
            "extra": "mean: 202.85060310202095 usec\nrounds: 5029"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2595.1472400426396,
            "unit": "iter/sec",
            "range": "stddev: 0.000009310708260459884",
            "extra": "mean: 385.3345908741461 usec\nrounds: 2608"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1195.1505831838513,
            "unit": "iter/sec",
            "range": "stddev: 0.000004591929227289124",
            "extra": "mean: 836.7146484052453 usec\nrounds: 1223"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1265.5457306279513,
            "unit": "iter/sec",
            "range": "stddev: 0.00002399792206330957",
            "extra": "mean: 790.172947368571 usec\nrounds: 1121"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 169.14775594934372,
            "unit": "iter/sec",
            "range": "stddev: 0.00005794265376031086",
            "extra": "mean: 5.911990935897958 msec\nrounds: 156"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 10.933415173590117,
            "unit": "iter/sec",
            "range": "stddev: 0.0008712731791421366",
            "extra": "mean: 91.4627300000022 msec\nrounds: 11"
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
          "id": "355c9359c9b177f47cd3fff3ce3088b85135a3aa",
          "message": "chore(release): prepare 1.28.0 release and update changelog",
          "timestamp": "2026-09-27T20:03:50+02:00",
          "tree_id": "9171908075af1677fe417ea31f34cf1de8be3d55",
          "url": "https://github.com/ma2za/pseudonymize/commit/355c9359c9b177f47cd3fff3ce3088b85135a3aa"
        },
        "date": 1790532275096,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1037810.2003146491,
            "unit": "iter/sec",
            "range": "stddev: 4.396212670802839e-7",
            "extra": "mean: 963.5673263731793 nsec\nrounds: 173914"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 655.8626801488908,
            "unit": "iter/sec",
            "range": "stddev: 0.00003802410912388586",
            "extra": "mean: 1.5247094098615046 msec\nrounds: 649"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2606.775465945815,
            "unit": "iter/sec",
            "range": "stddev: 0.0000071914650816689624",
            "extra": "mean: 383.61570187525547 usec\nrounds: 2613"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2607.082580986247,
            "unit": "iter/sec",
            "range": "stddev: 0.000008179482477979509",
            "extra": "mean: 383.57051184075056 usec\nrounds: 2618"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 445.85770674210943,
            "unit": "iter/sec",
            "range": "stddev: 0.00008423188772185315",
            "extra": "mean: 2.2428680381169555 msec\nrounds: 446"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2605.9217412575254,
            "unit": "iter/sec",
            "range": "stddev: 0.000009243270662736152",
            "extra": "mean: 383.7413780190634 usec\nrounds: 2484"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2595.293295982263,
            "unit": "iter/sec",
            "range": "stddev: 0.000023243300215512387",
            "extra": "mean: 385.31290530749874 usec\nrounds: 2619"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2605.3044544176187,
            "unit": "iter/sec",
            "range": "stddev: 0.000010481448719347253",
            "extra": "mean: 383.83229963944336 usec\nrounds: 2493"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2580.0624784639945,
            "unit": "iter/sec",
            "range": "stddev: 0.00003481603222397574",
            "extra": "mean: 387.58751322771707 usec\nrounds: 2457"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2599.159282739105,
            "unit": "iter/sec",
            "range": "stddev: 0.000012398023530217221",
            "extra": "mean: 384.7397913013462 usec\nrounds: 2621"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2606.037601897204,
            "unit": "iter/sec",
            "range": "stddev: 0.000010192407687620056",
            "extra": "mean: 383.72431743578716 usec\nrounds: 2621"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16163.33618122888,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025198375798618637",
            "extra": "mean: 61.868415578792415 usec\nrounds: 16009"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4928.882553757089,
            "unit": "iter/sec",
            "range": "stddev: 0.000004283533485893094",
            "extra": "mean: 202.88574318690962 usec\nrounds: 5027"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2600.280492706646,
            "unit": "iter/sec",
            "range": "stddev: 0.000013171042160293123",
            "extra": "mean: 384.5738960873004 usec\nrounds: 2300"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1195.717172995014,
            "unit": "iter/sec",
            "range": "stddev: 0.000006673132631877044",
            "extra": "mean: 836.318171708796 usec\nrounds: 1223"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1266.4085746780354,
            "unit": "iter/sec",
            "range": "stddev: 0.000027277236376309375",
            "extra": "mean: 789.6345776513984 usec\nrounds: 1056"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 168.85759830686206,
            "unit": "iter/sec",
            "range": "stddev: 0.00007277608085030491",
            "extra": "mean: 5.922149847131646 msec\nrounds: 157"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 11.053160684758627,
            "unit": "iter/sec",
            "range": "stddev: 0.0009861831237216966",
            "extra": "mean: 90.47185945454638 msec\nrounds: 11"
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
          "id": "2e513f9f689260252adcd5fad58312af5fbc6e5d",
          "message": "chore(release): bump development version to 1.29.0",
          "timestamp": "2026-09-27T20:08:26+02:00",
          "tree_id": "8ba27a478963a0ce22960496cfe491aaba874ad7",
          "url": "https://github.com/ma2za/pseudonymize/commit/2e513f9f689260252adcd5fad58312af5fbc6e5d"
        },
        "date": 1790532554380,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1051946.5860028528,
            "unit": "iter/sec",
            "range": "stddev: 1.5020849831656032e-7",
            "extra": "mean: 950.6186086878827 nsec\nrounds: 175101"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 638.2977945535714,
            "unit": "iter/sec",
            "range": "stddev: 0.000057868843525505795",
            "extra": "mean: 1.5666668575902019 msec\nrounds: 639"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2604.237395762803,
            "unit": "iter/sec",
            "range": "stddev: 0.000008046176311921391",
            "extra": "mean: 383.9895708536555 usec\nrounds: 2484"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2603.4254300190346,
            "unit": "iter/sec",
            "range": "stddev: 0.00000826084543937603",
            "extra": "mean: 384.10933091050305 usec\nrounds: 2614"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 426.3085261283693,
            "unit": "iter/sec",
            "range": "stddev: 0.00004897002381731102",
            "extra": "mean: 2.3457189774780196 msec\nrounds: 444"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2588.3609697462034,
            "unit": "iter/sec",
            "range": "stddev: 0.000020313525683964956",
            "extra": "mean: 386.34487681138734 usec\nrounds: 2484"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2586.4845608195724,
            "unit": "iter/sec",
            "range": "stddev: 0.00002135854645424949",
            "extra": "mean: 386.6251572300639 usec\nrounds: 2455"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2593.182046603724,
            "unit": "iter/sec",
            "range": "stddev: 0.00001701110032082216",
            "extra": "mean: 385.6266093272142 usec\nrounds: 2616"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2601.8215954375232,
            "unit": "iter/sec",
            "range": "stddev: 0.000009026742096306719",
            "extra": "mean: 384.34610649460757 usec\nrounds: 2479"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2572.100213187647,
            "unit": "iter/sec",
            "range": "stddev: 0.000033908066557225986",
            "extra": "mean: 388.7873399616429 usec\nrounds: 2615"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2600.089423189829,
            "unit": "iter/sec",
            "range": "stddev: 0.000010217965242245194",
            "extra": "mean: 384.60215678781725 usec\nrounds: 2615"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16155.934079913874,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023780551273929052",
            "extra": "mean: 61.89676158949338 usec\nrounds: 16006"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4922.827533637928,
            "unit": "iter/sec",
            "range": "stddev: 0.000004161005820903588",
            "extra": "mean: 203.1352902710789 usec\nrounds: 5016"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2601.441494996125,
            "unit": "iter/sec",
            "range": "stddev: 0.000009176445746439457",
            "extra": "mean: 384.4022638692821 usec\nrounds: 2145"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1195.171848616898,
            "unit": "iter/sec",
            "range": "stddev: 0.0000056212126939698475",
            "extra": "mean: 836.6997609232859 usec\nrounds: 1213"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1263.4769542505833,
            "unit": "iter/sec",
            "range": "stddev: 0.000011543913536868857",
            "extra": "mean: 791.4667510442551 usec\nrounds: 1197"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 167.62657846580427,
            "unit": "iter/sec",
            "range": "stddev: 0.00009702655624402488",
            "extra": "mean: 5.965641064516504 msec\nrounds: 155"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 10.922530098446895,
            "unit": "iter/sec",
            "range": "stddev: 0.000947473120621517",
            "extra": "mean: 91.55387909090703 msec\nrounds: 11"
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
          "id": "6c8e01714ef07d154b4d8855443f59261ca00032",
          "message": "feat(recall): reduce false negatives via area-code phone support, contextual word skipping, and international postal formats",
          "timestamp": "2026-09-27T23:39:22+02:00",
          "tree_id": "71161ff9340c90bd8bd71b08996104fdb598c9c2",
          "url": "https://github.com/ma2za/pseudonymize/commit/6c8e01714ef07d154b4d8855443f59261ca00032"
        },
        "date": 1790545204726,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1769468.3044691286,
            "unit": "iter/sec",
            "range": "stddev: 6.518427157563965e-8",
            "extra": "mean: 565.141515942563 nsec\nrounds: 137723"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 1191.2471219641416,
            "unit": "iter/sec",
            "range": "stddev: 0.00005400969758959332",
            "extra": "mean: 839.4563827790735 usec\nrounds: 1173"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 5635.005960780123,
            "unit": "iter/sec",
            "range": "stddev: 0.000010680031591557433",
            "extra": "mean: 177.46210154169168 usec\nrounds: 5643"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 5290.983221534647,
            "unit": "iter/sec",
            "range": "stddev: 0.00004254194549622124",
            "extra": "mean: 189.00078834684916 usec\nrounds: 5698"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 735.1868612850134,
            "unit": "iter/sec",
            "range": "stddev: 0.00010289575354807589",
            "extra": "mean: 1.3601984103090836 msec\nrounds: 485"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 5544.096331282542,
            "unit": "iter/sec",
            "range": "stddev: 0.000021553005488417177",
            "extra": "mean: 180.37204627154546 usec\nrounds: 3004"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 5408.952768897942,
            "unit": "iter/sec",
            "range": "stddev: 0.00003188623645961632",
            "extra": "mean: 184.87867110803907 usec\nrounds: 5704"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 5497.275411060629,
            "unit": "iter/sec",
            "range": "stddev: 0.000027183052251748088",
            "extra": "mean: 181.9082955145343 usec\nrounds: 5685"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 5535.522361435493,
            "unit": "iter/sec",
            "range": "stddev: 0.000024905367958553756",
            "extra": "mean: 180.65142450994927 usec\nrounds: 5663"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 5611.700182979523,
            "unit": "iter/sec",
            "range": "stddev: 0.000013322480364598541",
            "extra": "mean: 178.19911388584762 usec\nrounds: 5646"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 5583.649060613093,
            "unit": "iter/sec",
            "range": "stddev: 0.000016674963067802556",
            "extra": "mean: 179.09435015426965 usec\nrounds: 4538"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 21196.232279273103,
            "unit": "iter/sec",
            "range": "stddev: 0.000002712395591095865",
            "extra": "mean: 47.17819595597929 usec\nrounds: 20969"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 7152.788295433031,
            "unit": "iter/sec",
            "range": "stddev: 0.000002606773384175153",
            "extra": "mean: 139.8056196684149 usec\nrounds: 7057"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 5240.527968282052,
            "unit": "iter/sec",
            "range": "stddev: 0.00004592048119632482",
            "extra": "mean: 190.82046810024366 usec\nrounds: 5627"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1710.1370070084386,
            "unit": "iter/sec",
            "range": "stddev: 0.000018135595539503195",
            "extra": "mean: 584.7484709715222 usec\nrounds: 1688"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 2540.6612897306627,
            "unit": "iter/sec",
            "range": "stddev: 0.000013440376190953693",
            "extra": "mean: 393.59831396730993 usec\nrounds: 2513"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 311.20754505824027,
            "unit": "iter/sec",
            "range": "stddev: 0.00006812079817016743",
            "extra": "mean: 3.2132897028986145 msec\nrounds: 276"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 19.827213723629814,
            "unit": "iter/sec",
            "range": "stddev: 0.004800130448918663",
            "extra": "mean: 50.43573009999953 msec\nrounds: 20"
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
          "id": "0d3d9fbfbb7f45a7e3a56006bcd9946d44afebd2",
          "message": "chore(release): prepare 1.29.0 release and update changelog",
          "timestamp": "2026-09-28T20:07:00+02:00",
          "tree_id": "023552ec354ae00fc8ec5feca5c47a43d470c8bb",
          "url": "https://github.com/ma2za/pseudonymize/commit/0d3d9fbfbb7f45a7e3a56006bcd9946d44afebd2"
        },
        "date": 1790618886258,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1232344.0628076312,
            "unit": "iter/sec",
            "range": "stddev: 7.922738634465973e-8",
            "extra": "mean: 811.4616933534899 nsec\nrounds: 119290"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 897.0474996120664,
            "unit": "iter/sec",
            "range": "stddev: 0.00003699885060587601",
            "extra": "mean: 1.1147681705065295 msec\nrounds: 868"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 3363.986899713679,
            "unit": "iter/sec",
            "range": "stddev: 0.000035094733966352817",
            "extra": "mean: 297.2663181551371 usec\nrounds: 3426"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 3420.4595350707373,
            "unit": "iter/sec",
            "range": "stddev: 0.000009469472844971784",
            "extra": "mean: 292.358377506524 usec\nrounds: 3441"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 627.850208940194,
            "unit": "iter/sec",
            "range": "stddev: 0.00002725324909370161",
            "extra": "mean: 1.5927365886968357 msec\nrounds: 637"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 3424.622743213167,
            "unit": "iter/sec",
            "range": "stddev: 0.0000085890994757648",
            "extra": "mean: 292.0029664528087 usec\nrounds: 3428"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 3392.972765986058,
            "unit": "iter/sec",
            "range": "stddev: 0.00002059012368521471",
            "extra": "mean: 294.7267982887514 usec\nrounds: 3272"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 3387.426741775932,
            "unit": "iter/sec",
            "range": "stddev: 0.000027881623130318242",
            "extra": "mean: 295.2093362396166 usec\nrounds: 3441"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 3425.7162572719717,
            "unit": "iter/sec",
            "range": "stddev: 0.000008286307960542053",
            "extra": "mean: 291.90975693834554 usec\nrounds: 3423"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 3425.4781826786057,
            "unit": "iter/sec",
            "range": "stddev: 0.000007548002296287527",
            "extra": "mean: 291.9300449953631 usec\nrounds: 3267"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 3405.4185939576028,
            "unit": "iter/sec",
            "range": "stddev: 0.000020400453944476323",
            "extra": "mean: 293.6496563959414 usec\nrounds: 3213"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 17545.620540868633,
            "unit": "iter/sec",
            "range": "stddev: 0.000001859633586343347",
            "extra": "mean: 56.994279436895475 usec\nrounds: 17546"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 5849.664576616265,
            "unit": "iter/sec",
            "range": "stddev: 0.000004210890905082037",
            "extra": "mean: 170.94997275526686 usec\nrounds: 5836"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 3426.6695376539924,
            "unit": "iter/sec",
            "range": "stddev: 0.000007062414501603419",
            "extra": "mean: 291.82854926963046 usec\nrounds: 3217"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1418.2985431686577,
            "unit": "iter/sec",
            "range": "stddev: 0.000007319338571543837",
            "extra": "mean: 705.070173565767 usec\nrounds: 1377"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1732.6116102043363,
            "unit": "iter/sec",
            "range": "stddev: 0.000011027669878653461",
            "extra": "mean: 577.1633954836909 usec\nrounds: 1727"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 224.65725317269744,
            "unit": "iter/sec",
            "range": "stddev: 0.00021265276667098922",
            "extra": "mean: 4.451225081218655 msec\nrounds: 197"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 14.902683909290372,
            "unit": "iter/sec",
            "range": "stddev: 0.0011684632270197114",
            "extra": "mean: 67.10200700000067 msec\nrounds: 15"
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
          "id": "7f77f39de0ac016fa9432ad24d5ff322a73d444e",
          "message": "chore(release): bump development version to 1.30.0 and harden Windows CI installer",
          "timestamp": "2026-09-28T20:19:54+02:00",
          "tree_id": "b4d8d37842816b0e3030dc7790a350080d5af369",
          "url": "https://github.com/ma2za/pseudonymize/commit/7f77f39de0ac016fa9432ad24d5ff322a73d444e"
        },
        "date": 1790619639258,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1033731.631848555,
            "unit": "iter/sec",
            "range": "stddev: 1.78977453496531e-7",
            "extra": "mean: 967.3690629082957 nsec\nrounds: 192308"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 656.602881370824,
            "unit": "iter/sec",
            "range": "stddev: 0.00001750611382985292",
            "extra": "mean: 1.5229905752351376 msec\nrounds: 638"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2603.2777229447242,
            "unit": "iter/sec",
            "range": "stddev: 0.000008510636506049495",
            "extra": "mean: 384.1311248455043 usec\nrounds: 2427"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2600.5853818427645,
            "unit": "iter/sec",
            "range": "stddev: 0.000010500445053318083",
            "extra": "mean: 384.5288091604221 usec\nrounds: 2620"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 427.9028403850139,
            "unit": "iter/sec",
            "range": "stddev: 0.00003153469746205768",
            "extra": "mean: 2.3369791121279553 msec\nrounds: 437"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2602.1611408957006,
            "unit": "iter/sec",
            "range": "stddev: 0.000011513015246692719",
            "extra": "mean: 384.29595472930083 usec\nrounds: 2474"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2597.0156946951834,
            "unit": "iter/sec",
            "range": "stddev: 0.00001779448684489948",
            "extra": "mean: 385.0573571975936 usec\nrounds: 2612"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2601.979369748572,
            "unit": "iter/sec",
            "range": "stddev: 0.000010011634528522725",
            "extra": "mean: 384.3228011821745 usec\nrounds: 2369"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2601.4025523896794,
            "unit": "iter/sec",
            "range": "stddev: 0.000010667419137873055",
            "extra": "mean: 384.40801831357777 usec\nrounds: 2621"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2597.063211360734,
            "unit": "iter/sec",
            "range": "stddev: 0.000011536999919443623",
            "extra": "mean: 385.05031207001275 usec\nrounds: 2618"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2586.8522562673515,
            "unit": "iter/sec",
            "range": "stddev: 0.000014071426492625856",
            "extra": "mean: 386.5702022901496 usec\nrounds: 2620"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16143.976317193083,
            "unit": "iter/sec",
            "range": "stddev: 0.000002575360194693858",
            "extra": "mean: 61.942608212018726 usec\nrounds: 16001"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4922.466164741352,
            "unit": "iter/sec",
            "range": "stddev: 0.000004214426247209524",
            "extra": "mean: 203.15020287245477 usec\nrounds: 5013"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2602.4883700325145,
            "unit": "iter/sec",
            "range": "stddev: 0.000008490242014442405",
            "extra": "mean: 384.2476345004786 usec\nrounds: 2342"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1194.833692383866,
            "unit": "iter/sec",
            "range": "stddev: 0.0000058231087058954476",
            "extra": "mean: 836.9365597691301 usec\nrounds: 1213"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1267.4193482629767,
            "unit": "iter/sec",
            "range": "stddev: 0.000011163105564582745",
            "extra": "mean: 789.0048399296726 usec\nrounds: 1137"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 166.25874382128313,
            "unit": "iter/sec",
            "range": "stddev: 0.0000662769918348569",
            "extra": "mean: 6.01472125324688 msec\nrounds: 154"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 10.91064395359577,
            "unit": "iter/sec",
            "range": "stddev: 0.0013899890744689912",
            "extra": "mean: 91.6536186363624 msec\nrounds: 11"
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
          "id": "f6c67b41a027d3a041319771206fd8cd191fad1c",
          "message": "chore(release): prepare 1.30.0 release and update changelog",
          "timestamp": "2026-09-28T20:40:12+02:00",
          "tree_id": "58861b56cc343fb703f384a9a817e4e962c743f6",
          "url": "https://github.com/ma2za/pseudonymize/commit/f6c67b41a027d3a041319771206fd8cd191fad1c"
        },
        "date": 1790620857946,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1230512.882914932,
            "unit": "iter/sec",
            "range": "stddev: 7.185480024639337e-8",
            "extra": "mean: 812.6692648931269 nsec\nrounds: 118568"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 856.2342315603254,
            "unit": "iter/sec",
            "range": "stddev: 0.0001587871478875353",
            "extra": "mean: 1.167904719457068 msec\nrounds: 884"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 3361.4425150052525,
            "unit": "iter/sec",
            "range": "stddev: 0.00003553938560942939",
            "extra": "mean: 297.49132865907046 usec\nrounds: 3423"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 3369.378131964704,
            "unit": "iter/sec",
            "range": "stddev: 0.000030548610582759327",
            "extra": "mean: 296.79067199765257 usec\nrounds: 3439"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 615.0733776100818,
            "unit": "iter/sec",
            "range": "stddev: 0.00011970650380386269",
            "extra": "mean: 1.6258222781248999 msec\nrounds: 640"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 3363.2369588836223,
            "unit": "iter/sec",
            "range": "stddev: 0.00003469582392527391",
            "extra": "mean: 297.33260315144 usec\nrounds: 3427"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 3293.325729709496,
            "unit": "iter/sec",
            "range": "stddev: 0.00005324324493505188",
            "extra": "mean: 303.64442574837864 usec\nrounds: 3441"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 3430.5600858634643,
            "unit": "iter/sec",
            "range": "stddev: 0.000006268930828721021",
            "extra": "mean: 291.49759076390063 usec\nrounds: 3443"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 3429.953107976748,
            "unit": "iter/sec",
            "range": "stddev: 0.00000791087946730849",
            "extra": "mean: 291.54917531507516 usec\nrounds: 3411"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 3431.099053105339,
            "unit": "iter/sec",
            "range": "stddev: 0.000006824269311679258",
            "extra": "mean: 291.45180145555497 usec\nrounds: 3435"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 3427.3414080903517,
            "unit": "iter/sec",
            "range": "stddev: 0.000010717377475940388",
            "extra": "mean: 291.77134137832525 usec\nrounds: 3439"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 17544.396565879986,
            "unit": "iter/sec",
            "range": "stddev: 0.000001927961983779867",
            "extra": "mean: 56.998255610841646 usec\nrounds: 17288"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 5848.984497596036,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032359513365761612",
            "extra": "mean: 170.96984962278586 usec\nrounds: 5832"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 3429.5542756188975,
            "unit": "iter/sec",
            "range": "stddev: 0.0000064843319370074344",
            "extra": "mean: 291.583080375522 usec\nrounds: 3409"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1418.29009483663,
            "unit": "iter/sec",
            "range": "stddev: 0.000006842475054289898",
            "extra": "mean: 705.07437345897 usec\nrounds: 1379"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1709.1142657097296,
            "unit": "iter/sec",
            "range": "stddev: 0.00005786264893484734",
            "extra": "mean: 585.098386961704 usec\nrounds: 1672"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 223.01590597521712,
            "unit": "iter/sec",
            "range": "stddev: 0.00011514862691562232",
            "extra": "mean: 4.48398510243985 msec\nrounds: 205"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 14.457336835609745,
            "unit": "iter/sec",
            "range": "stddev: 0.0015198635415479376",
            "extra": "mean: 69.16903239999974 msec\nrounds: 15"
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
          "id": "672f8c91fc797e0bf7e1e31413a845cef6e235b5",
          "message": "chore(release): bump development version to 1.31.0",
          "timestamp": "2026-09-28T21:23:21+02:00",
          "tree_id": "6a8e7041b77002a654766649f2b820c5319bb1ad",
          "url": "https://github.com/ma2za/pseudonymize/commit/672f8c91fc797e0bf7e1e31413a845cef6e235b5"
        },
        "date": 1790623434893,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1046302.5575841215,
            "unit": "iter/sec",
            "range": "stddev: 1.6632676634696315e-7",
            "extra": "mean: 955.7464929732824 nsec\nrounds: 199243"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 638.3720039745507,
            "unit": "iter/sec",
            "range": "stddev: 0.00006805868658137692",
            "extra": "mean: 1.5664847358184995 msec\nrounds: 617"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2605.1351912664068,
            "unit": "iter/sec",
            "range": "stddev: 0.000008831644037964417",
            "extra": "mean: 383.8572383316049 usec\nrounds: 2614"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2607.1244640434406,
            "unit": "iter/sec",
            "range": "stddev: 0.000007773570411005881",
            "extra": "mean: 383.5643498389334 usec\nrounds: 2484"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 424.544423304671,
            "unit": "iter/sec",
            "range": "stddev: 0.0000532262131324615",
            "extra": "mean: 2.3554661069764133 msec\nrounds: 430"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2604.131819790733,
            "unit": "iter/sec",
            "range": "stddev: 0.000011622622267824345",
            "extra": "mean: 384.0051384496963 usec\nrounds: 2593"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2489.2668846955376,
            "unit": "iter/sec",
            "range": "stddev: 0.00007433774625462589",
            "extra": "mean: 401.7247030232799 usec\nrounds: 2613"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2585.2292717106966,
            "unit": "iter/sec",
            "range": "stddev: 0.000030792298431057426",
            "extra": "mean: 386.81288771663975 usec\nrounds: 1327"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2605.831280740085,
            "unit": "iter/sec",
            "range": "stddev: 0.000011200657687012335",
            "extra": "mean: 383.7546994661868 usec\nrounds: 2622"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2603.5207419372414,
            "unit": "iter/sec",
            "range": "stddev: 0.00000942613671623344",
            "extra": "mean: 384.09526910698423 usec\nrounds: 2486"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2575.168702536858,
            "unit": "iter/sec",
            "range": "stddev: 0.000035332428945547504",
            "extra": "mean: 388.3240732985288 usec\nrounds: 2483"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16169.934640368883,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023723727791865907",
            "extra": "mean: 61.84316895774336 usec\nrounds: 16004"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4930.683544704977,
            "unit": "iter/sec",
            "range": "stddev: 0.0000039804286130037815",
            "extra": "mean: 202.81163675042424 usec\nrounds: 4936"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2604.429811803726,
            "unit": "iter/sec",
            "range": "stddev: 0.000007536266596746966",
            "extra": "mean: 383.96120159116106 usec\nrounds: 2262"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1196.283731721507,
            "unit": "iter/sec",
            "range": "stddev: 0.000004795647833807831",
            "extra": "mean: 835.9220922957418 usec\nrounds: 1246"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1241.6169295992365,
            "unit": "iter/sec",
            "range": "stddev: 0.00010432661155194589",
            "extra": "mean: 805.4013892374803 usec\nrounds: 1115"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 167.9051013283505,
            "unit": "iter/sec",
            "range": "stddev: 0.00006667612682115366",
            "extra": "mean: 5.955745192306147 msec\nrounds: 156"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 10.926104482753766,
            "unit": "iter/sec",
            "range": "stddev: 0.0009536210282866258",
            "extra": "mean: 91.523927999997 msec\nrounds: 11"
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
          "id": "e4f0249c7114010a7311e2ea129d54fbaf4fec38",
          "message": "feat(benchmarks): support flexible entity and text schemas in grouped template partitioning",
          "timestamp": "2026-09-29T08:15:46+02:00",
          "tree_id": "1d1e7354b02a1e21a209c0e405b1b893e60f7e73",
          "url": "https://github.com/ma2za/pseudonymize/commit/e4f0249c7114010a7311e2ea129d54fbaf4fec38"
        },
        "date": 1790662581325,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 922538.273010739,
            "unit": "iter/sec",
            "range": "stddev: 1.0982780353770321e-7",
            "extra": "mean: 1.083965868143835 usec\nrounds: 30139"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 695.6698041213543,
            "unit": "iter/sec",
            "range": "stddev: 0.000029237069573167863",
            "extra": "mean: 1.4374635697506248 msec\nrounds: 681"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2656.882720410762,
            "unit": "iter/sec",
            "range": "stddev: 0.000009672876575127819",
            "extra": "mean: 376.3809340614767 usec\nrounds: 2563"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2658.384005713711,
            "unit": "iter/sec",
            "range": "stddev: 0.000009080964477683199",
            "extra": "mean: 376.1683781766226 usec\nrounds: 2676"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 496.10886812648243,
            "unit": "iter/sec",
            "range": "stddev: 0.000020464574503091793",
            "extra": "mean: 2.01568660478984 msec\nrounds: 501"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2657.529697075922,
            "unit": "iter/sec",
            "range": "stddev: 0.000009610901228486271",
            "extra": "mean: 376.2893039728961 usec\nrounds: 2668"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2654.345524996434,
            "unit": "iter/sec",
            "range": "stddev: 0.00001631699505773798",
            "extra": "mean: 376.7407033420577 usec\nrounds: 2663"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2624.086057596965,
            "unit": "iter/sec",
            "range": "stddev: 0.000039244564071446",
            "extra": "mean: 381.08506278020496 usec\nrounds: 2676"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2646.299086779216,
            "unit": "iter/sec",
            "range": "stddev: 0.000009967898066969831",
            "extra": "mean: 377.88623553397736 usec\nrounds: 2454"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2657.1780169988456,
            "unit": "iter/sec",
            "range": "stddev: 0.00000986201029457776",
            "extra": "mean: 376.3391062257288 usec\nrounds: 2570"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2658.0704702176185,
            "unit": "iter/sec",
            "range": "stddev: 0.000008580126240794845",
            "extra": "mean: 376.212749513044 usec\nrounds: 2567"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 13613.196263872278,
            "unit": "iter/sec",
            "range": "stddev: 0.00000259969480089411",
            "extra": "mean: 73.45813434379662 usec\nrounds: 13525"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4542.071349973777,
            "unit": "iter/sec",
            "range": "stddev: 0.000004744943246630606",
            "extra": "mean: 220.16386862918247 usec\nrounds: 4552"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2659.1845041145134,
            "unit": "iter/sec",
            "range": "stddev: 0.00000779579071412922",
            "extra": "mean: 376.0551396312351 usec\nrounds: 2657"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1100.834118086111,
            "unit": "iter/sec",
            "range": "stddev: 0.000005247170834607244",
            "extra": "mean: 908.4020776341679 usec\nrounds: 1082"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1347.659417842718,
            "unit": "iter/sec",
            "range": "stddev: 0.00001919134490395986",
            "extra": "mean: 742.0272412749224 usec\nrounds: 1318"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 177.34999248567692,
            "unit": "iter/sec",
            "range": "stddev: 0.00007062754134258576",
            "extra": "mean: 5.638568042684082 msec\nrounds: 164"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 11.77848080410613,
            "unit": "iter/sec",
            "range": "stddev: 0.0011253324677896965",
            "extra": "mean: 84.90059258333105 msec\nrounds: 12"
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
          "id": "36568241b5082b96703cadcd7fe0742c6abdff97",
          "message": "chore(release): prepare 1.31.0 release and update changelog",
          "timestamp": "2026-09-29T08:48:14+02:00",
          "tree_id": "47082b92816f105bf10e4804ce11828e03270504",
          "url": "https://github.com/ma2za/pseudonymize/commit/36568241b5082b96703cadcd7fe0742c6abdff97"
        },
        "date": 1790664541309,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 946496.5033281383,
            "unit": "iter/sec",
            "range": "stddev: 1.237764204959663e-7",
            "extra": "mean: 1.05652793907186 usec\nrounds: 91517"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 660.875505064627,
            "unit": "iter/sec",
            "range": "stddev: 0.00020507425266648156",
            "extra": "mean: 1.513144294706777 msec\nrounds: 699"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2630.51480133384,
            "unit": "iter/sec",
            "range": "stddev: 0.00003012735291116922",
            "extra": "mean: 380.15372484995555 usec\nrounds: 2664"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2655.758551929523,
            "unit": "iter/sec",
            "range": "stddev: 0.000010267037921049183",
            "extra": "mean: 376.54025411062196 usec\nrounds: 2676"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 488.35527349977406,
            "unit": "iter/sec",
            "range": "stddev: 0.000041031081054100444",
            "extra": "mean: 2.0476895700000313 msec\nrounds: 500"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2652.275048732028,
            "unit": "iter/sec",
            "range": "stddev: 0.0000157449568776668",
            "extra": "mean: 377.0348028112957 usec\nrounds: 2561"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2654.7323603291825,
            "unit": "iter/sec",
            "range": "stddev: 0.0000127761970052186",
            "extra": "mean: 376.68580642758343 usec\nrounds: 2676"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2655.422565480901,
            "unit": "iter/sec",
            "range": "stddev: 0.00000962099935481946",
            "extra": "mean: 376.5878971578667 usec\nrounds: 2674"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2622.0138776098615,
            "unit": "iter/sec",
            "range": "stddev: 0.000036255424216301224",
            "extra": "mean: 381.3862346569904 usec\nrounds: 2493"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2658.9647523543404,
            "unit": "iter/sec",
            "range": "stddev: 0.00000828674087370197",
            "extra": "mean: 376.0862189371127 usec\nrounds: 2672"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2659.2076786304706,
            "unit": "iter/sec",
            "range": "stddev: 0.000008688410580584634",
            "extra": "mean: 376.0518623784262 usec\nrounds: 2674"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 13611.677238445647,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025392487035376808",
            "extra": "mean: 73.4663320678468 usec\nrounds: 13434"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4540.721826139161,
            "unit": "iter/sec",
            "range": "stddev: 0.000004306582687647119",
            "extra": "mean: 220.22930236408467 usec\nrounds: 4230"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2660.1348741591155,
            "unit": "iter/sec",
            "range": "stddev: 0.00000783274443550967",
            "extra": "mean: 375.9207887217019 usec\nrounds: 2660"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1100.5993015289532,
            "unit": "iter/sec",
            "range": "stddev: 0.000004595159599657312",
            "extra": "mean: 908.5958882681457 usec\nrounds: 1074"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1346.9935153811703,
            "unit": "iter/sec",
            "range": "stddev: 0.000010277035412929052",
            "extra": "mean: 742.3940713753336 usec\nrounds: 1345"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 167.9580760485228,
            "unit": "iter/sec",
            "range": "stddev: 0.0008071335238022795",
            "extra": "mean: 5.953866723926402 msec\nrounds: 163"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 11.344388824691496,
            "unit": "iter/sec",
            "range": "stddev: 0.0017979139170466068",
            "extra": "mean: 88.14930583333513 msec\nrounds: 12"
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
          "id": "e359a2f9c6b1cb379f597c6a7aaf88403215e861",
          "message": "chore(release): bump development version to 1.32.0",
          "timestamp": "2026-09-29T09:41:03+02:00",
          "tree_id": "90f5119fe7ad101a107611904d911da9f390f51d",
          "url": "https://github.com/ma2za/pseudonymize/commit/e359a2f9c6b1cb379f597c6a7aaf88403215e861"
        },
        "date": 1790667699040,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1044531.0538914393,
            "unit": "iter/sec",
            "range": "stddev: 1.4729340455560613e-7",
            "extra": "mean: 957.3674198334868 nsec\nrounds: 171233"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 634.2444680627016,
            "unit": "iter/sec",
            "range": "stddev: 0.00010837105260771198",
            "extra": "mean: 1.5766791045958948 msec\nrounds: 631"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2466.8443198467207,
            "unit": "iter/sec",
            "range": "stddev: 0.00008465980084016342",
            "extra": "mean: 405.3762095786149 usec\nrounds: 2610"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2488.959222568713,
            "unit": "iter/sec",
            "range": "stddev: 0.0000725575533352705",
            "extra": "mean: 401.7743605168256 usec\nrounds: 2477"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 454.1490533147986,
            "unit": "iter/sec",
            "range": "stddev: 0.000056962131809363135",
            "extra": "mean: 2.2019202565789313 msec\nrounds: 456"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2597.6845492827943,
            "unit": "iter/sec",
            "range": "stddev: 0.000017740878359536902",
            "extra": "mean: 384.958212218683 usec\nrounds: 2488"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2539.165045355385,
            "unit": "iter/sec",
            "range": "stddev: 0.00006247089864211469",
            "extra": "mean: 393.83024818697385 usec\nrounds: 2482"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2423.413363181357,
            "unit": "iter/sec",
            "range": "stddev: 0.00011962948238638555",
            "extra": "mean: 412.6411181818529 usec\nrounds: 2310"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2601.9084171506165,
            "unit": "iter/sec",
            "range": "stddev: 0.000011553997449206908",
            "extra": "mean: 384.3332814515865 usec\nrounds: 2480"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2588.8779342773682,
            "unit": "iter/sec",
            "range": "stddev: 0.00001185267115598758",
            "extra": "mean: 386.2677288719406 usec\nrounds: 2615"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2517.981605818923,
            "unit": "iter/sec",
            "range": "stddev: 0.00005506828720386096",
            "extra": "mean: 397.14348893139356 usec\nrounds: 2620"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16149.910341720104,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024524933601318236",
            "extra": "mean: 61.91984839796278 usec\nrounds: 16042"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4929.162039829428,
            "unit": "iter/sec",
            "range": "stddev: 0.000004070720876799037",
            "extra": "mean: 202.87423945888472 usec\nrounds: 4435"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2601.7587413111874,
            "unit": "iter/sec",
            "range": "stddev: 0.000008303550095546251",
            "extra": "mean: 384.3553916517402 usec\nrounds: 2252"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1195.603631163727,
            "unit": "iter/sec",
            "range": "stddev: 0.000004752843803232318",
            "extra": "mean: 836.3975935960161 usec\nrounds: 1218"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1264.2602976763426,
            "unit": "iter/sec",
            "range": "stddev: 0.000010420816835933391",
            "extra": "mean: 790.9763533964943 usec\nrounds: 1163"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 167.29975028686155,
            "unit": "iter/sec",
            "range": "stddev: 0.00004954787008852288",
            "extra": "mean: 5.9772952337666005 msec\nrounds: 154"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 10.849255304255461,
            "unit": "iter/sec",
            "range": "stddev: 0.0012786087252133521",
            "extra": "mean: 92.17222490909259 msec\nrounds: 11"
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
          "id": "988bc88be5388a3c0e05012316df150aa7f517bf",
          "message": "feat(benchmarks): support flexible annotation schemas in evaluate_quality",
          "timestamp": "2026-09-29T10:15:56+02:00",
          "tree_id": "2d4f5867ac869d06995a263a24492d08b26658dc",
          "url": "https://github.com/ma2za/pseudonymize/commit/988bc88be5388a3c0e05012316df150aa7f517bf"
        },
        "date": 1790669794489,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1385703.5796142202,
            "unit": "iter/sec",
            "range": "stddev: 7.403056809450062e-8",
            "extra": "mean: 721.6550600803095 nsec\nrounds: 109099"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 743.0427651222792,
            "unit": "iter/sec",
            "range": "stddev: 0.00003585084359371736",
            "extra": "mean: 1.3458175584758363 msec\nrounds: 761"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2760.0863641430474,
            "unit": "iter/sec",
            "range": "stddev: 0.000012706113782594801",
            "extra": "mean: 362.3075034865731 usec\nrounds: 2868"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2688.5820608084177,
            "unit": "iter/sec",
            "range": "stddev: 0.00003733137409799303",
            "extra": "mean: 371.94326875011376 usec\nrounds: 2720"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 553.8271533145049,
            "unit": "iter/sec",
            "range": "stddev: 0.00006120478035661695",
            "extra": "mean: 1.8056175000002652 msec\nrounds: 552"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2772.305586929413,
            "unit": "iter/sec",
            "range": "stddev: 0.00001189201925312973",
            "extra": "mean: 360.7105957996475 usec\nrounds: 2714"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2669.1505314941724,
            "unit": "iter/sec",
            "range": "stddev: 0.00003482392104668456",
            "extra": "mean: 374.65103155504937 usec\nrounds: 2662"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2767.4663920249955,
            "unit": "iter/sec",
            "range": "stddev: 0.000012423776260400671",
            "extra": "mean: 361.34133476081183 usec\nrounds: 2802"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2727.7688867452894,
            "unit": "iter/sec",
            "range": "stddev: 0.000014163966087311896",
            "extra": "mean: 366.59997291529226 usec\nrounds: 2806"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2730.666606052204,
            "unit": "iter/sec",
            "range": "stddev: 0.000015812649679956863",
            "extra": "mean: 366.2109456290331 usec\nrounds: 2814"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2775.2064748117446,
            "unit": "iter/sec",
            "range": "stddev: 0.000012505404143605432",
            "extra": "mean: 360.33354962096456 usec\nrounds: 2771"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 19669.018346581062,
            "unit": "iter/sec",
            "range": "stddev: 0.000002366513854200641",
            "extra": "mean: 50.84137817044761 usec\nrounds: 18846"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 6626.777905222732,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036601266817248675",
            "extra": "mean: 150.90289946368577 usec\nrounds: 6714"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2742.489908941778,
            "unit": "iter/sec",
            "range": "stddev: 0.000012062349399619657",
            "extra": "mean: 364.6321529714805 usec\nrounds: 2726"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1569.9823122095108,
            "unit": "iter/sec",
            "range": "stddev: 0.000010119975276370777",
            "extra": "mean: 636.9498511054258 usec\nrounds: 1538"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1530.1946567079797,
            "unit": "iter/sec",
            "range": "stddev: 0.000024946152771962383",
            "extra": "mean: 653.5116271751814 usec\nrounds: 1494"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 231.41650325761205,
            "unit": "iter/sec",
            "range": "stddev: 0.00007388010858703753",
            "extra": "mean: 4.321212990098651 msec\nrounds: 202"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 14.973549030980532,
            "unit": "iter/sec",
            "range": "stddev: 0.0010946094419766758",
            "extra": "mean: 66.78443420000045 msec\nrounds: 15"
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
          "id": "04922ffc3ea1235dd1e6759207e9a3fd0ad6494c",
          "message": "chore(release): prepare 1.32.0 release and update changelog",
          "timestamp": "2026-09-29T22:26:06+02:00",
          "tree_id": "afb7df5e97f5fabde11bafa74d32d47a73daec84",
          "url": "https://github.com/ma2za/pseudonymize/commit/04922ffc3ea1235dd1e6759207e9a3fd0ad6494c"
        },
        "date": 1790713624147,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1422816.0019060285,
            "unit": "iter/sec",
            "range": "stddev: 6.639661684709452e-8",
            "extra": "mean: 702.8315668789099 nsec\nrounds: 95521"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 747.2821676665105,
            "unit": "iter/sec",
            "range": "stddev: 0.000020713838800994384",
            "extra": "mean: 1.3381826079466541 msec\nrounds: 755"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2783.3974925241473,
            "unit": "iter/sec",
            "range": "stddev: 0.000011108446359285533",
            "extra": "mean: 359.2731554461312 usec\nrounds: 2644"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2781.1611771282314,
            "unit": "iter/sec",
            "range": "stddev: 0.000011063339518347202",
            "extra": "mean: 359.56204488392115 usec\nrounds: 2629"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 621.2463247520268,
            "unit": "iter/sec",
            "range": "stddev: 0.000133068789740448",
            "extra": "mean: 1.6096674703052039 msec\nrounds: 623"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2793.256325145986,
            "unit": "iter/sec",
            "range": "stddev: 0.000011195721248671364",
            "extra": "mean: 358.00509641654037 usec\nrounds: 2707"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2776.318855243463,
            "unit": "iter/sec",
            "range": "stddev: 0.00002817117242676419",
            "extra": "mean: 360.18917571782555 usec\nrounds: 2891"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2746.555449076601,
            "unit": "iter/sec",
            "range": "stddev: 0.00001163330016815575",
            "extra": "mean: 364.09241267501176 usec\nrounds: 2714"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2804.1001438617727,
            "unit": "iter/sec",
            "range": "stddev: 0.000011125053034707672",
            "extra": "mean: 356.6206443050968 usec\nrounds: 2713"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2797.4516867143034,
            "unit": "iter/sec",
            "range": "stddev: 0.000011104493666151578",
            "extra": "mean: 357.468193194976 usec\nrounds: 2645"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2780.255161459133,
            "unit": "iter/sec",
            "range": "stddev: 0.00001429579999815933",
            "extra": "mean: 359.6792171676718 usec\nrounds: 2726"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 20178.032928346955,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017648488177037376",
            "extra": "mean: 49.55884468773751 usec\nrounds: 19831"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 6759.935876245595,
            "unit": "iter/sec",
            "range": "stddev: 0.0000035058617094881905",
            "extra": "mean: 147.93039731545363 usec\nrounds: 6705"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2774.2833395769044,
            "unit": "iter/sec",
            "range": "stddev: 0.00001018679367195624",
            "extra": "mean: 360.45344962944785 usec\nrounds: 2700"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1553.5909246209321,
            "unit": "iter/sec",
            "range": "stddev: 0.00006243377576081124",
            "extra": "mean: 643.670083386973 usec\nrounds: 1547"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1550.0089339827273,
            "unit": "iter/sec",
            "range": "stddev: 0.000022231625249551946",
            "extra": "mean: 645.1575717247728 usec\nrounds: 1450"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 235.9276317807715,
            "unit": "iter/sec",
            "range": "stddev: 0.00014616208305978857",
            "extra": "mean: 4.238587877359016 msec\nrounds: 212"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 15.069432228158126,
            "unit": "iter/sec",
            "range": "stddev: 0.0017886985815224166",
            "extra": "mean: 66.35950079999968 msec\nrounds: 15"
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
          "id": "49de503e98b38792ad2c02721eb950c9da25a862",
          "message": "chore(release): bump development version to 1.33.0",
          "timestamp": "2026-09-29T22:33:25+02:00",
          "tree_id": "61c412fef26757cc36d6a2c4ddfc61eed4dcde21",
          "url": "https://github.com/ma2za/pseudonymize/commit/49de503e98b38792ad2c02721eb950c9da25a862"
        },
        "date": 1790714038467,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1066215.3052382653,
            "unit": "iter/sec",
            "range": "stddev: 1.0077513867404754e-7",
            "extra": "mean: 937.8968723174835 nsec\nrounds: 102376"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 650.2001561646401,
            "unit": "iter/sec",
            "range": "stddev: 0.00004572949909793546",
            "extra": "mean: 1.5379879418958267 msec\nrounds: 654"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2605.0181917559626,
            "unit": "iter/sec",
            "range": "stddev: 0.00000819420440995167",
            "extra": "mean: 383.87447856014046 usec\nrounds: 2472"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2607.770948805702,
            "unit": "iter/sec",
            "range": "stddev: 0.000007345987593602055",
            "extra": "mean: 383.4692615384708 usec\nrounds: 2470"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 439.51930975368765,
            "unit": "iter/sec",
            "range": "stddev: 0.000024195175437437518",
            "extra": "mean: 2.275212892376476 msec\nrounds: 446"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2603.747177175471,
            "unit": "iter/sec",
            "range": "stddev: 0.000009731372648149333",
            "extra": "mean: 384.06186620806784 usec\nrounds: 2616"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2598.9957589518854,
            "unit": "iter/sec",
            "range": "stddev: 0.000015784331526953425",
            "extra": "mean: 384.7639983850057 usec\nrounds: 2477"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2604.145620857377,
            "unit": "iter/sec",
            "range": "stddev: 0.000009244224393034081",
            "extra": "mean: 384.0031033559347 usec\nrounds: 2622"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2602.5582441275706,
            "unit": "iter/sec",
            "range": "stddev: 0.000013114835156655204",
            "extra": "mean: 384.2373181297312 usec\nrounds: 2609"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2576.483020842774,
            "unit": "iter/sec",
            "range": "stddev: 0.00003561450965350579",
            "extra": "mean: 388.125981002156 usec\nrounds: 2474"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2582.7369840264037,
            "unit": "iter/sec",
            "range": "stddev: 0.00003375592156866821",
            "extra": "mean: 387.18615413987385 usec\nrounds: 2621"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16162.455522655995,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022436198450425247",
            "extra": "mean: 61.87178666003028 usec\nrounds: 14348"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4931.14111288718,
            "unit": "iter/sec",
            "range": "stddev: 0.000004093211190500619",
            "extra": "mean: 202.7928175461401 usec\nrounds: 5004"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2602.600305070162,
            "unit": "iter/sec",
            "range": "stddev: 0.00000979167950508039",
            "extra": "mean: 384.23110842332807 usec\nrounds: 2398"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1195.9770708216145,
            "unit": "iter/sec",
            "range": "stddev: 0.000004320345287794838",
            "extra": "mean: 836.1364313723993 usec\nrounds: 1224"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1268.958450747227,
            "unit": "iter/sec",
            "range": "stddev: 0.000014575230320808619",
            "extra": "mean: 788.047866666674 usec\nrounds: 1140"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 167.959148150126,
            "unit": "iter/sec",
            "range": "stddev: 0.00006913707618336335",
            "extra": "mean: 5.953828719744252 msec\nrounds: 157"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 10.9580957924082,
            "unit": "iter/sec",
            "range": "stddev: 0.0010641584801255883",
            "extra": "mean: 91.25673099999756 msec\nrounds: 11"
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
          "id": "5fdee58a31d53fcb15f003e1287ebda4f0d4dfcf",
          "message": "feat(benchmarks): complete 1.33.0 model bake-off, evidence fusion tests, and decision record",
          "timestamp": "2026-09-29T23:05:19+02:00",
          "tree_id": "d43415b0850b6246b57796479946a704b25ddedf",
          "url": "https://github.com/ma2za/pseudonymize/commit/5fdee58a31d53fcb15f003e1287ebda4f0d4dfcf"
        },
        "date": 1790715958681,
        "tool": "pytest",
        "benches": [
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[email]",
            "value": 1043266.6473909685,
            "unit": "iter/sec",
            "range": "stddev: 1.556415754348564e-7",
            "extra": "mean: 958.5277191606085 nsec\nrounds: 192679"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[ip_address]",
            "value": 640.4141287951685,
            "unit": "iter/sec",
            "range": "stddev: 0.00007111548792389776",
            "extra": "mean: 1.5614895971788316 msec\nrounds: 638"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[payment_card]",
            "value": 2545.4130247780245,
            "unit": "iter/sec",
            "range": "stddev: 0.000013693594413607471",
            "extra": "mean: 392.86355112730917 usec\nrounds: 2484"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[iban]",
            "value": 2601.8136395827205,
            "unit": "iter/sec",
            "range": "stddev: 0.000008254963810491343",
            "extra": "mean: 384.3472817524241 usec\nrounds: 2488"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_fiscal_code]",
            "value": 438.86674779921196,
            "unit": "iter/sec",
            "range": "stddev: 0.0001209011695685716",
            "extra": "mean: 2.278595963386852 msec\nrounds: 437"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[italian_vat]",
            "value": 2578.421007300665,
            "unit": "iter/sec",
            "range": "stddev: 0.00001230595624415272",
            "extra": "mean: 387.83425870660835 usec\nrounds: 2613"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[spanish_nif]",
            "value": 2588.6668310336727,
            "unit": "iter/sec",
            "range": "stddev: 0.000011621276627074782",
            "extra": "mean: 386.299228626765 usec\nrounds: 2585"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[german_tin]",
            "value": 2592.2960652562483,
            "unit": "iter/sec",
            "range": "stddev: 0.000012015126385152189",
            "extra": "mean: 385.7584067663776 usec\nrounds: 2542"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[context_id]",
            "value": 2556.366522682691,
            "unit": "iter/sec",
            "range": "stddev: 0.000011902677083016192",
            "extra": "mean: 391.1802126678549 usec\nrounds: 2605"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[checksum]",
            "value": 2509.1071796286888,
            "unit": "iter/sec",
            "range": "stddev: 0.00001936268794059342",
            "extra": "mean: 398.5481401986126 usec\nrounds: 2418"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[phone]",
            "value": 2537.2839654393474,
            "unit": "iter/sec",
            "range": "stddev: 0.00001577308416183455",
            "extra": "mean: 394.122224244949 usec\nrounds: 2417"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[url]",
            "value": 16137.144744855317,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026815276779816883",
            "extra": "mean: 61.96883127783867 usec\nrounds: 15973"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[secret]",
            "value": 4895.402575599705,
            "unit": "iter/sec",
            "range": "stddev: 0.000004574354657821289",
            "extra": "mean: 204.273292044321 usec\nrounds: 4965"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[location]",
            "value": 2595.83155999425,
            "unit": "iter/sec",
            "range": "stddev: 0.000012231214717105682",
            "extra": "mean: 385.23300795457436 usec\nrounds: 1760"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[organization]",
            "value": 1192.3609973966843,
            "unit": "iter/sec",
            "range": "stddev: 0.000009345840358769488",
            "extra": "mean: 838.6721824877939 usec\nrounds: 1222"
          },
          {
            "name": "benchmarks/benchmark_detectors.py::test_detector_nonmatching_input[gazetteer]",
            "value": 1261.9573020934172,
            "unit": "iter/sec",
            "range": "stddev: 0.00003230272663333155",
            "extra": "mean: 792.4198372965035 usec\nrounds: 799"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[4 KiB]",
            "value": 166.83377886768926,
            "unit": "iter/sec",
            "range": "stddev: 0.00006484739895763608",
            "extra": "mean: 5.993989986842348 msec\nrounds: 152"
          },
          {
            "name": "benchmarks/benchmark_engine.py::test_process_synthetic_messages[64 KiB]",
            "value": 10.68093832672409,
            "unit": "iter/sec",
            "range": "stddev: 0.003662863890338079",
            "extra": "mean: 93.6247330909087 msec\nrounds: 11"
          }
        ]
      }
    ]
  }
}