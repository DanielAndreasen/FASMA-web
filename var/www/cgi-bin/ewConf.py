#!/home/daniel/Software/anaconda3/bin/python

# Import modules for CGI handling
import os
import cgi, cgitb
from time import time
from aresDriver import aresdriver
from emailSender import sendEmail


def cgi2dict(form, linelist):
    """Convert the form from cgi.FieldStorage to a python dictionary"""
    params = {'linelist': linelist.value}
    for key in form.keys():
        if key != 'linelist':
            params[key] = form[key].value
    return params


def ares(form, timestamp, fitsfile):
    """Create the configuration file for running the ARES driver"""
    def rejt_from_snr(snr):
        """Calculate rejt from SNR"""
        return 1-1/snr

    if form['continuum'] == 'snr':
        rejt = rejt_from_snr(form['snr'])
    elif form['continuum'] == 'rejt':
        rejt = form['rejt']
        rejt = 0.99999 if rejt > 0.99999 else rejt
    rvmask = False if form['rv'] == 0 else form['rv']

    # Make the StarMe_ares.cfg
    if form['linelist'] == 'Optical (parameters)':
        fout = 'Sousa2007_opt.lst'
    elif form['linelist'] == 'NIR (parameters)':
        fout = 'Andreasen2016_nir.lst'
    elif form['linelist'] == 'Optical (abundances)':
        fout = 'Neves2009_elements.lst'
    fout += ' /tmp/%s' % fitsfile
    fout += ' lambdai:%s,lambdaf:%s,smoothder:%s' % (form['w0'], form['wf'], form['smooth'])
    fout += ',space:%s,lineresol:%s' % (form['space'], form['lineresol'])
    fout += ',miniline:%s,EWcut:%s' % (form['miniline'], form['EWcut'])
    if form['continuum'] in ['snr', 'rejt']:
        fout += ',rejt:%s' % rejt
    if rvmask:
        fout += ',rvmask:%s' % rvmask
    if 'force' in form.keys():
        fout += ',force'

    cfgfile = '/tmp/StarMe_ares%s.cfg' % timestamp
    with open(cfgfile, 'w') as f:
        f.writelines(fout+'\n')

    aresdriver(cfgfile, timestamp, fitsfile, form['spectrum'])
    os.remove(cfgfile)


if __name__ == '__main__':
    # Enable debugging
    cgitb.enable()

    form = cgi.FieldStorage()
    timestamp = str(time()).replace('.', '')
    fitsfile = 'spectrum%s.fits' % timestamp
    os.system('mv /tmp/spectrum.fits /tmp/%s' % fitsfile)

    # Run ARES for one or several line lists
    if isinstance(form['linelist'], list):
        for linelist in form['linelist']:
            timestamp = str(time()).replace('.', '')
            output = '/tmp/spectrum%s.moog' % timestamp
            formDict = cgi2dict(form, linelist)
            final_output = '/tmp/%s.moog' % formDict['spectrum'].split('.')[0]
            ares(formDict, timestamp=timestamp, fitsfile=fitsfile)
            os.system('mv %s %s' % (output, final_output))
            sendEmail(to=formDict['email'], driver='EW', data=final_output)
            os.remove(final_output)
    else:
        timestamp = str(time()).replace('.', '')
        output = '/tmp/spectrum%s.moog' % timestamp
        formDict = cgi2dict(form, form['linelist'])
        final_output = '/tmp/%s.moog' % formDict['spectrum'].split('.')[0]
        ares(formDict, timestamp=timestamp, fitsfile=fitsfile)
        os.system('mv %s %s' % (output, final_output))
        sendEmail(to=formDict['email'], driver='EW', data=final_output)
        os.remove(final_output)

    os.remove('/tmp/%s' % fitsfile)
    os.remove('/tmp/mine.opt')

    # Show the finished html page
    print "Content-type: text/html\n\n"
    with open('../html/finish.html', 'r') as lines:
        for line in lines:
            print line
