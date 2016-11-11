#!/home/daniel/Software/anaconda3/bin/python
# -*- coding: utf8 -*-

import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def sendEmail(to, driver, data):
    """doc string

    Input
    -----
    to : str
      The email adress of the receiver
    driver : str
      The driver that has been used ('EW', 'EWmethod', 'abundances', 'synthesis')
    data : --
      The data to attach
    """

    if driver == 'EW':
        textfile = 'messages/EW.txt'
    elif driver == 'EWmethod':
        textfile = 'messages/EWmethod.txt'
    elif driver == 'abundances':
        textfile = 'messages/EW.txt'
    elif driver == 'synthesis':
        textfile = 'messages/synthesis.txt'

    msg = MIMEMultipart()
    with open(textfile, 'rb') as fp:
        msg.attach(MIMEText(fp.read()))

    me ='daniel.andreasen@astro.up.pt'
    you = to
    msg['Subject'] = 'FASMA results. Driver: %s' % driver
    msg['From'] = me
    msg['To'] = to

    with open(data, "rb") as f:
        part = MIMEApplication(f.read(), Name=basename(data))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(data)
        msg.attach(part)

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP(host='mail.astro.up.pt', port=25)
    s.sendmail(me, [you], msg.as_string())
    s.quit()


if __name__ == '__main__':
    sendEmail(to='daniel.andreasen@astro.up.pt', driver='EW', data='/tmp/spectrum.moog')
