<?php

if (isset($_POST['submit']) and $_POST['submit'] == 1) {
    $filename = $_FILES['linelist']['name'];
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

    $email = htmlentities($_POST['email'], ENT_QUOTES, 'ISO-8859-15');
    $atmosphere = htmlentities($_POST['atmosphere'], ENT_QUOTES, 'ISO-8859-15');
    $outlier = htmlentities($_POST['outlier'], ENT_QUOTES, 'ISO-8859-15');

    $sigma = $_POST['sigma'];
    if (is_numeric($sigma)) {
        $error5 = 'none existent';
    } else {
        $error5 = 'exists';
        echo 'You have an error in the sigma. Expected a float.<br>';
    }

    $iterations = $_POST['iterations'];
    if (is_numeric($iterations)) {
        $error6 = 'none existent';
    } else {
        $error6 = 'exists';
        echo 'You have an error in the iterations. Expected an integer.<br>';
    }

    $EPslope = $_POST['EPslope'];
    if (is_numeric($EPslope)) {
        $error7 = 'none existent';
    } else {
        $error7 = 'exists';
        echo 'You have an error in the EPslope. Expected a float.<br>';
    }

    $RWslope = $_POST['RWslope'];
    if (is_numeric($RWslope)) {
        $error8 = 'none existent';
    } else {
        $error8 = 'exists';
        echo 'You have an error in the RWslope. Expected a float.<br>';
    }

    $feDiff = $_POST['feDiff'];
    if (is_numeric($feDiff)) {
        $error9 = 'none existent';
    } else {
        $error9 = 'exists';
        echo 'You have an error in the feDiff. Expected a float.<br>';
    }

    if (isset($_POST['teffrange'])) {
        $teffrange = $_POST['teffrange'];
        if ($teffrange == 'on' or $teffrange == '') {
            $error10 = 'none existent';
        } else {
            $error10 = 'exists';
            echo 'You have an error in the teffrange. Do not try to hack us.<br>';
        }
    } else {
        $error10 = 'none existent';
        $teffrange = '';
    }

    if (isset($_POST['autofixvt'])) {
        $autofixvt = $_POST['autofixvt'];
        if ($autofixvt == 'on' or $autofixvt == '') {
            $error11 = 'none existent';
        } else {
            $error11 = 'exists';
            echo 'You have an error in the autofixvt. Do not try to hack us.<br>';
        }
    } else {
        $error11 = 'none existent';
        $autofixvt = '';
    }

    if (isset($_POST['refine'])) {
        $refine = $_POST['refine'];
        if ($refine == 'on' or $refine == '') {
            $error12 = 'none existent';
        } else {
            $error12 = 'exists';
            echo 'You have an error in the refine. Do not try to hack us.<br>';
        }
    } else {
        $error12 = 'none existent';
        $refine = '';
    }

    if (isset($_POST['initial'])) {
        $initial = $_POST['initial'];
        if ($initial == 'on' or $initial == '') {
            $error13 = 'none existent';
        } else {
            $error13 = 'exists';
            echo 'You have an error in the initial. Do not try to hack us.<br>';
        }
    } else {
        $error13 = 'none existent';
        $initial = '';
    }

    if (isset($_POST['fixteff'])) {
        $fixteff = $_POST['fixteff'];
        if ($fixteff == 'on' or $fixteff == '') {
            $error14 = 'none existent';
        } else {
            $error14 = 'exists';
            echo 'You have an error in the fixteff. Do not try to hack us.<br>';
        }
    } else {
        $error14 = 'none existent';
        $fixteff = '';
    }

    if (isset($_POST['fixlogg'])) {
        $fixlogg = $_POST['fixlogg'];
        if ($fixlogg == 'on' or $fixlogg == '') {
            $error15 = 'none existent';
        } else {
            $error15 = 'exists';
            echo 'You have an error in the fixlogg. Do not try to hack us.<br>';
        }
    } else {
        $error15 = 'none existent';
        $fixlogg = '';
    }

    if (isset($_POST['fixfeh'])) {
        $fixfeh = $_POST['fixfeh'];
        if ($fixfeh == 'on' or $fixfeh == '') {
            $error16 = 'none existent';
        } else {
            $error16 = 'exists';
            echo 'You have an error in the fixfeh. Do not try to hack us.<br>';
        }
    } else {
        $error16 = 'none existent';
        $fixfeh = '';
    }

    if (isset($_POST['fixvt'])) {
        $fixvt = $_POST['fixvt'];
        if ($fixvt == 'on' or $fixvt == '') {
            $error17 = 'none existent';
        } else {
            $error17 = 'exists';
            echo 'You have an error in the fixvt. Do not try to hack us.<br>';
        }
    } else {
        $error17 = 'none existent';
        $fixvt = '';
    }

    if ($error0 == 'exists' or $error1 == 'exists' or $error2 == 'exists' or $error3 == 'exists' or $error4 == 'exists' or $error5 == 'exists' or $error6 == 'exists' or $error7 == 'exists' or $error8 == 'exists' or $error9 == 'exists' or $error10 == 'exists' or $error11 == 'exists' or $error12 == 'exists' or $error13 == 'exists' or $error14 == 'exists' or $error15 == 'exists' or $error16 == 'exists' or $error17 == 'exists') {
        echo '<a href="#" onclick="history.back();">Click here to fix it</a>';
    } else {
        move_uploaded_file($_FILES['linelist']['tmp_name'], '/tmp/linelist.moog');
        header('Location: ../cgi-bin/ewmethodConf.py?linelist='.$filename.'&Teff='.$Teff.'&logg='.$logg.'&feh='.$feh.'&vt='.$vt.'&email='.$email.'&atmosphere='.$atmosphere.'&outlier='.$outlier.'&sigma='.$sigma.'&iterations='.$iterations.'&EPslope='.$EPslope.'&RWslope='.$RWslope.'&feDiff='.$feDiff.'&teffrange='.$teffrange.'&autofixvt='.$autofixvt.'&refine='.$refine.'&initial='.$initial.'&fixteff='.$fixteff.'&fixlogg='.$fixlogg.'&fixfeh='.$fixfeh.'&fixvt='.$fixvt);
    }
}
