# mcdecode
A simple python script to decode URLs created by the Mimecast URL Protect feature.

## Purpose

[URL Protect], part of the Mimecast Targetted Threat Protection email security product, offers end users an increased level of protection against malicious URLs embbed in emails. URLs in emails are replaced by unique URLs pointing to Mimecast servers, allowing various checks to be performed after a user has clicked on one of the links.

When Device Enrollment is configured, the encoded URL can only be decoded from a browser session which is enrolled. While device enrollment is quite straight forward, it does add a level of admin overhead for users who tend to use multiple devices/browsers. However device enrollment does have some limitations:

  - The enrollment status is not perserved for incognito/private browsing sessions
  - Command line clients such as curl is not supported

For technical personnels who needs to inspect these URLs in disposable sandboxed environments or using command line tools, these limitations can become very frustrating.

Mimecast does provide a number of ways to decode the URLs.

  - Use the decode tool on the URL Protection Dashboard
    This requires logging to the Administration Console which again takes time. Also the dashboard page is only accessible to admins.

  - Use the [API Endpint]
    This is cumbersome without some additional wrapper script. Also an API token is required, which again has to be created by an admin.

  - [Verify URL] by appending '+' in an enrolled browser
    This is probably the easiest method, if an already enrolled browser is easily accessible. However this method becomes very time consuming when multiple URLs need to be decoded in bulk


[URL Protect]:https://community.mimecast.com/s/article/Targeted-Threat-Protection-URL-Protect-793832582

[API Endpoint]:https://www.mimecast.com/tech-connect/documentation/endpoint-reference/targeted-threat-protection-url-protect/decode-url/

[Verify URL]:https://community.mimecast.com/s/article/Targeted-Threat-Protection-Verifying-a-URL-621586565
https://protect-eu.mimecast.com/s/aRiFCkZJmSQZo5h2iMzf?domain=github.com
