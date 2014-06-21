#!/usr/bin/perl

# generated from http://openstreetmap.gryph.de/bigmap.cgi/
# permalink for this map: http://openstreetmap.gryph.de/bigmap.cgi?xmin=4291&xmax=4308&ymin=2787&ymax=2793&zoom=13&scale=256&baseurl=http%3A%2F%2Fandy.sandbox.cloudmade.com%2Ftiles%2Fcycle%2F!z%2F!x%2F!y.png
#
use strict;
use LWP;
use GD;

my $img = GD::Image->new(4608, 1792, 1);
my $white = $img->colorAllocate(248,248,248);
$img->filledRectangle(0,0,4608,1792,$white);
my $ua = LWP::UserAgent->new();
$ua->env_proxy;
for (my $x=0;$x<18;$x++)
{
    for (my $y=0;$y<7;$y++)
    {
        my $xx = $x + 275431;
        my $yy = $y + 182710;
        foreach my $base(split(/\|/, "http://khm1.google.com/kh/v=88&x=!x&y=!y&z=19&s=Gal"))
#        foreach my $base(split(/\|/, "http://andy.sandbox.cloudmade.com/tiles/cycle/13/!x/!y.png"))
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
