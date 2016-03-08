import sys
import click

#import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

#set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

@click.command()
@click.argument('inp_text', required=False)
@click.option('--server', default='localhost:5000', help='ip:port to connect to')
def cli(server, inp_text):

    if not inp_text:
        inp_text = click.get_text_stream('stdin').read()
    #print(inp_text)
    # Send request to server with user input text and user's wallet address for payment
    sel_url = 'http://' + server + '/sentiment?text={0}&payout_address={1}'
    sel_url = sel_url.format(inp_text, wallet.get_payout_address())
    response = requests.get(url=sel_url)

    # Print the translated text out to the terminal
    click.echo(response.text)
