<?php

if (isset($_POST['submit']) and $_POST['submit'] == 1) {
    $filename = $_FILES['linelist']['name'];
    $email = htmlentities($_POST['email'], ENT_QUOTES, 'ISO-8859-15');

    if (isset($filename)) {
        $error0 = 'none existent';
    } else {
        $error0 = 'exists';
        echo 'An error occurred with the line list. Please upload one.<br>';
    }

    $Teff = $_POST['Teff'];
    if (is_numeric($Teff)) {
        $error1 = 'none existent';
    } else {
        $error1 = 'exists';
        echo 'You have an error in the Teff. Expected an integer.<br>';
    }

    $logg = $_POST['logg'];
    if (is_numeric($logg)) {
        $error2 = 'none existent';
    } else {
        $error2 = 'exists';
        echo 'You have an error in the logg. Expected a float.<br>';
    }

    $feh = $_POST['feh'];
    if (is_numeric($feh)) {
        $error3 = 'none existent';
    } else {
        $error3 = 'exists';
        echo 'You have an error in the [Fe/H]. Expected a float.<br>';
    }

    $vt = $_POST['vt'];
    if (is_numeric($vt)) {
        $error4 = 'none existent';
    } else {
        $error4 = 'exists';
        echo 'You have an error in the vt. Expected a float.<br>';
    }


    if ($error1 == 'exists' or $error2 == 'exists' or $error3 == 'exists' or $error4 == 'exists') {
        echo '<a href="#" onclick="history.back();">Click here to fix it</a>';
    } else {
        move_uploaded_file($_FILES['linelist']['tmp_name'], '/tmp/linelist.moog');
        header('Location: ../cgi-bin/abundanceConf.py?linelist='.$filename.'&email='.$email.'&Teff='.$Teff.'&logg='.$logg.'&feh='.$feh.'&vt='.$vt);
    }
}
