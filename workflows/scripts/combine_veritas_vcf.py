#!/usr/bin/env python
"""Combine two sets of variant calls into a single sample: ensemble style.

Picks the first caller if called, otherwise picks the second.

Works on stdin/stdout:

   zcat orig_vcf_w_two.vcf.gz | python combine_veritas_vcf.py | bgzip -c > combined.vcf.gz

You then want to run make_portable_veritas_vcf.py to correctly sort and make the file
a valid VCF.
"""
import sys

for line in sys.stdin:
    if not line.startswith("#"):
        parts = line.strip().split("\t")
        last = parts[-2] if parts[-2] != "." else parts[-1]
        line = "\t".join(parts[:-2] + [last]) + "\n"
    sys.stdout.write(line)
