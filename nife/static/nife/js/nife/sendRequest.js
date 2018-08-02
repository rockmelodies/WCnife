/*
*@author:elloit
*@date: 18-7-15
*@github:https://github.com/imjdl
* */

// 发送请求文件列表
function getFileList(path) {
    var xmlhttp = getXmlHttp();
    xmlhttp.open("POST",nife_url, true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    // var url = getID('url').value;
    // var pwd = getID('pwd').value;
    var csrf = getName('csrfmiddlewaretoken')[0].value;
    var data = "&csrfmiddlewaretoken=" + csrf + "&path=" + path;
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function() {
        getState(xmlhttp);
    }

}

// 响应处理, 动态创建元素
function  getState(xmlhttp) {
    if (xmlhttp.readyState == 4 && xmlhttp.status==200){
        var data = strtojson(xmlhttp.responseText);
        getID('url').value = data['url'];
        getID('pwd').value = data['pwd'];
        var bread = getID('bread');
        bread.innerHTML="";
        for(var i=0; i< data['path_list'].length; i++) {
            if (i == data['path_list'].length - 1) {
                bread.innerHTML = bread.innerHTML + '<li class="active">' + data['path_list'][i] + '</li>';
            } else {
                bread.innerHTML = bread.innerHTML + '<li><a href="##" onclick="getFileList(this.text)">' +
                        data['path_list'][i] +'</a></li>';
            }
        }
        var filebody = getID("filesbody");
        filebody.innerHTML="";
        for(var i=0; i < data['files'].length; i++){
                if (data['files'][i]['type'] == 'file'){
                    filebody.innerHTML = filebody.innerHTML + '<tr><td><a href='+dow_url+ '/?filename=' + data['files'][i]['name']+'>'+data['files'][i]['name'] +
                    '</td><td><span class="badge badge-info">'+ data['files'][i]['type'] +'</span></td>'+ '<td>'+ data['files'][i]['time'] +'</td>'+
                '<td>'+ data['files'][i]['size'] +'</td><td>' +
                        '<button class="btn btn-warning">重命名</button>' +
                        '<button class="btn btn-danger">删除</button>' +
                        '</td></tr>';
                }else {
                    filebody.innerHTML = filebody.innerHTML + '<tr><td><a href="#" onclick="getMoreFile(this)">'+data['files'][i]['name'] +
                    '</a></td><td><span class="badge badge-info">'+ data['files'][i]['type'] +'</span></td>'+ '<td>'+ data['files'][i]['time'] +'</td>'+
                '<td>'+ data['files'][i]['size'] +'</td><td>' +
                        '<button class="btn btn-warning">重命名</button>' +
                        '<button class="btn btn-danger">删除</button>' +
                        '</td></tr>';
                }
        }
    }
}

// 处理点击文件或目录，文件的话就下载目录的话就进去
function getMoreFile(ths) {
    // 父亲节点的父节点
    var ffnode = ths.parentNode.parentNode;
    // 找到父亲节点的父节点的孩子节点获取类型
    var type_node = ffnode.children[1];
    var file_type = type_node.children[0].innerText;
    if(file_type == 'dir'){
        getFileList(ths.text);

    }
}




