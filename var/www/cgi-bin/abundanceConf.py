#!/home/daniel/Software/anaconda3/bin/python

# Import modules for CGI handling
import cgi, cgitb
from abundanceDriver import abundancedriver
from emailSender import sendEmail


def cgi2dict(form):
    """Convert the form from cgi.FieldStorage to a python dictionary"""
    params = {}
    for key in form.keys():
        params[key] = form[key].value
    return params


def abundance(form):
    """Create the configuration file for running the abundance driver"""
    # Make the StarMe_ares.cfg
    fout = '/tmp/linelist.moog {Teff} {logg} {feh} {vt}'.format(**form)

    with open('/tmp/StarMe_abundance.cfg', 'w') as f:
        f.writelines(fout+'\n')

    abundancedriver('/tmp/StarMe_abundance.cfg')


if __name__ == '__main__':
    # Enable debugging
    import os
    os.system('touch /tmp/test1')
    cgitb.enable()

    form = cgi.FieldStorage()

    # Run ARES for one or several line lists
    formDict = cgi2dict(form)
    abundance(formDict)
    sendEmail(to=formDict['email'], driver='abundances', data='/tmp/abundances.dat')


    # Show the finished html page
    print "Content-type: text/html\n\n"
    with open('../html/finish.html', 'r') as lines:
        for line in lines:
            print line
