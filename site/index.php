<?php
  $host ="localhost";
  $suer ="zun95";
  $pass ="Hotdilvin95";
  $db   ="merucali";

try{
  $conn = new PDO("mysql:host=$host;dbname=$db",$user,$pass);
  $conn->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
  $sth = $conn->prepare("SELECT * FROM post ORDER BY post.time_update DESC LIMIT 0,200");
  $sth->execute();
  $datas = $sth->fetchAll();
  for($data as $datas){
    echo $data['id'];
  }
}
catch(PDOException $e){
    echo "Connection To db failed:".$e->getMessage();
}
?>
