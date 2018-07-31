/*
*@author:elloit
*@date: 18-7-15
*@github:https://github.com/imjdl
* */

function getFileList(ths) {
    var xmlhttp = getXmlHttp();
    xmlhttp.open("POST",nife_url, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    var url = getID('url').value;
    var pwd = getID('pwd').value;
    var csrf = getName('csrfmiddlewaretoken')[0].value;
    var path = ths.text;
    var data = "url=" + url + "&pwd=" + pwd + "&csrfmiddlewaretoken=" + csrf + "&path=" + path;
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == 4 && xmlhttp.status==200){
            var data = strtojson(xmlhttp.responseText);
            getID('url').value = data['url'];
            getID('pwd').value = data['pwd'];
            // alert(data['files']);
            var bread = getID('bread');
            bread.innerHTML=""
            for(var i=0; i< data['path_list'].length; i++) {
                if (i == data['path_list'].length - 1) {
                    bread.innerHTML = bread.innerHTML + '<li class="active">' + data['path_list'][i] + '</li>';
                } else {
                    bread.innerHTML = bread.innerHTML + '<li><a href="##" onclick="getFileList(this)">' +
                        data['path_list'][i] +'</a></li>';
                }
            }
            var filebody = getID("filesbody");
            filebody.innerHTML="";
            for(var i=0; i < data['files'].length; i++){
                filebody.innerHTML = filebody.innerHTML + '<tr><td>'+data['files'][i]['name']+'' +
                    '</td><td>'+ data['files'][i]['type'] +'</td>'+ '<td>'+ data['files'][i]['time'] +'</td>'+
                '<td>'+ data['files'][i]['size'] +'</td></tr>';
            }
        }
    }
}