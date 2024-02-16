<html>
<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "kisaandb";

$conn = mysqli_connect($servername, $username, $password, $dbname);

// $api_key_value = "tPmAT5Ab3j7F9";

$temperature = "";
$humidity = "";  
$LDR = "";
$Soilmoisture = "";

if ($_SERVER["REQUEST_METHOD"] == "POST")  {
        $temperature = test_input($_POST["temperature"]);
        $humidity = test_input($_POST["humidity"]);
        $LDR = test_input($_POST["LDR"]);
        $Soilmoisture = test_input($_POST["Soilmoisture"]);
        
        // Create connection
        $conn = new mysqli($servername, $username, $password, $dbname);
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 
        
        // $sql = "INSERT INTO dhtdata (temperature, humidity)
        // VALUES ('" .$temperature . "', '" .$humidity . "')";

        // $sql = "INSERT INTO ldrdata (LDR)
        // VALUES ('" .$LDR . "')";

        // $sql = "INSERT INTO moisture (Soilmoisture)
        // VALUES ('" .$Soilmoisture . "')";
        
        // if ($conn->query($sql) == TRUE) {
            $sql1 = "INSERT INTO dhtdata (temperature, humidity) VALUES ('" .$temperature . "', '" .$humidity . "')";
            $sql2 = "INSERT INTO ldrdata (LDR) VALUES ('" .$LDR . "')";
            $sql3 = "INSERT INTO moisture (Soilmoisture) VALUES ('" .$Soilmoisture . "')";

            if ($conn->query($sql1) === TRUE && $conn->query($sql2) === TRUE && $conn->query($sql3) === TRUE) {
            echo "New record created successfully";
                } 
            else {
            echo "Error: " . $sql . "<br>" . $conn->error;
                }
    
        $conn->close();
    }
    


else {
    echo "No data posted with HTTP POST.";
}

function test_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}
    
