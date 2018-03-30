#!/usr/bin/env python
"""Merge and sort VCF output from Veritas variant calling pipeline.

Will run combine_veritas_vcf.py if necessary to merge FreeBayes and VarScan calls.

Usage:
   make_portable_veritas_vcf.py orig_file.vcf.gz /path/to/ref.fa.fai
"""
import gzip
import os
import subprocess
import sys

def main(orig_file, ref_file):
    out_file = "%s-portable.vcf.gz" % orig_file.replace(".vcf", "").replace(".gz", "")
    first_call_parts = None
    header_parts = None
    with gzip.open(orig_file) as in_handle:
        for line in in_handle:
            if line.startswith("#CHROM"):
                header_parts = line.strip().split("\t")
                samples = header_parts[header_parts.index("FORMAT") + 1:]
            elif header_parts:
                first_call_parts = line.strip().split("\t")
                break
    # Check if we should run script to choose the right call
    choose_call = ""
    if header_parts and first_call_parts:
        sample_calls = first_call_parts[header_parts.index("FORMAT") + 1:]
        if len(sample_calls) == 2:
            choose_call = "| %s %s/combine_veritas_vcf.py" % (sys.executable,
                                                              os.path.normpath(os.path.dirname(__file__)))
        else:
            assert len(sample_calls) == 1, "Expect either single or two calls: %s" % first_call_parts
    sample_name = [x for x in samples if x != "unknown"][0]
    samples = r"\t".join(samples)
    if not ref_file.endswith(".fai") and os.path.exists(ref_file + ".fai"):
        ref_file += ".fai"
    cmd = ("gunzip -c {orig_file} {choose_call} | sed 's/{samples}/{sample_name}/' | gsort /dev/stdin {ref_file} "
           "| bgzip -c > {out_file}")

    print(cmd.format(**locals()))
    subprocess.check_call(cmd.format(**locals()), shell=True)
    cmd = "tabix -p vcf -f {out_file}"
    subprocess.check_call(cmd.format(**locals()), shell=True)

if __name__ == "__main__":
    main(*sys.argv[1:])
