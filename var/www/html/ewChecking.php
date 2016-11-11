<?php

if (isset($_POST['submit']) and $_POST['submit'] == 1) {
    $filename = $_FILES['spectrum']['name'];
    $linelist = htmlentities($_POST['linelist'], ENT_QUOTES, 'ISO-8859-15');
    $email = htmlentities($_POST['email'], ENT_QUOTES, 'ISO-8859-15');

    if (isset($filename)) {
        $error0 = 'none existent';
    } else {
        $error0 = 'exists';
        echo 'An error occurred with the spectrum. Please upload one.<br>';
    }

    $continuum = $_POST['continuum'];
    $snr = $_POST['snr'];
    $rejt = $_POST['rejt'];
    if (isset($continuum)) {
        $error1 = 'none existent';
        $error2 = 'none existent';
        $error3 = 'none existent';
        switch ($_POST['continuum']) {
      case 'autoRejt':
        break;
      case 'snr':
        if (is_numeric($snr) and $snr > 0) {
        } else {
            $error2 = 'exists';
            echo 'An error occurred with SNR. Expected a positive number.<br>';
        }
        break;
      case 'rejt':
        if (is_numeric($rejt) and $rejt > 0 and $rejt < 1) {
        } else {
            $error3 = 'exists';
            echo 'An error occurred with the rejt parameter. Expected a number between 0 and 1.<br>';
        }
        break;
      default:
        $error1 = 'exists';
        echo 'An error occurred. Need either auto rejt, SNR, or rejt to be set.<br>';
        break;
    }
    }

    $w0 = $_POST['w0'];
    if (is_numeric($w0) and $w0 > 0) {
        $error4 = 'none existent';
    } else {
        $error4 = 'exists';
        echo 'You have an error with wmin. Expected a positive integer.<br>';
    }

    $wf = $_POST['wf'];
    if (is_numeric($wf) and $wf > $w0) {
        $error5 = 'none existent';
    } else {
        $error5 = 'exists';
        echo 'You have an error with wmax. Expected a positive integer larger than wmin.<br>';
    }

    $rv = $_POST['rv'];
    if (is_numeric($rv)) {
        $error6 = 'none existent';
    } else {
        $error6 = 'exists';
        echo 'You have an error with RV. Expected a float.<br>';
    }

    $smooth = $_POST['smooth'];
    if (is_numeric($smooth) and $smooth > 0) {
        $error7 = 'none existent';
    } else {
        $error7 = 'exists';
        echo 'You have an error with the smooth parameter. Expected a positive number.<br>';
    }

    if (isset($_POST['force'])) {
        $force = $_POST['force'];
        if ($force == 'on' or $force == '') {
            $error8 = 'none existent';
        } else {
            $error8 = 'exists';
            echo 'You have an error in the force. Do not try to hack us.<br>';
        }
    } else {
        $error8 = 'none existent';
        $force = '';
    }

    $miniline = $_POST['miniline'];
    if (is_numeric($miniline) and $miniline > 0) {
        $error9 = 'none existent';
    } else {
        $error9 = 'exists';
        echo 'You have an error with EW min. Expected a positive float.<br>';
    }

    $ewcut = $_POST['EWcut'];
    if (is_numeric($ewcut) and $ewcut > $miniline) {
        $error10 = 'none existent';
    } else {
        $error10 = 'exists';
        echo 'You have an error with EW max. Expected a float bigger than EW min.<br>';
    }

    $lineresol = $_POST['lineresol'];
    if (is_numeric($lineresol) and $lineresol > 0) {
        $error11 = 'none existent';
    } else {
        $error11 = 'exists';
        echo 'You have an error with lineresol. Expected a positive float.<br>';
    }

    $space = $_POST['space'];
    if (is_numeric($space) and $space > 0) {
        $error12 = 'none existent';
    } else {
        $error12 = 'exists';
        echo 'You have an error with the space parameter. Expected a positive float.<br>';
    }

    if ($error1 == 'exists' or $error2 == 'exists' or $error3 == 'exists' or $error4 == 'exists' or $error5 == 'exists' or $error6 == 'exists' or $error7 == 'exists' or $error8 == 'exists' or $error9 == 'exists' or $error10 == 'exists' or $error11 == 'exists' or $error12 == 'exists') {
        echo '<a href="#" onclick="history.back();">Click here to fix it</a>';
    } else {
        move_uploaded_file($_FILES['spectrum']['tmp_name'], '/tmp/spectrum.fits');
        header('Location: ../cgi-bin/ewConf.py?spectrum='.$filename.'&linelist='.$linelist.'&email='.$email.'&continuum='.$continuum.'&snr='.$snr.'&rejt='.$rejt.'&w0='.$w0.'&wf='.$wf.'&rv='.$rv.'&smooth='.$smooth.'&miniline='.$miniline.'&EWcut='.$ewcut.'&lineresol='.$lineresol.'&space='.$space.'&force='.$force);
    }
}
