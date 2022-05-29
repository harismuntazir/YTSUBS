<?php
# globals 
$base = "https://www.";
$videoId = "AaaboZuI4lQ";
# connect to sqlite database accounts.db
$db = new PDO('sqlite:accounts.db');

# get all records from the db
$stmt = $db->prepare('SELECT * FROM accounts');
$stmt->execute();
# from stmt get all records
$accounts = $stmt->fetchAll(PDO::FETCH_ASSOC);

# do get request 
function get($url, $data) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_COOKIEJAR, "cookies.txt");
    curl_setopt($ch, CURLOPT_COOKIEFILE, "cookies.txt");
    curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36");
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);
    curl_setopt($ch, CURLOPT_HEADER, 1);
    curl_setopt($ch, CURLOPT_VERBOSE, 1);
    return curl_exec($ch);
}

# login
function login($host, $username, $password) {
    $url = $base . $host . "/signinclick.html";
    $data = "username=$username&password=$password";
    get($url, $data);
    curl_close($ch);

    # headers["Set-Cookie"].split("JSESSIONID=")
    $jsessionid = explode("JSESSIONID=", $result);
    $jsessionid = $jsessionid[1];
    $jsessionid = explode(";", $jsessionid);
    $jsessionid = $jsessionid[0];

    return $jsessionid;
}

# from each account get the username, password, accountId and host
foreach ($accounts as $account) {
    $username = $account['username'];
    $password = $account['password'];
    $accountId = $account['accountId'];
    $host = $account['host'];
    
    # login
    $jsessionid = login($host, $username, $password);
    # shift video url
    $tail = "/assignuservideo.html?idUser=$accountId&idVideo=$videoId";
    $url = $base . $host . $tail;
    $data = "";
    # create cookie file using jsessionid
    $cookie = "cookies.txt";
    $fp = fopen($cookie, 'w');
    fwrite($fp, "JSESSIONID=$jsessionid");
    fclose($fp);
    # get request
    $result = get($url, $data);
    
    

}

