#!/home/daniel/Software/anaconda3/bin/python

# Import modules for CGI handling
import cgi, cgitb
from aresDriver import aresdriver
from emailSender import sendEmail


def cgi2dict(form, linelist):
    """Convert the form from cgi.FieldStorage to a python dictionary"""
    params = {'linelist': linelist.value}
    for key in form.keys():
        if key != 'linelist':
            params[key] = form[key].value
    return params


def ares(form):
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
    fout += ' /tmp/spectrum.fits'
    fout += ' lambdai:%s,lambdaf:%s,smoothder:%s' % (form['w0'], form['wf'], form['smooth'])
    fout += ',space:%s,lineresol:%s' % (form['space'], form['lineresol'])
    fout += ',miniline:%s,EWcut:%s' % (form['miniline'], form['EWcut'])
    if form['continuum'] in ['snr', 'rejt']:
        fout += ',rejt:%s' % rejt
    if rvmask:
        fout += ',rvmask:%s' % rvmask
    if 'force' in form.keys():
        fout += ',force'

    with open('/tmp/StarMe_ares.cfg', 'w') as f:
        f.writelines(fout+'\n')

    aresdriver('/tmp/StarMe_ares.cfg')


if __name__ == '__main__':
    # Enable debugging
    cgitb.enable()

    form = cgi.FieldStorage()

    # Run ARES for one or several line lists
    if isinstance(form['linelist'], list):
        for linelist in form['linelist']:
            formDict = cgi2dict(form, linelist)
            ares(formDict)
            sendEmail(to=formDict['email'], driver='EW', data='/tmp/spectrum.moog')
    else:
        formDict = cgi2dict(form, form['linelist'])
        ares(formDict)
        sendEmail(to=formDict['email'], driver='EW', data='/tmp/spectrum.moog')


    # Show the finished html page
    print "Content-type: text/html\n\n"
    with open('../html/finish.html', 'r') as lines:
        for line in lines:
            print line
