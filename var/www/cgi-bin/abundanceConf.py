#!/home/daniel/Software/anaconda3/bin/python

# Import modules for CGI handling
import os
import cgi, cgitb
from time import time
from abundanceDriver import abundancedriver
from emailSender import sendEmail


def cgi2dict(form):
    """Convert the form from cgi.FieldStorage to a python dictionary"""
    params = {}
    for key in form.keys():
        params[key] = form[key].value
    return params


def abundance(form, timestamp, starname):
    """Create the configuration file for running the abundance driver"""
    # Make the StarMe_ares.cfg
    fout = '/tmp/{linelist} {Teff} {logg} {feh} {vt}'.format(**form)

    cfgfile = '/tmp/StarMe_abundance%s.cfg' % timestamp
    with open(cfgfile, 'w') as f:
        f.writelines(fout+'\n')

    abundancedriver(cfgfile, timestamp=timestamp, starname=starname)
    os.remove(cfgfile)


if __name__ == '__main__':
    # Enable debugging
    cgitb.enable()

    form = cgi.FieldStorage()
    formDict = cgi2dict(form)

    # Make a unique session
    timestamp = str(time()).replace('.', '')
    linelist = 'linelist%s.moog' % timestamp
    formDict['starname'] = formDict['linelist'].split('.')[0]
    formDict['linelist'] = linelist
    os.system('mv /tmp/linelist.moog /tmp/%s' % linelist)

    starname = formDict['starname']
    final_output = '/tmp/%s.dat' % starname
    output = '/tmp/abundresults%s.dat' % timestamp

    abundance(formDict, timestamp, starname)
    os.system('mv %s %s' % (output, final_output))
    sendEmail(to=formDict['email'], driver='abundances', data=final_output)
    os.remove(final_output)

    # Show the finished html page
    print "Content-type: text/html\n\n"
    with open('../html/finish.html', 'r') as lines:
        for line in lines:
            print line
