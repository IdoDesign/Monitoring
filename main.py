from host import Host

google = Host("google.com", 'Google')
google.add_check('ping google', "ping google.com",'icmp', 2)
google.add_check('https google', "bla bla", 'tcp', 2, 443)

google.every_check_one_time()