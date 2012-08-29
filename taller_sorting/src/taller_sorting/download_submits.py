import poplib
import base64
import email
import os
import shelve
import sys
import pickle
import imaplib

from time import sleep
from getpass import getpass
import re

here= os.path.dirname(os.path.abspath(__file__))
def get_imap_connection(user):
    password= getpass()

    imap_connection= imaplib.IMAP4_SSL('imap.gmail.com', 993)
    imap_connection.login(user, password)
    return imap_connection

def download_submits(user):
    mail_pattern= re.compile(r"(?P<mail>[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6})")
    imap_connection= get_imap_connection(user)

    imap_connection.select(mailbox='taller sorting')
    typ, data = imap_connection.search(None, 'ALL')
    mails= data[0].split()
    people= []
    for i, num in enumerate(reversed(mails)):
    #for i, num in enumerate(mails[index:]):

        typ, data = imap_connection.fetch(num, '(RFC822)')
        e= email.message_from_string(data[0][1])
        sender= None
        for k, v in e.items():
            if k == 'From':
                m= mail_pattern.search(v)
                if m is None: import ipdb;ipdb.set_trace()
                sender= m.groupdict()['mail']

        #import ipdb;ipdb.set_trace()

        cd= 'Content-Disposition'
        for p in e.walk():
            if cd in p and re.search('filename=".*?.py"', p[cd]):
                encoding= p.get('Content-Transfer-Encoding')
                if encoding == 'base64':
                    payload= base64.decodestring(p.get_payload())
                else:                        
                    payload= p.get_payload()
                yield sender, payload


    imap_connection.close()
    imap_connection.logout()

def main():
    username= sys.argv[1]
    
    iter= download_submits(username)
    algorithms_dir= os.path.join(here, 'sorting_algorithms')
    downloaded= set()
    for i, (sender, submit_content) in enumerate(iter):
        print sender 
        if sender in downloaded: continue
        downloaded.add(sender)
        sender= sender[:sender.find('@')]
        with open(os.path.join(algorithms_dir, sender.replace('.','_') + '.py'), 'w') as f:
            f.write(submit_content)

    
def prune_contacts(contacts):
    c.endswith('mail.gmail.com')
    cs= [c for c in cs if len(c) <= 37]

if __name__ == '__main__':
    main()
