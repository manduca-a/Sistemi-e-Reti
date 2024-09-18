use warnings;       #in caso di errori di sintassi, su variabili ad esempio, stampa la presenza dell'errore


open(FILE, "<estensioni.txt") or die "Impossibile\n";

@file = <FILE>;

@tot = qx{du -ka};

#print @tot;


# for $e (@file){
#     @stri = split /\n/, $e;

#     print $stri[0];
# }
# print "\n\n\n";

for $s(@tot){
    for $e (@file){
        @stri = split /\n/, $e;
        @sp = split /\s+/, $s;
        
        if ($sp[1] =~ $stri[0]){
            #print "$sp[1]\t$sp[0]";
            $associazioni{$stri[0]} += $sp[0];
        }

        
    }
}


foreach $peso (keys %associazioni){
    print "$associazioni{$peso} $peso\n";
}
