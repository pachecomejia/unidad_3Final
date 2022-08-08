function add_use(){

    var nombre      = document.getElementById("nombre");
    var email       = document.getElementById("email");
    var numero      = document.getElementById("numero");

    var payload ={
       
        "nombre": nombre.value,
        "email": email.value,
        "numero": numero.value     
    }
  
    console.log("nombre: " + nombre.value);
    console.log("email: " + email.value);
    console.log("numero: " + numero.value);
    var token = sessionStorage.getItem('UID')


    var request = new XMLHttpRequest();
    request.open("POST","https://8000-pachecomeji-unidad3fina-mmu6o5n9ekr.ws-us59.gitpod.io/cliente/",true);
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