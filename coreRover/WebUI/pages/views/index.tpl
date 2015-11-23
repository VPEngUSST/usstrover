% rebase('layout.tpl', title='Home Page', year=year)
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        <script type="text/javascript" src="jquery/jquery v2.1.0.min.js"></script>
        <script type="text/javascript" src = "js/Gamepad.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
        <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    </head>
    <body>
    <center>
    <div class="container">
        <div class="jumbotron">
            <h1>USST Rover GUI</h1>
            <p>Click the button below to run Gamepad and Interact with the Rover!</p>
            <button class = "btn btn-primary" onclick ="location.href='/gamepad'">Run Gamepad </button>
            <p></p>
            <div class = "row text-center">
                <img src = "USST Logo.png" class="img-rounded" alt="Cinque Terre" width="757" height="477">
            </div>
  </div>
    </center>
</body>
</html> 
