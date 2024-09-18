#!usr/bin/perl

$name = shift || die "Folder path required.";       #con shift prende il primo elemento di @ARGV e, se non esiste, muore
die "Too many arguments" if @ARGV>0;                    #se dopo lo shift ci sono altri elementi muore


sub controlla{
    return $_[0] =~ /.*\..*/
}

@content = qx(ls -l $name);             #fa ls della cartella richiesta

if(&controlla($name)){

}

print $name;
