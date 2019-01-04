# How I hacked Altervista.org
By @jacopoMii (https://www.facebook.com/jacopotediosi)<br>
How I hacked Altervista.org, and I found a vulnerability that allowed to steal access tokens

## Foreword
This was the first bounty I attended, and this is my first writeup in English.<br>
I'm just an Italian student with a strong wish to learn new IT-Security stuffs and with a strong belief about ethical hacking.<br>
If someone finds errors or wants to give me suggestions, please open here an issue or a pull request.

## About Altervista.org
From [Wikipedia](https://it.wikipedia.org/wiki/AlterVista):
>  AlterVista is an Italian web platform where you can open a website for free.
>  On AlterVista you can create a website with PHP, MySQL database and FTP access.
>  Use of the space is free but some additional services are subject to charges.
>  Altervista was bought by Mondadori spa in 2016 and today it hosts about 3 million sites.

Altervista allows you to manage your website via a comfortable web panel after having logged in.

Altervista also has a [forum](http://forum.it.altervista.org/) where people can ask for programming questions and participate in community life:
![The Altervista forum](https://raw.githubusercontent.com/jacopotediosi/Writeups/master/Real/Altervista.org/img1.png)

## How the login system works
I wandered on Altervista for a while, until I noticed that if you had already logged in to the administration panel of your site, to log in on the forum you just have to click on the "Login" button, without having to retype your credentials; so I started studying how that button works:

It was a simple link for `https://aa.altervista.org/?client_id=altervista&response_type=code&redirect_uri=http://forum.it.altervista.org/`

If you have already authenticated, that page does nothing more than generate an "authorization_code" and then redirect you to `http://forum.it.altervista.org/login.php?do=login-aHR0cDovL2ZvcnVtLml0LmFsdGVydmlzdGEub3JnL2ZvcnVtLnBocA%3D%3D&authorization_code=XXXXXXXXXXXXXXXXXXX`<br>
The strange parameter "do" contains the word "login" and then the link "http://forum.it.altervista.org/forum.php" coded in base64 (I know, that's a strange choice).<br>
Parameter "authorization_code" contains the "authorization_code" generated before.<br>
If you haven't authenticated yet, it first asks you for your username and password and then redirects you in the same way.

## How I came to discover the vulnerability
The vulnerability is that if we can change the value of the "redirect_uri" get-parameter, we can create a special link that if clicked redirects the user to our servers instead of the altervista server, allowing us to steal the authorization_code that is added at the end of the url (and then login with profile of other people).

Unfortunately there seemed to be a filter on the parameter, which accepted only subdomains of it.altervista.org.

At this point I remembered a video of [LiveOverflow](https://www.youtube.com/channel/UClcE-kVhqyiHCcjYwcpfj9w):  "[HOW FRCKN' HARD IS IT TO UNDERSTAND A URL?!](https://www.youtube.com/watch?v=0uejy9aCNbI)", where he shows that often programmers make mistakes when they have to parse urls, especially when the input is not compliant with specifications.

Then I started fuzzing, until I found a way to bypass the filter:<br>
`https://aa.altervista.org/?client_id=altervista&response_type=code&redirect_uri=http://google.it/http://it.altervista.org/`

It redirects you as follow: ![We can steal access token](https://raw.githubusercontent.com/jacopotediosi/Writeups/master/Real/Altervista.org/img2.png)

So if instead of google.it we put our malicious server address here, we can steal the access token.<br>
And then login with it: `http://forum.it.altervista.org/login.php?do=login-aHR0cDovL2ZvcnVtLml0LmFsdGVydmlzdGEub3JnL2ZvcnVtLnBocA%3D%3D&authorization_code=XXXXXXXXXXXXXXXXXXX`

![enter image description here](https://raw.githubusercontent.com/jacopotediosi/Writeups/master/Real/Altervista.org/img3.png)

## Epilogue
I immediately reported my discovery to Altervista through [the appropriate form](https://it.altervista.org/feedback.php?who=feedback), and they fixed it almost immediately.<br>
As a reward, they added my name to the [thanks list](https://it.altervista.org/ringraziamenti.php): ![enter image description here](https://raw.githubusercontent.com/jacopotediosi/Writeups/master/Real/Altervista.org/img4.png)

## Timeline
- 02 January 2018: Started looking for vulnerabilities on Altervista.org
- 03 January 2018: Discovered vulnerability and sent a PoC to Security Team
- 04 January 2018: Patch went online and my name was added to thanks list
