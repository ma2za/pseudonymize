window.BENCHMARK_DATA = {
  "lastUpdate": 1789722747675,
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
      }
    ]
  }
}