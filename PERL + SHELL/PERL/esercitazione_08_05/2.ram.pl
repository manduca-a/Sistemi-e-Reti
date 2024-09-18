#!/usr/bin/perl

@ram = qx{ps -o command ax | sort -k2 -r | head -n 5};

print @ram;
