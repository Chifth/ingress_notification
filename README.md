# ingress_notification

### Package needed
-   imaplib2

### Usage
Check the following code example
    # Setup the email parameters
    user = 'user@example.com'
    pwd = 'yourpassword'
    server = 'imap.gmail.com'
    t = 60 #timeout

    # This function will be invoked when there are new mails
    def handler(raw_email):
        # Parse a raw email to get details of a email
        _to, _from, _sub, _msg = MailChecker.plain_text_from_raw_email(raw_email)

        # Print out what we got
        print("to (type={0!r}) {1!r}".format(type(_to), _to))
        print("from (type = {0!r}) {1!r}".format(type(_from), _from))
        print("subject (type = {0!r}) {1!r}".format(type(_sub), _sub))
        print("message:")

        # Make the contents in the form of list of strings. Also the empty
        # lines end \r will be removed
        m = MailChecker.content_cleanup(_msg)

        # Print the cleaned up contents nicely
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(m)

    mail_checker = MailChecker(user, pwd, server, t, handler)
    mail_checker.start()
    input()
    mail_checker.kill()
