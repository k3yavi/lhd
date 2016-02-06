# lhd
**load haul and dump** machine for SRA to fastq dumping

Frusted by waiting hours for fastq-dump, trying to find an alternative.

Keeping log of realizations with time.
###Feb 6
* Intial reading gives an intution that it'll be difficult to parse SRA's vertical database architecture.
* Plan B is to use vdb-dump for getting intermediate dump, use that to parse and get fastq dump.
