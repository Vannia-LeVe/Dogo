    document.getElementById("btn-register").addEventListener("click", register);

    function register(){

         password=document.getElementById("user-password").value;
         password2=document.getElementById("user-repeat-password").value;

        if (password!=password2){
            alert("Las contraseña no coinciden")
            return;
            //Sweetalert
        }

        const data= {
            name: document.getElementById("user-name").value,
            email:document.getElementById("user-email").value,
            password:document.getElementById("user-password").value
        }
    }

