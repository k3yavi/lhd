# lhd
**load haul and dump** machine for SRA to fastq dumping

Frusted by waiting hours for fastq-dump, trying to find an alternative.

Keeping log of realizations with time.
###Feb 6
* Intial reading gives an intution that it'll be difficult to parse SRA's vertical database architecture.
* Plan B is to use vdb-dump for getting intermediate dump, use that to parse and get fastq dump.
* So turns out Plan-B will not work:
```
╰─$ /usr/bin/time fastq-dump --split-3  SRR453569.sra                                              127 ↵
Read 4032514 spots for SRR453569.sra
Written 4032514 spots for SRR453569.sra
367.82user 4.41system 6:16.85elapsed 98%CPU (0avgtext+0avgdata 40412maxresident)k
0inputs+5064544outputs (0major+265353minor)pagefaults 0swaps
```
where as dumping itself through vda-dump take:
```
╰─$ /usr/bin/time vdb-dump SRR453569.sra > /dev/null                                                     
688.99user 1.53system 11:31.19elapsed 99%CPU (0avgtext+0avgdata 429516maxresident)k
0inputs+0outputs (0major+1359521minor)pagefaults 0swaps
```
so no matter how fast I try to take input from vda it'll take minimum 11 min which is worse then fastq-dump i.e. 6 min

###Feb7
* OMG OMG realization check this shittt,  !!!
* lesson learnt: take shower when stuck :p
```
╰─$ /usr/bin/time vdb-dump -f fastq  SRR453569.sra > test.fastq
22.37user 3.36system 0:27.27elapsed 94%CPU (0avgtext+0avgdata 323528maxresident)k
0inputs+4186232outputs (0major+785178minor)pagefaults 0swaps
```

* ok so reading from stream in python slows it down:
```
╰─$ /usr/bin/time python3 lhd.py > /dev/null                                                       127 ↵
46.62user 2.49system 0:45.81elapsed 107%CPU (0avgtext+0avgdata 323628maxresident)k
0inputs+0outputs (0major+508963minor)pagefaults 0swaps
```
