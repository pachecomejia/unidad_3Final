function deleteClientes(){
    var id_cliente = window.location.search.substring(1);
    console.log("id_cliente: " +id_cliente);
    var token = sessionStorage.getItem('UID')
    var id_cliente = document.getElementById("id_cliente");

   
    var payload ={
        "id_cliente": id_cliente.value,
  
    }
    
    var request = new XMLHttpRequest();
    request.open("DELETE","https://8000-pachecomeji-unidad3fina-mmu6o5n9ekr.ws-us59.gitpod.io/delete/"+ id_cliente,true);
    request.setRequestHeader("Authorization","Bearer " + token);
    request.setRequestHeader("Content-Type","application/json");
    request.setRequestHeader("Accept","application/json");
    

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);
        const status = request.status;


        console.log("Response: " + response);
        console.log("JSON: " + json);
        console.log("Status: " + status);

        if(status == 202){
            alert(json.message);
            window.location.replace("/get_clientes.html");
        }
    

    };
    
    request.send(JSON.stringify(payload));

};