#!usr/bin/perl


die "Too many arguments" if @ARGV>2;

$#ARGV == 1 ? print "vuoto" : print "fornito";

@commands = qx(cat $ENV{HOME}/.bash_history);

if($#ARGV==-1){

	for (sort{$b cmp $a} @commands){
		@splitted = split " ";
		#print "$splitted[0]\n";
		
		$comandi{$splitted[0]}++;
	}

	#foreach $p (sort{$comandi{$b} <=> $comandi{$a} || $b cmp $a}  keys %comandi){
	#	print "$p - $comandi{$p}\n";
	#}

	my ($most) = reverse sort { $comandi{$a} <=> $comandi{$b} || $a cmp $b } keys %comandi;
	my ($least) = sort { $comandi{$a} <=> $comandi{$b} || $a cmp $b } keys %comandi;

	print "$most $comandi{$most} \n $least $comandi{$least}";

}      

elsif($#ARGV==1 && $ARGV[0] eq "-n" && $ARGV[1] =~ "/^\d+$/"){  #se riceve due argomenti uguali a -n e un numero
	
	$output = "last_calls";
	open($fh, '>', $output) or die "Impossibile aprire!";

	$n = $ARGV[1];
	while($n > 0){
		print $fh "$commands[-$n]\n";
	}

	close($fh);
}
else {
	die "Wrong arguments!";
} 
