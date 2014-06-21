#!/usr/bin/perl

# generated from http://openstreetmap.gryph.de/bigmap.cgi/
# permalink for this map: http://openstreetmap.gryph.de/bigmap.cgi?xmin=68656&xmax=68943&ymin=44592&ymax=44703&zoom=17&scale=256&baseurl=http%3A%2F%2Fandy.sandbox.cloudmade.com%2Ftiles%2Fcycle%2F!z%2F!x%2F!y.png
#
use strict;
use LWP;
use GD;

my $img = GD::Image->new(73728, 28672, 1);
my $white = $img->colorAllocate(248,248,248);
$img->filledRectangle(0,0,73728,28672,$white);
my $ua = LWP::UserAgent->new();
$ua->env_proxy;
for (my $x=0;$x<288;$x++)
{
    for (my $y=0;$y<112;$y++)
    {
        my $xx = $x + 68656;
        my $yy = $y + 44592;
        foreach my $base(split(/\|/, "http://andy.sandbox.cloudmade.com/tiles/cycle/17/!x/!y.png"))
	{
		my $url = $base;
                $url =~ s/!x/$xx/g;
                $url =~ s/!y/$yy/g;
		print STDERR "$url... ";
		my $resp = $ua->get($url);
		print STDERR $resp->status_line;
		print STDERR "\n";
		next unless $resp->is_success;
		my $tile = GD::Image->new($resp->content);
		next if ($tile->width == 1);
		$img->copy($tile, $x*256,$y*256,0,0,256,256);
	}
    }
}
binmode STDOUT;
print $img->png();
