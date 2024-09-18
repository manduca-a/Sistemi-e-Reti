#!usr/bin/perl

#traccia 5 dicembre 2022


#prima cosa controllare il contenuto del path on ls /usr/include


#i parametri passati come OPTIONS verranno inseriti nell'array di sistema ARGV

                            $#ARGV è l'indice dell'ultimo elemento dell'array ARGV

if($#ARGV=-1){                           #se non riceve il parametro

    #da ls prendo solo quelli che terminano per .h

    print "nessun parametro in input\n\n".qx{ls /usr/include | grep -P "\.h\$"};
}                       
elsif($#ARGV=0){                       #se riceve un parametro
    $cont=0;
    #devo cercare le linee che iniziano per /*

    $file = shift @ARGV;        #con shift prendo il primo elemento e lo rimuovo da ARGV

    @righe = qx{cat /usr/include/$file};        #salvandolo in array, ogni riga del file corrisponderà ad un elemento dell'array

    for $r(@righe){             #se avessi avuto for (@righe).. l'iteratore sarebbe $_
        if($r =~ /\/\*(.*)/)        #con (.*) cerca qualsiasi carattere 0 o più volte, tranne \n
        {
            if($r =~ /\/\*(.*)\*\//){
                $result[$cont] = $1;       #con $1 prendo quello che corrisponde a .* cioè l'interno del commento
                $cont++;                            #gruppo compreso tra /* e */

                next;               #prossima iterzione del for    
            }               #non posso stampare subito perché devo ordinarli
            else{
                $result[cont] = $1;
                $inCommento = 1;
            }
        }
        elsif($inCommento=1){
            if($r =~ /(.*)\*\//){
                $result[$cont] .= $1;
                $inCommento = 0;
                $cont++;
            }
            else{
                $result[$cont] .= $r;
            }

        }
    }

    for(sort({lenght $a <=> lenght $b || $a cmp $b} @result)){       #presi due elementi a e b di result, li ordina in modo lunghezz crescente
        print $_."\n";                                          # in caso di lunghezza uguale li mette in ordine alfabetico
    }
}
else{
    die "troppi parametri";
}