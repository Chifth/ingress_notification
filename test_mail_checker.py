#!/usr/bin/env python3

import unittest
from mail_checker import MailChecker
import pprint
PP = pprint.PrettyPrinter(indent=2)
import logging
import time
import pickle

class MailCheckerTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        pass

    def tearDown(self):
        pass

    def test_assert(self):
        self.assertEquals(1, 1)
        self.assertTrue(True)
        self.assertFalse(False)

    def test_plain_text_from_raw_eamil(self):
        with open('raw_email_sample.txt', 'r') as f:
            raw_email = f.read()
            MailChecker.plain_text_from_raw_email(raw_email)
            _to, _from, _sub, _msg, _html = MailChecker.plain_text_from_raw_email(raw_email)
            self.assertEquals(_to, 'yyyyyyy <yyyyyyy@gmail.com>')
            self.assertEquals(_from, 'Niantic Project Operations <ingress-support@nianticlabs.com>')
            self.assertEquals(_sub, 'Ingress Damage Report: Entities attacked by dindindon')
            self.assertEquals(len(_msg), 467)
            self.assertEquals(len(_html), 3885)
            logging.debug('type: {}'.format(type(_html)))
                
            

    def test_content_cleanup(self):
        with open('message_list_sample.pkl', 'rb') as f:
            msg_list = pickle.load(f)
            msg_list = MailChecker.content_cleanup(msg_list)
            self.assertEquals(msg_list[0], '** Ingress - Begin Transmission**')
            self.assertEquals(msg_list[1], 'Agent Name:wycchen')
            self.assertEquals(msg_list[2], 'Faction:Enlightened')
            self.assertEquals(msg_list[3], 'Current Level:L11')
            self.assertEquals(msg_list[4], 'DAMAGE REPORT')
            self.assertEquals(msg_list[5], '什麼鬼東西來的')
            self.assertEquals(msg_list[6], 'No. 1, Lane 128, Section 2, Yanjiuyuan Road, Nangang District, Taipei City,  ')
            self.assertEquals(msg_list[7], 'Taiwan 115')
            self.assertEquals(msg_list[8], 'Portal - 什麼鬼東西來的')
            self.assertEquals(msg_list[9], 'Map')
            self.assertEquals(msg_list[10], 'DAMAGE:')
            self.assertEquals(msg_list[11], '1 Resonator destroyed by dindindon at 17:27 hrs GMT')
            self.assertEquals(msg_list[12], '5 Resonators remaining on this Portal.')
            self.assertEquals(msg_list[13], 'STATUS:')
            self.assertEquals(msg_list[14], 'Level 4')
            self.assertEquals(msg_list[15], 'Health: 52%')
            self.assertEquals(msg_list[16], 'Owner: rhinogreen')
            self.assertEquals(msg_list[17], '** Ingress - End Transmission **')
            

    def test_mail_checker(self):
        username = 'bothsiu@gmail.com'
        password = 'yijWBcjb9iwK6q'
        imap_server = 'imap.gmail.com'
        def handler(raw_email):
            _to, _from, _sub, _msg, _html = MailChecker.plain_text_from_raw_email(raw_email)
        mail_checker = MailChecker(username, password, imap_server, raw_mail_handler=handler)
        mail_checker.start()
        input()
        mail_checker.kill()


if __name__ == '__main__':
    unittest.main()
        
