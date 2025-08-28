//fazer sumir em 2 segundos o alert com  tag
setTimeout(() => {
        const alert = document.getElementById('autoAlert');
        if(alert){
            alert.classList.remove('show');
            alert.classList.add('hide');
        }
    }, 10000);