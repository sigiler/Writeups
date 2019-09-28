<?=preg_replace('/(\pL)/e',"\$c++&1?'$1'|~ß:'$1'&ß",$argv[1]);
/*************************************************************

based on pearl version
used bitwise trick for lcfirst and ucfirst
http://www.phpgolf.org/tips
remember to force ISO western on encoding on browser!

optimization:
<?=preg_replace('/\pL/e',"\$c++&1?'$0'|~ß:'$0'&ß",$argv[1]);

fails
<?=preg_replace('/[A-Z]([A-Z])/e',"'$1'^' '",$argv[1]);
<?=preg_filter('//e',"'$1'^' '",$argv[1]);
<?=preg_replace('/[A-Z]([A-Z])/e',"'$1'^' '",$argv[1]);
<?=preg_replace('/([a-zA-Z])/e',"'$1'^' '",$argv[1]);
<?=preg_replace('/(\w)(\w)/e',"ucfirst('$1').lcfirst('$2')",$argv[1]);
<?=join(array_map('ucfirst',str_split($argv[1],2)));
<?=array_reduce(str_split($argv[1]),function($a,$i){return $a.$i;});
<?=preg_replace_callback('/[a-z]/i',function($matches){return $matches[0]^' ';},$s)
<?=join(array_map('strtoupper',preg_split('/[:alpha:].*[:alpha:]/',$argv[1]))
<?=join(preg_split('//',$argv[1],-1,2))
<?$s=$argv[1];for(;++$i<strlen($s);)echo $s;
