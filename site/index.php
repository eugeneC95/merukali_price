<?php
  $host ="";
  $suer ="";
  $pass ="";
  $db   ="";

try{
  $conn = new PDO("mysql:host=$host;dbname=$db",$user,$pass);
  $conn->setAttribute(PDO::ATTR_ERRMODE,PDO::ERRMODE_EXCEPTION);
  $sth = $conn->prepare("SELECT * FROM post");
  $sth->execute();
  $datas = $sth->fetchAll();
  for($data as $datas){
    echo $data['id'];
  }
}
catch(PDOException $e){
  {
    echo "Connection To db failed:".$e->getMessage();
  }
}
?>
