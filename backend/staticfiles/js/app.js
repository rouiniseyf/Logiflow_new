

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

