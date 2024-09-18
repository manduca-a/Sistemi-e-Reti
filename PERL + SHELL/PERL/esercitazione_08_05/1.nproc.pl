#!/usr/bin/perl

$nproc = qx{cat /proc/cpuinfo | grep processor > nproc.txt};

$n = qx{wc -l ./nproc.txt};

print "$n";