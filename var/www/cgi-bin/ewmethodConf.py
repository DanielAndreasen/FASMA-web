#!/home/daniel/Software/anaconda3/bin/python

# Import modules for CGI handling
import cgi, cgitb
from ewDriver import ewdriver


def cgi2dict(form):
    """Convert the form from cgi.FieldStorage to a python dictionary"""

    params = {'initial': False,
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
        params[key] = form[key].value
    params['outlier'] = outlier[params['outlier']]  # Translate to FASMA
    # Adjust the model atmosphere for FASMA
    if params['atmosphere'] == 'Kurucz':
        params['atmosphere'] = 'kurucz95'
    params['atmosphere'] = params['atmosphere'].lower()
    return params


def ew(form, name=None):
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
        fout += ',teff'
    if form['fixlogg']:
        fout += ',logg'
    if form['fixfeh']:
        fout += ',feh'
    if form['fixvt']:
        fout += ',vt'

    with open('/tmp/StarMe_ew.cfg', 'w') as f:
        f.writelines(fout + '\n')

    parameters = ewdriver(starLines='/tmp/StarMe_ew.cfg', overwrite=True, name=name)
    return parameters


def parameters2HTML(parameters):
    """Convert the parameters to HTML in a table"""

    data = {'teff': parameters[0], 'tefferr': parameters[1],
            'logg': parameters[2], 'loggerr': parameters[3],
            'feh': parameters[4], 'feherr': parameters[5],
            'vt': parameters[6], 'vterr': parameters[7]}

    table = '''<table class="table table-hover table-bordered table-striped">
                 <thead>
                   <tr>
                     <th>Parameters</th>
                     <th>Value</th>
                   </tr>
                     </thead>
                     <tbody>
                   <tr>
                     <td>T<sub>eff</sub></td>
                     <td>{teff}&plusmn;{tefferr}</td>
                   </tr>
                   <tr>
                     <td>logg</td>
                     <td>{logg}&plusmn;{loggerr}</td>
                   </tr>
                   <tr>
                     <td>[Fe/H]</td>
                     <td>{feh}&plusmn;{feherr}</td>
                   </tr>
                   <tr>
                     <td>&xi;<sub>tur</sub></td>
                     <td>{vt}&plusmn;{vterr}</td>
                   </tr>
                 </tbody>
               </table>'''.format(**data)
    print table


if __name__ == '__main__':
    # Enable debugging
    cgitb.enable()

    form = cgi.FieldStorage()
    # Run the minimization for a line list
    formDict = cgi2dict(form)
    parameters = ew(formDict, name=formDict['linelist'])

    # Show the finished html page
    print 'Content-type: text/html\n\n'
    with open('../html/finish.html', 'r') as lines:
        for line in lines:
            if 'Congratulations' in line:
                print line,
                print '<h2 class="text-secondary text-center">Results for %s</h2>' % formDict['linelist'].rpartition('.')[0]
                print '<br>'
                parameters2HTML(parameters)
                continue
            print line,
