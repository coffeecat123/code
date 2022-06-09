<html>
    <head>
        <meta charset="UTF-8">
        <title>文字集</title>
        <style>
            html{
                font-size:5vw;
            }
        </style>
    </head>
    <body>
        <canvas style="width:227;height:29;z-index:10000000;background-color:white;position:fixed;bottom:0;right:1%;"></canvas>
        <script>
            // 字串
            //str = "中文";
            // 獲取字元
            //char0 = str.charAt(0); // "中"
            // 數字編碼值
            //code = str.charCodeAt(0); // 20013
            // 編碼互轉
            //str0 = String.fromCharCode(code); // "中"
            // 轉為16進位制陣列
            //code16 = code.toString(16); // "4e2d"
            //143924+34300
            for(i=0;i<143924+34300-18;i++){
                document.write("&#x"+i.toString(16)+";");
                if((i+1)%16==0){
                    document.write("<br>");
                }
            }
        </script>
    </body>
</html>
<!--
function ucd($unicode_str){
    $json = '{"str":"'.$unicode_str.'"}';
    $arr = json_decode($json,true);
    if(empty($arr)) return '';
    return $arr['str'];
}
for($i=0;$i<16*16*16*16;$i++){
    if($i%16==0 && $i>0){
        echo "<br>";
    }
    $e="";
    if($i<16*16*16){
        $e=$e."0";
    }
    if($i<16*16){
        $e=$e."0";
    }
    if($i<16){
        $e=$e."0";
    }
    $eor="";
    $eor="\u".$e.base_convert($i,10,16);
    $woex=ucd($eor);
    echo $woex;
}
-->