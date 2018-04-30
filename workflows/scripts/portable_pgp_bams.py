#!/usr/bin/env python
"""Merge and sort a set of PGP input files split by chromosome.

Usage:
  portable_pgp_bams.py <pgp_hu_id> <ref file> <list of> <bam files> ...

ref_file is a hg19 reference file with chromosomes in standard GATK order:

https://software.broadinstitute.org/gatk/download/bundle
ftp://gsapubftp-anonymous:pass@ftp.broadinstitute.org/bundle/hg19/ucsc.hg19.fasta.gz

Requires:
  picard, samtools
"""
import os
import subprocess
import sys

def main(huid, ref_file, *in_files):
    order = ["M"] + range(1, 23) + ["X", "Y"]
    out_file = "%s.bam" % huid
    in_files = [x for x in in_files if not x.endswith((out_file, "-fixheader.bam"))]

    used_files = []
    cmd = ["samtools", "cat"]
    for chrom in order:
        curext = "chr%s.bam" % chrom
        cur_files = [x for x in in_files if x.endswith(curext)]
        if len(cur_files) == 1:
            fix_file = "%s-fixheader.bam" % os.path.splitext(cur_files[0])[0]
            used_files.append(cur_files[0])
            if not os.path.exists(fix_file):
                fix_cmd = ("picard ReorderSam INPUT=%s OUTPUT=%s REFERENCE=%s" % (cur_files[0], fix_file,
                                                                                  ref_file))
                print(fix_cmd)
                subprocess.check_call(fix_cmd, shell=True)
            cmd += [fix_file]
    unused_files = [x for x in in_files if x not in used_files]
    assert len(unused_files) == 0, "Did not use all input files: %s" % unused_files
    cmd += ["-o", out_file]
    print(" ".join(cmd))
    subprocess.check_call(cmd)
    subprocess.check_call(["samtools", "index", "-@", "16", out_file])

if __name__ == "__main__":
    main(*sys.argv[1:])
