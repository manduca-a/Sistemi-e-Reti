# Si legga il contenuto della cartella ./francesco
@lista_file = qx(ls ./francesco);
# Scorre e stampa la lista ordinata lessicograficamente
for(sort{$a cmp $b} @lista_file){
    print $_;
}

@var = ("francesco", "giovambattista", "denise");
# Stampare il valore dell'oggetto var su file    


#  Apri il file in scrittura
open($fh, ">", "nomefile.txt");		#con "<" lo apre in lettura  e con ">>" ci aggiunge contenuto
    
# Scorri l'array  
for $valore (@var){    # Stampa sul file precedentemente ogni elemento di @var 
	print "$valore\n";
	print $fh "$valore";       
}     
# Chiudi il file
close($fh);
