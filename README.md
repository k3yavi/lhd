# lhd
**load haul and dump** machine for SRA to fastq dumping

Frusted by waiting hours for fastq-dump, trying to find an alternative.

Keeping log of realizations with time.
###Feb 6
* Intial reading gives an intution that it'll be difficult to parse SRA's vertical database architecture.
* Plan B is to use vdb-dump for getting intermediate dump, use that to parse and get fastq dump.
###Feb7
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
