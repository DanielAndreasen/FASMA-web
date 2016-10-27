#!/home/daniel/Software/anaconda3/bin/python

# Import modules for CGI handling
import cgi, cgitb
from ewDriver import ewdriver


def cgi2dict(form, linelist):
    """Convert the form from cgi.FieldStorage to a python dictionary"""

    params = {'linelist': linelist.value,
              'initial': False,
              'fixTeff': False,
              'fixlogg': False,
              'fixfeh': False,
              'fixvt': False,
              'refine': False,
              'outlier': False,
              'teffrange': False,
              'autofixvt': False}
    outlier = {'None': None,
               'All once': 'allOnce',
               'All iteratively': 'allIter',
               'One iteratively': '1Iter'}
    for key in form.keys():
        if key != 'linelist':
            params[key] = form[key].value
    params['outlier'] = outlier[params['outlier']]  # Translate to FASMA
    # Adjust the model atmosphere for FASMA
    if params['atmosphere'] == 'Kurucz':
        params['atmosphere'] = 'kurucz95'
    params['atmosphere'] = params['atmosphere'].lower()
    return params


def ew(form):
    """Create the configuration file for running the ARES driver"""

    fout = 'linelist.moog '
    fout += '%s ' % form['Teff']
    fout += '%s ' % form['logg']
    fout += '%s ' % form['feh']
    fout += '%s ' % form['vt']
    fout += 'model:%s' % form['atmosphere']
    fout += ',iterations:%s' % form['iterations']
    fout += ',EPcrit:%s' % form['EPslope']
    fout += ',RWcrit:%s' % form['RWslope']
    fout += ',Abdiffcrit:%s' % form['feDiff']
    if form['teffrange']:
        fout += ',teffrange'
    if form['autofixvt']:
        fout += ',autofixvt'
    if form['refine']:
        fout += ',refine'
    if form['initial']:
        fout += ',tmcalc'
    if form['outlier']:
        fout += ',outlier:%s' % form['outlier']
        fout += ',sigma:%s' % form['sigma']
    if form['fixTeff']:
        fout += 'fixteff'
    if form['fixlogg']:
        fout += 'fixlogg'
    if form['fixfeh']:
        fout += 'fixfeh'
    if form['fixvt']:
        fout += 'fixvt'

    with open('/tmp/StarMe_ew.cfg', 'w') as f:
        f.writelines(fout + '\n')

    ewdriver(starLines='/tmp/StarMe_ew.cfg', overwrite=True)


if __name__ == '__main__':
    # Enable debugging
    cgitb.enable()

    form = cgi.FieldStorage()

    # Save the line list to a standard location
    with open('/tmp/linelist.moog', 'w') as f:
        f.write(form['linelist'].value)

    # Run the minimization for a line list
    formDict = cgi2dict(form, form['linelist'])
    ew(formDict)

    # Show the finished html page
    print "Content-type: text/html\n\n"
    # for l in formDict.iterkeys():
        # print "<p>%s: %s</p>" % (l, formDict[l])
    # print "<p>%s</p>" % formDict
    with open('../html/finish.html', 'r') as lines:
        for line in lines:
            print line
