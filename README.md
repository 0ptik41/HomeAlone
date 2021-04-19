# Home Alone 
A simple and open source honeypot system for detecting and tracking live threats on the internet. 

	- Logging the requests being made, the addresses and the time.
	- Discord bot to interact with the honeypot and see whats happening in real time.
More features to come.

## Logging 
Requests to the server are logged by date/time (files created each time you start honeypot).
Here's an example of some of the malicious traffic I've seen: 

```
====================================================================
Connection at 4/19/2021 - 0:41:23 :
{"5.178.86.76" : "b'POST http://check.best-proxies.ru/azenv.php?s=VJVJVDNRIJOOVEVCPRNRPJUONNURYR HTTP/1.1\r\nHost: check.best-proxies.ru\r\nCookie: testCookie=true\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0\r\nReferer: https://best-proxies.ru/\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: 13\r\nConnection: close\r\n\r\ntestPost=true\r\n\r\n'"
================================================================================
Connection at 4/19/2021 - 0:41:28 :
{"5.178.86.74" : "b'CONNECT 5.178.86.76:80 HTTP/1.1\r\nHost: check.best-proxies.ru:80\r\n\r\n'"
================================================================================
Connection at 4/19/2021 - 0:41:33 :
{"5.178.86.78" : "b'\x04\x01\x00P\x05\xb2VL0\x00'"
================================================================================
```

## Discord Bot 
Using the discord bot you can retrieve and view these logs in real time as well as do GeoIP lookups:
```
"{\n  \"ip\": \"211.40.129.246\",\n  \"city\": \"Seonghwan\",\n  \"region\": \"Chungcheongnam-do\",\n  \"country\": \"KR\",\n  \"loc\": \"36.9156,127.1314\",\n  \"org\": \"AS3786 LG DACOM Corporation\",\n  \"postal\": \"31014\",\n  \"timezone\": \"Asia/Seoul\",\n  \"readme\": \"https://ipinfo.io/missingauth\"\n}"

"{\n  \"ip\": \"46.43.113.22\",\n  \"hostname\": \"adsl-46.43.113.22.mada.ps\",\n  \"city\": \"Ramallah\",\n  \"region\": \"West Bank\",\n  \"country\": \"PS\",\n  \"loc\": \"31.8996,35.2042\",\n  \"org\": \"AS51407 Mada ALArab LTD\",\n  \"timezone\": \"Asia/Hebron\",\n  \"readme\": \"https://ipinfo.io/missingauth\"\n}"
```

**working on a feature for automated reporting to AbuseIPDB.com **