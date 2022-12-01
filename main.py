import requests, datetime, itertools, time, os, binascii, random, threading, tls_client

colorsPool = itertools.cycle([27, 33, 69, 74, 74, 73, 73, 73, 78, 114, 114, 113, 113, 155, 155, 155, 155, 155, 155, 191, 191, 185, 185, 185, 185, 185, 185, 221, 221, 221, 221, 221, 215, 215, 215, 209, 209, 209, 203, 203, 203, 204, 204, 204, 198, 198, 129, 129, 135, 99, 99, 99, 99, 63, 63, 63, 63, 69, 69, 69])

def cout(input):
    print('[\x1b[38;5;%sm%s\x1b[0m] %s' % (next(colorsPool), datetime.datetime.now().strftime('%H:%M:%S'), input))

class Main:
    def __init__(self):
        self.watchingToken = 'x'
        self.snitchingToken = 'x'
        self.capmonsterKey = 'x'
        self.websiteUrl = 'https://discord.com/'
        self.websiteKey = 'a9b5fb07-92ff-493f-86fe-352a2803b3df'
        self.proxy = ''
        self.userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        self.guildSettings = [
            {
                'guildId': 1,
                'snitchMessage': ':warning: **You joined a fake MM** :warning: \n:exclamation:The server you joined (** %s**), it\'s a **SCAM** and is **BOTTED**\n:white_check_mark: Use a trusted middleman such as: ** discord.gg/auto **\nFOR MORE PROOF DM "++;#0277"\nSome proof: Scroll far down in the members list and check registration and join dates of accounts, they\'re all similar (Botted), check total messages in vouches channel, they\'re too low for such a big server'
            }
        ]
        self.webhook = 'x'
        with open('tokens.txt', 'r', encoding = 'UTF-8') as file:
            self.tokenPool = itertools.cycle(file.read().splitlines())

    def getCaptcha(self, rqdata):
        json = {
            'clientKey': self.capmonsterKey,
            'task': {
                'type': 'HCaptchaTaskProxyless',
                'websiteURL': self.websiteUrl,
                'websiteKey': self.websiteKey,
                'userAgent': self.userAgent,
                'data': rqdata
            }
        }
        json = {
            'clientKey': self.capmonsterKey,
            'taskId': requests.post('https://api.capmonster.cloud/createTask', json = json).json()['taskId']
        }
        while True:
            response = requests.post('https://api.capmonster.cloud/getTaskResult', json = json)
            if response.json()['status'] == 'ready':
                return response.json()['solution']['gRecaptchaResponse']
            time.sleep(3)

    def getCfBm(self):
        response = requests.get('https://discord.com/register').text
        json = {
            'm': response.split(',m:\'')[1].split('\',s:')[0],
            'results': [
                str(binascii.b2a_hex(os.urandom(16)).decode('UTF-8')),
                str(binascii.b2a_hex(os.urandom(16)).decode('UTF-8'))
            ],
            'timing': random.randint(40, 180),
            'fp': {
                'id': 3,
                'e': {
                    'r': [
                        1920,
                        1080
                    ],
                    'ar': [
                        1054,
                        1920
                    ],
                    'pr': 1,
                    'cd': 24,
                    'wb': False,
                    'wp': False,
                    'wn': False,
                    'ch': True,
                    'ws': False,
                    'wd': False
                }
            }
        }
        return requests.post('https://discord.com/cdn-cgi/bm/cv/result?req_id=%s' % response.split('r:\'')[1].split('\',s')[0], json = json).cookies.get('__cf_bm')

    def getCookie(self):
        cookie = str(requests.get('https://discord.com/app').cookies)
        return cookie.split('dcfduid=')[1].split(' ')[0], cookie.split('sdcfduid=')[1].split(' ')[0], cookie.split('cfruid=')[1].split(' ')[0], self.getCfBm()

    def createSession(self, token):
        # session = requests.Session()
        session = tls_client.Session(client_identifier = 'chrome_105')
        session.headers.update({
            'accept': '*/*',
            'accept-encoding': 'application/json',
            'accept-language': 'en-US,en;q=0.8',
            'authorization': token,
            'cookie': '__dcfduid=%s; __sdcfduid=%s; __cfruid=%s; locale=en-US; __cf_bm=%s' % self.getCookie(),
            'referer': 'https://discord.com/channels/@me',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': self.userAgent,
            'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNy4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA3LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE1ODE4MywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='
        })
        return session

    def blacklistUser(self, userId, guildId):
        with open('Blacklist/%s.txt' % str(guildId), 'a', encoding = 'UTF-8') as file:
            file.write('%s\n' % userId)

    def getGuildChannels(self, guildId):
        session = self.createSession(self.watchingToken)
        return session.get('https://discord.com/api/v9/guilds/%s/channels' % guildId).json()

    def getChannel(self, userId):
        json = {
            'recipients': [userId]
        }
        session = self.createSession(self.snitchingToken)
        return session.post('https://discord.com/api/v9/users/@me/channels', json = json).json()['id']

    def snitch(self):
        detectedChannels = []
        while True:
            for guildSetting in self.guildSettings:
                try:
                    guildId = guildSetting['guildId']
                    open('Blacklist/%s.txt' % guildId, 'a+', encoding = 'UTF-8').close()
                    for channel in self.getGuildChannels(guildId):
                        users = []
                        with open('Blacklist/%s.txt' % guildId, 'r', encoding = 'UTF-8') as file:
                            for user in file.read().splitlines():
                                users.append(int(user))
                        for permission in channel['permission_overwrites']:
                            if permission['type'] == 1:
                                permissionId = int(permission['id'])
                                if permissionId not in users:
                                    channelName = channel['name']
                                    if channelName not in detectedChannels:
                                        cout('Ticket detected -> %s' % channelName)
                                        detectedChannels.append(channelName)
                                    guildName = self.createSession(self.watchingToken).get('https://discord.com/api/v9/guilds/%s' % guildId).json()['name']
                                    session = self.createSession(self.snitchingToken)
                                    response = session.get('https://discord.com/api/v9/users/%s' % permissionId).json()
                                    userTag = '%s#%s' % (response['username'], response['discriminator'])
                                    cout('User detected -> %s' % userTag)
                                    json = {
                                        'content': 'Your ticket: <#%s>\n%s' % (channel['id'], guildSetting['snitchMessage'] % guildName)
                                    }
                                    response = session.post('https://discord.com/api/v9/channels/%s/messages' % self.getChannel(permissionId), json = json)
                                    if response.status_code == 200:
                                        cout('DMed %s.' % userTag)
                                        self.blacklistUser(permissionId, guildId)
                                        json = {
                                            'content': 'Hit raped. :yum:',
                                            'embeds': [
                                                {
                                                    'color': 161791,
                                                    'author': {
                                                        'name': 'Success'
                                                    },
                                                    'footer': {
                                                        'text': 'Hit Fucker'
                                                    },
                                                    'timestamp': str(datetime.datetime.utcnow()),
                                                    'fields': [
                                                        {
                                                            'name': 'Type',
                                                            'value': 'DM'
                                                        },
                                                        {
                                                            'name': 'Tag | User ID',
                                                            'value': '%s | %s' % (userTag, permissionId)
                                                        },
                                                        {
                                                            'name': 'Guild Name | Guild ID',
                                                            'value': '%s | %s' % (guildName, guildId)
                                                        },
                                                        {
                                                            'name': 'Ticket',
                                                            'value': channelName
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                        requests.post(self.webhook, json = json)
                                    # if 'captcha' in response.text:
                                    #     rqdata = response.json()['captcha_rqdata']
                                    #     json = {
                                    #         'content': guildSetting['snitchMessage'],
                                    #         'captcha_key': self.getCaptcha(rqdata),
                                    #         'captcha_rqtoken': rqdata
                                    #     }
                                    #     session.post('https://discord.com/api/v9/channels/%s/messages' % self.getChannel(permissionId), json = json)
                                    elif 'captcha' in response.text:
                                        self.blacklistUser(permissionId, guildId)
                                        json = {
                                            'embeds': [
                                                {
                                                    'color': 16721703,
                                                    'author': {
                                                        'name': 'Error'
                                                    },
                                                    'footer': {
                                                        'text': 'Hit Fucker'
                                                    },
                                                    'timestamp': str(datetime.datetime.utcnow()),
                                                    'fields': [
                                                        {
                                                            'name': response.status_code,
                                                            'value': str(response.json())
                                                        },
                                                        {
                                                            'name': 'Tag | User ID',
                                                            'value': '%s | %s' % (userTag, permissionId)
                                                        },
                                                        {
                                                            'name': 'Guild Name | Guild ID',
                                                            'value': '%s | %s' % (guildName, guildId)
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                        requests.post(self.webhook, json = json)
                                    else:
                                        self.blacklistUser(permissionId, guildId)
                                        json = {
                                            'embeds': [
                                                {
                                                    'color': 16721703,
                                                    'author': {
                                                        'name': 'Error'
                                                    },
                                                    'footer': {
                                                        'text': 'Hit Fucker'
                                                    },
                                                    'timestamp': str(datetime.datetime.utcnow()),
                                                    'fields': [
                                                        {
                                                            'name': response.status_code,
                                                            'value': str(response.json())
                                                        },
                                                        {
                                                            'name': 'Tag | User ID',
                                                            'value': '%s | %s' % (userTag, permissionId)
                                                        },
                                                        {
                                                            'name': 'Guild Name | Guild ID',
                                                            'value': '%s | %s' % (guildName, guildId)
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                        requests.post(self.webhook, json = json)
                                        for _ in range(20):
                                            threading.Thread(target = self.friend, args = (permissionId,)).start()
                                        json = {
                                            'content': 'Hit raped. :yum:',
                                            'embeds': [
                                                {
                                                    'color': 161791,
                                                    'author': {
                                                        'name': 'Success'
                                                    },
                                                    'footer': {
                                                        'text': 'Hit Fucker'
                                                    },
                                                    'timestamp': str(datetime.datetime.utcnow()),
                                                    'fields': [
                                                        {
                                                            'name': 'Type',
                                                            'value': 'Mass friend'
                                                        },
                                                        {
                                                            'name': 'Tag | User ID',
                                                            'value': '%s | %s' % (userTag, permissionId)
                                                        },
                                                        {
                                                            'name': 'Guild Name | Guild ID',
                                                            'value': '%s | %s' % (guildName, guildId)
                                                        },
                                                        {
                                                            'name': 'Ticket',
                                                            'value': channelName
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                        requests.post(self.webhook, json = json)
                except:
                    continue
            time.sleep(15)

    def getProxy(self):
        return {
            'http': 'http://%s' % self.proxy,
            'https': 'http://%s' % self.proxy
        }

    def friend(self, userId):
        try:
            session = self.createSession(next(self.tokenPool))
            response = session.put('https://discord.com/api/v9/users/@me/relationships/%s' % userId, json = {}) # proxy = self.getProxy()
            if response.status_code == 429:
                time.sleep(response.json()['retry_after'])
                session.put('https://discord.com/api/v9/users/@me/relationships/%s' % userId, json = {}) # proxy = self.getProxy()
            # if 'captcha' in response.text:
            #     rqdata = response.json()['captcha_rqdata']
            #     json = {
            #         'captcha_key': self.getCaptcha(rqdata),
            #         'captcha_rqtoken': rqdata
            #     }
            #     session.put('https://discord.com/api/v9/users/@me/relationships/%s' % userId, json = json)
        except:
            pass

    def run(self):
        self.snitch()

if __name__ == '__main__':
    os.system('cls')
    Main().run()
