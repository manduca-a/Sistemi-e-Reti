@lista_file = qx{ls ./ESERCIZI};
# Scorre e stampa la lista ordinata lessicograficamente
for(sort { $a cmp $b } @lista_file){
    print $_;    
}