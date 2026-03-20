   
document.getElementById('btn-register').addEventListener("click",register);
//document.getElementById("btn-register").addEventListener("click", register());


    function register(){
        // se usa let para determinar que es una varoable que solo vive en ese bloque de codigo, no se puede usar fuera de esa funcion
        // se usa const para determinar que es una variable que no va a cambiar su valor
         const password=document.getElementById("user-password").value;
         const password2=document.getElementById("user-repeat-password").value;

        if (password!=password2){
           Swal.fire({
            icon: 'warning',
            title: 'Contraseñas no coinciden',
            text: 'Por favor verifica que ambas contraseñas sean iguales',
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Entendido',
        });
            return;
            //Sweetalert
        }

        const data= {
            name: document.getElementById('user-name').value,
            email:document.getElementById("user-email").value,
            password:document.getElementById("user-password").value
        }
        //GET es para obtener datos
        // POST es para enviar datos
        // PUT es para actualizar datos
        // DELETE es para eliminar datos
        fetch('api/users', {
            method: 'POST', 
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        }).then(response=> response.json())// una promesa de que regresará algo de la llamada asincrona 
        .then(result=>{
            if(result.success){
                Swal.fire({
                    icon: 'success',
                    title: '¡Registro exitoso!',
                    text: 'Usuario guardado correctamente',
                    confirmButtonColor: '#3085d6',
                    confirmButtonText: 'Continuar'})
            }else{
                 Swal.fire({
                icon: 'error',
                title: 'Error al registrar',
                text: result.message || 'Ocurrió un error al guardar el usuario',
                confirmButtonColor: '#d33',
                confirmButtonText: 'Intentar de nuevo'
            });
            }

        })
        .catch(error=>{
            console.error('Error:', error);
            Swal.fire({
            icon: 'error',
            title: 'Error de conexión',
            text: 'No se pudo conectar con el servidor',
            confirmButtonColor: '#d33',
            confirmButtonText: 'OK'
            });
        });
}
