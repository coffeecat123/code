<html>
    <head>
        <meta charset="UTF-8">
        <style>
            body{
                font-size:50px;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
                align-content: space-around;
                align-items: center;
            }
            a{
                margin: 30px;
                background: rgb(255 254 109);
            }
        </style>
        <script>
            window.addEventListener("load",()=>{
                setTimeout(()=>{
                    document.querySelectorAll("script")[document.querySelectorAll("script").length-1].remove();
                    document.querySelectorAll("div")[document.querySelectorAll("div").length-1].remove();
                },100);
            });
        </script>
    </head>
    <body>
        <?php
            $a=["/1/123.html","表單",
                "/2/unicode.html","密碼",
                "/3/index.html","排版",
                "/4/1.html","各種文字",
                "/5/1.html","危",
                "/6/1.html","coffeecat",
                "/7/1.php","圖片分享區",
                "/8/1.html","混色器",
                "/9/1.php","時間",
                "/10/1.html","奇怪按鈕",
                "/11/1.html","相反色",
                "/12/1.html","test",
                "/13/1.php","ck",
                "/14/1.html","cr",
                "/15/1.html","cr2",
                "/16/1.html","draw",
                "/17/1.html","1A2B",
                "/18/1.html","img2",
                "/19/1.html","game1",
                "/20/1.html","game2",
                "/21/1.html","game3",
                "/22/1.html","a"];
            for($i=0;$i<count($a);$i+=2){
                echo "<a href=".$a[$i]." target='_blank'>".$a[$i+1]."</a> ";
            }
        ?>
    </body>
</html>