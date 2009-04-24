#!/usr/bin/perl

use CSS::SAC;
use CSS::SAC::Writer;
#use Nexopia::DocHandler;
#use Nexopia::ErrorHandler;

my $output = "";

#my $doc = Nexopia::DocHandler->new();
#my $error = Nexopia::ErrorHandler->new();
my $doc = CSS::SAC::Writer->new({string => \$output});

my $sac = CSS::SAC->new
(
	{
		DocumentHandler => $doc,
		#ErrorHandler => $error,
		ErrorHandler => $doc,
	}
);

$sac->parse({filename => $ARGV[0]});

print "$output\n";
