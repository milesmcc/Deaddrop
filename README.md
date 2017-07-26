# Deaddrop
Secure, authenticated, and monitored file 'dead drops'

![Secure access code](images/1.png)
![Security questions](images/2.png)
![Security questions](images/5.png)

## Abbreviated features
* Hide files behind personal information, not passwords.
* Log downloads and login attempts.
* No Javascript required
* Time-based and download-based file expiration.
* Sender anonymity
* House-Of-Cards style(see LeAnn Harvey and Aidan MacAllen)
* 100% open source

## Potential use cases
* You want to make information available to one person, and one person only, but do not trust their email and want to ensure that only *they* are able to gain access to the files.
* You're unsatisfied with the level of logging that Dropbox or Google Drive provides.
* You want the files to expire after a single download.
* You want the files to expire after a certain period of time.
* ...or any combination of the above.

*Security questions aren't required, so it's possible to use Deaddrop as a super-monitored version of Dropbox or Google Drive.*

## Setting it up
Deaddrop is a pure Django app, and runs smoothly on both Python 2 and Python 3. Make sure to change the secret in `settings.py`, and be sure to turn `DEBUG` to `False`. Make sure that you use HTTPS to ensure that data is encrypted in transit.

For security, **make sure you do the following things before deployment:**
* Enable HSTS
* Change the Django secret
* Enable: `SECURE_CONTENT_TYPE_NOSNIFF`, `SECURE_BROWSER_XSS_FILTER`, `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`
* Set `X_FRAME_OPTIONS` to `DENY`
* Generally secure the production machine, because as of right now, DATA IS NOT ENCRYPTED AT REST.

It's possible to simply copy-and-paste the following settings into the beginning of your `settings.py` file, however you should also be sure to remember to change the secret key value!

```
# Special security settings for production hardening
SECURE_HSTS_SECONDS = 3600
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SECURE = True
```

If you want to be hardcore, you can also enable HTTPS HSTS preloading, however only do so if you're sure (and if you're OK with your Deaddrop url not being private)!

*These settings aren't default to make debugging and development quicker and easier. The default `settings.py` is NOT suitable for production use!*

## Caveats
* Data is not encrypted at rest (on roadmap to fix, in the meantime, encrypt your uploads in .ZIP files!)
* Answers to security questions are stored as plaintext (on roadmap to fix)
* There aren't extensive unit tests
* Still a beta-level product - **use with caution**

Apart from these concerns, however, Deaddrop was designed with security as its top priority. The session/authentication system has been seriously vetted. It is also worth noting that the two caveats are only problematic once the server and the filesystem itself is compromised.

If you have found a security vulnerability, please either create an issue or **contribute a fix!**

## Extended screenshots
![another screenshot](images/1.png)
**Secure access code entry page.**

![another screenshot](images/2.png)
**Identity verification page.**

![another screenshot](images/4.png)
**Identity verification page with incorrect response.**

![another screenshot](images/5.png)
**Drop index.**

![another screenshot](images/6.png)
**Example drop page.**

![another screenshot](images/9.png)
**Logged out message.**

![another screenshot](images/10.png)
**Incorrect/invalid secure access code.**

![another screenshot](images/7.png)
**Authenticated toolbar status.**

![another screenshot](images/8.png)
**Unauthenticated toolbar status.**
