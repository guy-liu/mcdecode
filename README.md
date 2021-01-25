# mcdecode
A simple python script to decode URLs created by the Mimecast URL Protection feature.

## Problem
[URL Protection], part of the Mimecast Targetted Threat Protection email security product, offers end users an increased level of protection against malicious URLs embbed in emails. URLs in emails are replaced by unique URLs pointing to Mimecast servers, allowing various checks to be performed after a user has clicked on one of the links.

The problem comes when a user wishes to retrieve the original URL without first visiting it. This is a common scenario for technical personnels. For example, a help desk technician might wish to investigate the hyperlinks embeded in a suspected spam email, or a cyber security analyst might wish to investigate a malware delivery email by following the link in a sandboxed environment. Mimecast provides several methods for decoding URLS but each presents its own challenges:

### From an Enrolled Browser
The main issue with using the browser is that Mimecast automatically redirects you to the page. This is not a desireable behaviour if you suspect the link might take you to a malicious web site.
Also when Device Enrollment is configured, the encoded URL can only be decoded from a browser session which is enrolled. While device enrollment is quite straight forward, the enrollment status is not preserved in incognito/private browsing session. Also you are stuck if you want to use a command line tools such as curl or wget.

### Decode Tool on the URL Protection Dashboard
On the surface, this sounds really promising. However to use this, you need to be logged in to the Administration Console and navigate the web UI, which takes a lot of time considering that without the URL Protection feature, you only need to move the mouse over the link to see where it points to. Also the dashboard page is only accessible by admins.

### Use the Decode Function provided by the API
Mimecast has also very helpfully provided an [API] function that can be used to decode these URLs. This again is cumbersome without some additional wrapper script. Also you will need to supply an API authentication token, which is of course good security, but unfortunately also requires you to have admin level access.

### Use the Handy URL Preview Feature
I only came across this while writting this tool and I must admit that this is quite a handy feature, albeit not intuitive to use. Mimecast has a built-in [Preview URL] feature and to use you, you need to paste the URL into an enrolled browser with an additional '+' character at the end of the URL.
This is a great way to manually preview the URL, however the URL is actually an image, which is no good if you want to grab the URL as plain text to take to other systems. Also I feel this can be a bit accident prone - if you forgot to add the '+' or pressed Enter after paste you will be taken to the URL without further warning.

## Solution
After some basic investigation, it appears that the enrollment status of a browser is simply kept in a single session cookie. This can be easily exported to other systems or used in command line tools such as curl.

I decided to write a simple python script to simulate the URL decoding process that happens in an enrolled browser. But rather than follow the redirection to the original URL, the script simply displays that URL in the console. This allows me to quickly decode a URL on the command line to see what it is, and in a format that can then be copied and pasted.

The script requires a valid enrollment cookie "borrowed" from an already enrolled browser. I decided to implement a save option to save the cookie in a config file, so that the rather long and messy cookie values are not needed for subsequent uses.

### Extra Challenge
On Mimecast tenants that have user awareness training feature enabled, every so often, instead of decoding the URL in the browser, you are prompted to decide whether the URL is Safe or Unsafe. I initially thought since the URL is displayed on the page, I could just extract it from the page source code. However it turns out that the original URL is not actually included in the source code of the page as the entire page appears to be a JavaScript client. Further investigation showed that the JavaScript makes API calls to retrieve the various fields used on the page so I had to reverse engineer that process as well.

## Installation
No need to install. Simply download the python script and run. Requires python 3.

I wrote this on a Linux system, but this might run on Python 3 on Windows. If you have this working on Windows I would love to hear from you.

## Examples
Run the first decode, specify the URL (-u) and also a valid authentication cookie from an enrolled browser (-c) and save the cookie in a config file for future use. Please do not use the cookie in the example as it is not a valid cookie. 
```
$ ./mcdecode.py -u https://protect-eu.mimecast.com/s/4YYXx3RhcsBNOrkmt5hm -c x-mc-ea-o40zr1n2e8198tnm83avpkel5p6hra53=8BAABklWQvuP8sqJ78k2_sU87dP6P31eu0bmFqgthqziyHZrwy_xWlZekXtPcSg0fGUNL_sU87dP-OcNFoQpEXLLDvwgJ1LEBAnaeliHj92u7tI6tgXqyRDLSel6RqAoIVRjGiKU7GqqMHFj1CFQcaLJKSN4HQxr2r9Ziu1t_c17TMZEIU4BoPZ_3YTUROFG -s
https://github.com/guy-liu/mcdecode
```
The subsequent decodes only require the URL (-u).
```
$ ./mcdecode.py -u https://protect-eu.mimecast.com/s/4YYXx3RhcsBNOrkmt5hm 
https://github.com/guy-liu/mcdecode
``` 
You can also specify a different cookie (-c) as a one time value for testing, or in combination with the save cookie option (-s) to update the stored cookie in the config file. The config file is located at ~/.mcdecode 

Enjoy. 

[URL Protection]:https://community.mimecast.com/s/article/Targeted-Threat-Protection-URL-Protect-793832582

[API]:https://www.mimecast.com/tech-connect/documentation/endpoint-reference/targeted-threat-protection-url-protect/decode-url/

[Preview URL]:https://community.mimecast.com/s/article/Targeted-Threat-Protection-Verifying-a-URL-621586565
