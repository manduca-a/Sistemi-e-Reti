#!/usr/bin/perl
                    #   ; obbligatorio
$var = 2314;                                #dollaro per indicare una variabile scalare unaria(numeri, bool...)
$str = "ciao";

$str2 = "Ciao $var";                    #concatena la variabile stringa(nei singoli apici non funziona)
#o anche
$str3 = 'Ciao'.$var;

@array = (1, 2, 3);                                     #chiocciola per indicare insieme di variabili
@array2 = (4) x 100;                                                    #nessuna sizemax
                        # con (a)xn riempio l'array con n (elementi)

print $#array . "\n";          #indice dell'ultimo elemento di array

%hash;                                      #percentuale per array associativi

print $array2[52] . "\n";

@stringhe = ($str, $str2, $str3);

print join " / ", @stringhe;

print "\n", join " - ", @array;                       #con join imposto il separatore degli elementi

#print "\n", join " + ", @array2;

push @array, 45;            #aggiunge in coda

unshift @array, 10;         #aggiunge in testa

print "\n", join " - ", @array;                       #con join imposto il separatore degli elementi

pop @array;                             #rimuove dalla coda

shift @array;                           #rimuove dalla testa

print "\n", join " - ", @array;                       #con join imposto il separatore degli elementi
