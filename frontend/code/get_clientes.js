function get_clientes(){
    var query = window.location.search.substring(1);

    

    console.log("Query: " + query)
    var token = sessionStorage.getItem('UID')
    console.log (token);
    var request = new XMLHttpRequest();
    request.open("GET","https://8000-pachecomeji-unidad3fina-mmu6o5n9ekr.ws-us59.gitpod.io/user/",true);
    request.setRequestHeader("Authorization","Bearer " + token);
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("Accept","application/json");


    const  tabla   = document.getElementById("tabla_clientes");
    const  thead   = document.getElementById("thead_clientes");

    request.onload = () =>{
        const response = request.responseText;
        const json = JSON.parse(response);

        console.log("Response: "+response);
        console.log("JSON: "+typeof json);
        var tbody = document.getElementById("tbody_clientes");


        
        for(let row=0; row<json.length; row++){
            var tr = document.createElement("tr");
            var tr_actualizar       = document.createElement("td");
            var tr_detalles_cliente = document.createElement("td");
            var tr_borrar           = document.createElement("td");
            var tr_id_cliente       = document.createElement("td");
            var tr_nombre           = document.createElement("td");
            var tr_email            = document.createElement("td");
            var tr_numero           = document.createElement("td");

            tr_detalles_cliente.innerHTML        = "<a href='\get_cliente.html?"    +json[row].id_cliente+"'>Detalles_cliente</a>";
            tr_actualizar.innerHTML              = "<a href='\put_clientes.html?"   +json[row].id_cliente+"'>actualizar</a>";
            tr_borrar.innerHTML                  = "<a href='\delete_clientes.html?"+json[row].id_cliente+"'>Borrar</a>";
            tr_id_cliente.innerHTML     = json[row].id_cliente;
            tr_nombre.innerHTML         = json[row].nombre;
            tr_email.innerHTML          = json[row].email;
            tr_numero.innerHTML         = json[row].numero;
           
            tr.appendChild(tr_detalles_cliente);
            tr.appendChild(tr_actualizar);
            tr.appendChild(tr_borrar);
            tr.appendChild(tr_id_cliente);
            tr.appendChild(tr_nombre);
            tr.appendChild(tr_email);
            tr.appendChild(tr_numero);

            tbody.appendChild(tr);


        }
        
    };
    request.send();

};