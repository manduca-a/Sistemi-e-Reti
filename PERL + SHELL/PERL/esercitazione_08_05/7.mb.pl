#! usr/bin/perl

@mb = qx{cat /proc/meminfo};

for $s (@mb){
    @sp = split /\s+/, $s;
    $sp[1] = $sp[1]/1024;
    print $sp[0].$sp[1].$sp[2]."\n";
}