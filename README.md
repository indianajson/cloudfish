<h1 align="center">Cloudfish<br>
  <sup><sub>FIND SUBDOMAINS USING CLOUDFLARE</sub></sup><br></h1>
  
This tool finds subdomains using Cloudflare's DNS scanner. That's it. 

When run it will automatically create a Cloudflare zone for a given domain, scan for DNS records, save any records found, and delete the zone. The script is quiet by default (outputting only a tab delimited list of DNS records). If you want to see what's going on add the `--verbose` flag to your command. The request is totally passive since Cloudflare runs the test on their end. 

## Output

```sh
indy@mac > ./cloudfish.py -k de567yuhgfr567yhg -e indy@example.com -a 3456ygfe3456ygf -d yahoo.com --verbose


 █████╗██╗    █████╗ ██╗  ██╗█████╗  ██████╗██╗██████╗██╗ ██╗
██╔═══╝██║   ██╔══██╗██║  ██║██╔═██╗ ██╔═══╝██║██╔═══╝██║ ██║
██║    ██║   ██║  ██║██║  ██║██║ ██║ ████╗  ██║██████╗██████║
██║    ██║   ██║  ██║██║  ██║██║ ██║ ██╔═╝  ██║╚═══██║██╔═██║
╚█████╗█████╗╚█████╔╝╚█████╔╝█████╔╝ ██║    ██║██████║██║ ██║
 ╚════╝╚════╝ ╚════╝  ╚════╝ ╚════╝  ╚═╝    ╚═╝╚═════╝╚═╝ ╚═╝
          ________________________________________
              FIND SUBDOMAINS USING CLOUDFLARE
                   github.com/indianajson
          ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
          
[STATUS] Creating zone for yahoo.com in your indy@example.com Cloudflare account.
[STATUS] Starting scan of yahoo.com (this will take a moment).
[SUCCESS] We found some DNS records for yahoo.com.
	[A] cn.yahoo.com ===> 124.108.115.100
	[A] cn.yahoo.com ===> 98.136.103.23
	[A] cn.yahoo.com ===> 106.10.248.150
	[A] cn.yahoo.com ===> 74.6.136.150
	[A] cn.yahoo.com ===> 212.82.100.150
	[A] data.yahoo.com ===> 66.228.173.54
	[A] dns.yahoo.com ===> 68.142.196.63
	[A] go.yahoo.com ===> 34.98.88.98
[STATUS] Deleting zone for yahoo.com.
```

## Documentation

```sh
indy@mac > ./cloudfish.py -h     
usage: cloudfish -d [domain] -k [globalkey] -e [email on cloudflare] -a [cloudflare account number]

Find subdomains with Cloudflare.

required arguments:
  -k ff86g56783...   Provide your Cloudflare global key
  -d example.com     Provide a domain to enumerate (no subdomains)
  -e john@email.com  Provide email on your Cloudflare account
  -a u3nd92ldhs...   Provide your Cloudflare account number

optional arguments:
  --verbose          Noisy output with banner and step by step updates
```

## Inspiration
Back in 2016, Matthew Bryant released [`cloudflare_enum`](https://github.com/mandatoryprogrammer/cloudflare_enum/), which made use of Cloudflare's automatic DNS scanner to find subdomains for pentesting against targets. I stumbled across Cloudflare's DNS scanner and eventually onto the [`cloudflare_enum`](https://github.com/mandatoryprogrammer/cloudflare_enum/) project. I realize it was completely broken given its age and wrote a new script using the Cloudflare API. Enjoy.  
