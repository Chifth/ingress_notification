#!/usr/bin/env python3

import sys, os
import threading
from imaplib2 import imaplib2
import email
from email.header import decode_header
import logging, logging.config, json
import pprint


### Logger settings ###
if __debug__:
    lg = logging.getLogger('debugger')
else:
    lg = logging.getLogger()

pp = pprint.PrettyPrinter(indent=2)



### Main Class ###
class MailChecker(threading.Thread):
    waitingEvent = threading.Event()
    imap = None
    old_mails = set()
    raw_mail_handler = None
    kill_now = False
    timeout = 0

    @staticmethod
    def plain_text_from_raw_email(raw_email):
        """
        Extract (to, from, subject, contents) of a given raw_email using
        'email' module. Contents only contains "text/plain" part. Other
        parts will be ignored.
        """
        lg.debug('start plain_text_from_raw_email')
        lg.debug("raw_email = {}".format(raw_email))
        mail = email.message_from_string(raw_email)

        _to = ''
        _from = ''
        _subject = ''
        _msg = ''

        if mail['To']:
            _to = mail['To']

        if mail['From']:
            _from = mail['From']

        # Extract the subject.
        encoded_subject = mail['Subject']
        lg.debug("encoded_subject = {!r}".format(encoded_subject))
        if encoded_subject:
            headers = decode_header(encoded_subject)
            lg.debug("headers = {}".format(pp.pformat(headers)))
            # If mutliple encodings are used in subject, the list headers will
            # have many tuples in the form of (text, encode_method).
            for (s, enc) in headers:
                # Encode is not necessary if s is str not bytes
                if isinstance(s, bytes):
                    if enc: # enc could be None
                        s = s.decode(enc)
                    else:
                        s = s.decode()
                _subject += s

        # Extract contents. (only text/plain type).
        for part in mail.walk():
            lg.debug("type = {}".format(part.get_content_type()))
            lg.debug("\t {!r}".format(part.get_payload()))
            if part.get_content_type() == 'text/plain':
                _msg = part.get_payload(decode=True).decode(part.get_content_charset())

        return (_to, _from, _subject, _msg)

    @staticmethod
    def content_cleanup(msg):
        msg = msg.split('\n')
        new_msg = []
        for m in msg:
            if m not in ['\r', '\n', '']:
                if m[-1] == '\r':
                    m = m[:-1]
                new_msg.append(m)
        return new_msg

    def __init__(self, username, password,
            server='imap.gmail.com',
            timeout=60,
            raw_mail_handler=lambda *args : None):
        threading.Thread.__init__(self)
        lg.info('MailChecker object initialized.')
        lg.info('username = %s', username)
        lg.debug('password = %s', password)
        self.imap = imaplib2.IMAP4_SSL(server)
        self.timeout = timeout
        self.raw_mail_handler = raw_mail_handler
        try:
            typ, data = self.imap.login(username, password)
            self.imap.select('INBOX')
            typ, data = self.imap.SEARCH(None, 'ALL')
            self.old_mails = set(data[0].split())
        except:
            lg.error('Could\'t connect to IMAP server.')
            sys.exit(1)
        lg.info('Found %d mails.', len(self.old_mails))
        lg.debug('Exists mails:')
        lg.debug(self.old_mails)

    def run(self):
        lg.info('Running MailChecker.')
        while not self.kill_now:
            self.wait_for_new_mail()
        lg.info('Stop running MailChecker.')

    def kill(self):
        lg.info('Killing MailChecker.')
        self.kill_now = True
        self.waitingEvent.set()

    def _get_raw_email_from_fetched_data(self, data):
        for i in range(len(data)):
            if isinstance(data[i], tuple):
                return data[i][1]

    def wait_for_new_mail(self):
        lg.info('Waiting for new mails....')
        self.waitingEvent.clear()
        callback_normal = True
        def _idle_callback(args):
            lg.info("imap.idle callback with args {!r}".format(args))
            try:
                if args[0][1][0] == ('IDLE terminated (Success)'):
                    lg.info('Got a new mail or timeout')
                    self.callback_normal = True
                else:
                    lg.info('imap.idle callback abnormally')
                    self.callback_normal = False
            except TypeError:
                lg.error('imap.idle callback abnormally')
                self.callback_normal = False
            self.waitingEvent.set()
        self.imap.idle(timeout=self.timeout, callback=_idle_callback)
        self.waitingEvent.wait()
        lg.info('Waiting ended.')
        if self.kill_now:
            lg.info('The thread is killed. Stop waiting.')
            self.imap.CLOSE()
            self.imap.LOGOUT()
        elif self.callback_normal == True:
            typ, data = self.imap.SEARCH(None, 'UNSEEN')
            lg.debug('Data: %r', data)
            new_mails = 0
            new_mails = set(data[0].split()) - self.old_mails
            if len(new_mails) == 0:
                lg.info('No new mail.')
            else:
                lg.info('Got new mail(s)!')
                for _id in new_mails:
                    lg.info('Mail ID: %r', _id)
                    typ, d = self.imap.fetch(_id, '(RFC822)')
                    lg.debug("d = {!r}".format(d))
                    raw_email = self._get_raw_email_from_fetched_data(d)
                    self.raw_mail_handler(raw_email)



### Demo ###

#The following part demoes printing senders of new mails
def main():
    def setup_logging(path='logging.json'):
        """
        setup logging configuration from a json file
        """
        if os.path.exists(path):
            with open(path, 'r') as log_json_file:
                logging.config.dictConfig(json.load(log_json_file))
        else:
            logging.basicConfig(level=level)

    setup_logging(path='logging.json')

    user = 'user@example.com'
    pwd = 'yourpassword'
    server = 'imap.gmail.com'
    t = 86400
    def handler(raw_email):
        lg.debug('%r', raw_email)
        _to, _from, _sub, _msg = MailChecker.plain_text_from_raw_email(raw_email)
        print("to (type={0!r}) {1!r}".format(type(_to), _to))
        print("from (type = {0!r}) {1!r}".format(type(_from), _from))
        print("subject (type = {0!r}) {1!r}".format(type(_sub), _sub))
        m = MailChecker.content_cleanup(_msg)
        print("message:")
        pp.pprint(m)

    mail_checker = MailChecker(user, pwd, server, t, handler)
    mail_checker.start()
    input()
    mail_checker.kill()
    sys.exit()

if __name__ == '__main__':
    main()
