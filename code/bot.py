from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
import requests
import asyncio
import discord
import random
import utils
import json
import time
import os


if not os.path.isfile('.env'):
	print('[!!] Missing .env file')
	exit()
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
ABUSE = os.getenv('ABUSE')
SERVE = os.getenv('HONEY')
HOSTN = os.getenv('HOSTN')
ARMED = True;
# Load client and Set command prefix
bot = commands.Bot(command_prefix = "$")

@bot.event
async def on_ready():
	guild = get(bot.guilds, name=GUILD)
	print(guild)
	print(f'{bot.user} has connected to Discord!')		
	print(f'{guild.name}(id: {guild.id})')

@bot.command(name='abusive-acts', pass_context=True)
async def list_abuse(ctx):
	#ID	Title	Description
	abusive=  { 1: 	'Altering DNS records resulting in improper redirection.',
				2 : 'Falsifying domain server cache (cache poisoning).',
				3 : 'Fraudulent orders.',
				4 : 'Participating in distributed denial-of-service (usually part of botnet).',
				5 : 'FTP Brute-Force', 	
				6 : 'Ping of Death/Oversized IP packets.',
				7 : 'Phishing websites and/or email.',
				8 : 'Fraud VoIP ',
				9 : 'Open proxy, open relay, or Tor exit node.',
				10: 'Comment/forum spam, HTTP referer spam, or other CMS spam.',
				11: 'Spam email content, infected attachments, and phishing emails.',
				12: 'CMS blog comment spam.',
				13: 'VPN IP',
				14: 'Scanning for open ports and vulnerable services.',
				15: 'Hacking ',
				16: 'Attempts at SQL injection.',
				17: 'Email sender spoofing.',
				18: 'Credential Stuffing',
				19: 'Bad Web Bot',
				20: 'Exploited Host, likely infected with malware and being used for other attacks or host content', 
				21: 'Web App Attack',
				22: 'Secure Shell (SSH) abuse.',
				23: 'Abuse was targeted at an "Internet of Things" type device.'}
	opts = ''
	for k in abusive.keys():
		opts+='%d: %s\n' % (k, abusive[k]) 
	await ctx.send(opts)


@bot.command(name='report', pass_context=True)
async def report_abuse(ctx, ip, comment, categories):
	# Defining the api-endpoint
	url = 'https://api.abuseipdb.com/api/v2/report'

	# String holding parameters to pass in json format
	params = {
	    'ip':'%s' % ip,
	    'categories':categories,
	    'comment': comment
	}

	headers = {
	    'Accept': 'application/json',
	    'Key': '$%s' % ABUSE
	}
	
	response = utils.cmd(cmd,True)
	await ctx.send(json.dumps(params))
	response = requests.request(method='POST', url=url, headers=headers, params=params)
	print(headers)
	# # Formatted output
	await ctx.send('```'+json.dumps(response.text)+'```')

async def check_alarm(ctx,filename,n):
	print('[-] Checking Alarm File')
	while ARMED:
			await asyncio.sleep(30)
			try:
				c = f"sftp {HOSTN}@{SERVE}:/home/{HOSTN}/HomeAlone/code/logs <<< $'get {filename}'"
				utils.arr2str(utils.cmd(c,False))
				N = int(utils.cmd("cat %s| grep 'Connection at ' | wc -l" % filename, False).pop())
				if N > n:
					m = '{0.author.mention} **New Connection <a:siren:833794872204722248> **'.format(ctx.message)
					m += '```' + utils.arr2str(utils.cmd(f"tail -n 10 {filename} ",False))+'```'
					await ctx.send(m)
			except IndexError:
				print('[!] Unable to read log file')
				pass

@bot.command(name='kill-honey', pass_context=True)
async def kill_process(ctx):
	c = 'sudo kill -9 $(pid of python)'
	utils.cmd(c,False)
	await ctx.send()


@bot.command(name='alert-me', pass_context=True)
async def set_alarm(ctx, filename):
	try:
		c = f"sftp {HOSTN}@{SERVE}:/home/{HOSTN}/HomeAlone/code/logs <<< $'get {filename}'"
		utils.arr2str(utils.cmd(c,False))
		n = int(utils.cmd("cat %s| grep 'Connection at ' | wc -l" % filename, False).pop())
		await ctx.send('*Setting Alarm on %s*, which currently has **%d** entries.' % (filename, n))
		ARMED = True
		bot.loop.create_task(check_alarm(ctx,filename,n))
	except:
		c = 'ssh %s@%s ls -la HomeAlone/code/logs'% (HOSTN,SERVE)
		result = 'Something went wrong... Select one of these to set alarm on:\n'
		result += '```' + (utils.arr2str(utils.cmd(c,False)))+'```'	
		pass


@bot.command(name='disarm',pass_context=True)
async def disable_alarm(ctx):
	ARMED = False
	await ctx.send('**Disabling Alarm on %s**' % (filename, n))


@bot.command(name='list-logs',pass_context=True)
async def list_log_files(ctx):
	await ctx.send('*Getting list of log files*')
	c = 'ssh %s@%s ls -la HomeAlone/code/logs'% (HOSTN,SERVE)
	result = '```' + (utils.arr2str(utils.cmd(c,False)))+'```'
	try:
		await ctx.send(result)
	except:
		print(result)
		pass

@bot.command(name='list-cnx', pass_context=True)
async def show_connection(ctx):
	msg = 'Aw Geez, lets see who is connected <:morty:833787268148887623>'.format(ctx.message)
	await ctx.send(msg)
	c = 'ssh %s@%s netstat -antup'% (HOSTN,SERVE)
	result = '```' + (utils.arr2str(utils.cmd(c,False)))+'```'
	try:
		await ctx.send(result)
	except:
		print(result)
		pass


async def ping_user(ctx):
	m = "{0.author.mention}".format(ctx.message)
	await ctx.send(m)



@bot.command(name='lookup',pass_context=True)
async def ipinfo(ctx, ip):
	link = 'http://ipinfo.io/%s'%ip
	response = requests.request(method='GET', url=link)
	await ctx.send('```'+json.dumps(response.text).replace('\n','')+'```')


@bot.command(name='read-log', pass_context=True)
async def read_log(ctx, filename):
	c = f'ssh {HOSTN}@{SERVE} ls HomeAlone/code/logs'
	if filename in utils.cmd(c,False):
		await ctx.send('**This will take a minute...**')
		c = f"sftp {HOSTN}@{SERVE}:/home/{HOSTN}/HomeAlone/code/logs <<< $'get {filename}'"
		utils.arr2str(utils.cmd(c,False))
		f = open(filename, 'r')
		while True:
			piece = f.read(1024)  
			if not piece:
				break
			try:
				await ctx.send('```\n'+piece+'\n```')
				time.sleep(3)
			except:
				print(result)
				pass
		f.close()
		os.remove(filename)
	else:
		await ctx.send("I can't find %s" % filename)

@bot.command(name='clear', pass_context=True)
async def clean(ctx, arg):
	# Clear messages from the the last <args> minutes
	passed = 0
	failed = 0
	async for msg in ctx.message.channel.history(limit=int(arg)):
		try:
			await msg.delete()
			passed += 1
		except:
			failed += 1
	print(f"[Complete] Removed {passed} messages with {failed} fails")


def main():
	bot.run(TOKEN)

if __name__ == '__main__':
	main()
