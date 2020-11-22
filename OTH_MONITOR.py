import requests, json, lxml, time, discord
from discord_webhook import DiscordWebhook, DiscordEmbed
from bs4 import BeautifulSoup as bs

def monitor():
    list_of_notified_raffles = []
    while True:
        print ('Monitoring OTH Raffles...')
        s = requests.Session()
        url = 'https://offthehook.ca/pages/raffles'
        headers = {
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
            }
        raffle_list = s.get(url, headers=headers)
        soup = bs(raffle_list.text, 'lxml')
        existing_raffle_list = soup.find('div', {'class':'rte'})
        for data in existing_raffle_list('p'):
            #print (data.text)
            try:
                raffle_name = data.text
                if "ENDED" in raffle_name:
                    pass
                else:
                    if raffle_name in list_of_notified_raffles:
                        print ('Found in Notified Raffles Already, Should be moving on...')
                        pass
                    else:
                        raffle_link = data.a.get('href')
                        print ('Found Live Raffle! {}'.format(raffle_name))
                        raffle_page = s.get(raffle_link, headers=headers)
                        soup = bs(raffle_page.text, 'lxml')
                        picture_frame = soup.find('div', {'class':'rte'})
                        try:
                            product_image = picture_frame.img.get('src')
                            print ('IMAGE URL: {}'.format(product_image))
                        except:
                            print ('Error Finding Product Image')
                            pass
                        webhook_url = 'https://discordapp.com/api/webhooks/695274168647680022/PeB-ymh35O_c_OOGZuviz8edcFq8hCu0WYTZcB1qmmSySbc5LiYPJ51p3vmXA1lxdNew'
                        webhook = DiscordWebhook(url=webhook_url)
                        embed = DiscordEmbed(title='{}'.format(raffle_name), url='{}'.format(raffle_link), color=10181046)
                        embed.add_embed_field(name='Region:', value='CA')
                        embed.add_embed_field(name='Site:', value='OFFTHEHOOK')
                        embed.add_embed_field(name='Release Type:', value='ONLINE')
                        embed.add_embed_field(name='Closes', value='UNKNOWN')
                        embed.add_embed_field(name='Entry', value='[Click Here]({})'.format(raffle_link))
                        embed.set_thumbnail(url='{}'.format(product_image))
                        embed.set_footer(text='Made by alin#8437')
                        embed.set_timestamp()
                        webhook.add_embed(embed)
                        webhook.execute()
                        list_of_notified_raffles.append(raffle_name)
                        print ('Change Detected! Sending Notification to Discord!')
                        time.sleep(2)
            except:
                print ('Exception Error')
                pass
        time.sleep(10)
            

monitor()
