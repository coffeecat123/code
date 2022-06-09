<html>
    <head>
        <meta charset="UTF-8">
        <style>
            body{
                font-size:5vw;
            }
        </style>
    </head>
    <body>
        <canvas style="width:227;height:29;z-index:10000000;background-color:white;position:fixed;bottom:0;right:1%;"></canvas>
        <?php
            $a=["/1/123.html","表單",
                "/2/unicode.html","密碼",
                "/3/index.html","排版",
                "/4/1.php","各種文字",
                "/5/1.html","危",
                "/6/1.html","coffeecat"];
            for($i=0;$i<count($a);$i+=2){
                echo "<a href=".$a[$i]." target='_blank'>".$a[$i+1]."</a><br>";
            }
        ?>
    </body>
</html>