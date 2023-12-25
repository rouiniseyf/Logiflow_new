
function export_to_excel(table_id){
    
    var records = {
        headers: [], 
        data:[]
    };

    var table = document.getElementById(table_id);

        // GET THE CELLS COLLECTION OF THE CURRENT ROW.
        var objCells = table.rows.item(0).cells;

        for (var j = 0; j < table.rows.item(0).cells.length; j++) {
            records.headers.push(objCells.item(j).innerHTML);
        }

    console.log(records);
    // LOOP THROUGH EACH ROW OF THE TABLE AFTER HEADER.
    for (i = 1; i < table.rows.length; i++) {

        // GET THE CELLS COLLECTION OF THE CURRENT ROW.
        var objCells = table.rows.item(i).cells;
        // LOOP THROUGH EACH CELL OF THE CURENT ROW TO READ CELL VALUES.
        var items = new Array();
        for (var j = 0; j < objCells.length; j++) {
            items.push(objCells.item(j).innerHTML)
        }
        records.data.push(items);
    }

    const csrftoken = getCookie('csrftoken');
    

        fetch(export_to_excel_url, {
        method: 'POST',
        credentials: 'same-origin',
        responseType: 'blob',
        headers:{
            'content_type': 'application/ms-excel',
            'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
            'X-CSRFToken': csrftoken,
        },
            body: JSON.stringify({'data':records}) //JavaScript object of data to POST
        })
        .then(response => {
                return response.blob();  //Convert response to JSON
        })
        .then(data => {
            var a = document.createElement("a");
            a.href = window.URL.createObjectURL(data);
            a.download = "export.xls";
            a.click();
        })


}


function success(){
    Notification('Succès',"L'opération a été effectuée avec succès.",'success');   
}

    


function Notification(header,body,type){
    var type_class = '';
    if(type=='success'){
        type_class = 'border-0 bg-success text-white';
    }else{
        type_class = 'border-0 bg-danger text-white';
    }
    
    new bs5.Toast({
        body: body,
        placement: 'top-right',
        autohide: true,
        delay: 3000,
        animation: true,
        btnCloseWhite: true,
        className: type_class,
    }).show();
}


function printitems(id){
    let sidebaritems = document.getElementsByClassName('sidebarnavitem');

    for (item of sidebaritems){
        if(id == item.id){
            item.classList.add('active')
        }else{
            item.classList.remove('active')    
        }    
    }
} 

function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

function today(){
 var now = new Date();

 var day = ("0" + now.getDate()).slice(-2);
 var month = ("0" + (now.getMonth() + 1)).slice(-2);

 var today = now.getFullYear()+"-"+(month)+"-"+(day) ;

 return today;
}


function get_articles(id_select_gros, is_select_article){
    $.ajax({
            type: 'GET',
            url: get_articles_url,
            data: {
                "gros_id": id_select_gros,
            },
            success: function (response) { 
                is_select_article.innerHTML = "";
                response.data.forEach(item => {
                    var option = document.createElement("option");
                    option.text = item.numero;
                    option.value = item.id;
                    is_select_article.add(option);
                    }
                )
            },
            error: function (response) {
                console.log(response);
            }
        })  
}

