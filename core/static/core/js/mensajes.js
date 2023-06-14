function eliminarProducto(id){
    Swal.fire({
      title: "Estas seguro ?",
      text: "Estas seguro que deseas eliminar este producto?",
      icon: "question",
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Aceptar'
    }).then((result) => {
      if (result.isConfirmed) {
        window.location.href = "/eliminarproducto/"+id+"/"
      }
    })
}

function confirmarSubscripcion(event) {
  event.preventDefault(); // Evita el envío del formulario

  swal({
    title: "¿Estás seguro de suscribirte?",
    text: "Esta acción no se puede deshacer",
    icon: "warning",
    buttons: {
      cancel: "Cancelar",
      confirm: "Sí, suscribirse"
    },
  })
  .then((value) => {
    if (value) {
      // Si el usuario confirma la suscripción, envía el formulario
      event.target.form.submit();
    }
  });
}

//Desuscribirse
document.getElementById('btnDesuscribirse').addEventListener('click', function(e) {
  e.preventDefault(); // Prevenir el envío del formulario
  
  // Mostrar SweetAlert para confirmar la desuscripción
  Swal.fire({
    title: "Confirmación",
    text: "¿Estás seguro de que deseas desuscribirte?",
    icon: "warning",
    showCancelButton: true,
    buttons: ["Cancelar", "Aceptar"],
    dangerMode: true,
  }).then((confirm) => {
    if (confirm.isConfirmed) {
      // Enviar la solicitud POST una vez confirmada la desuscripción
      document.getElementById('desuscribirse-form').submit();
    }
  });
});

//Subscribirse
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('btnSubscribirse').addEventListener('click', function(e) {
    e.preventDefault(); // Prevenir el envío del formulario
    
    // Mostrar SweetAlert para confirmar la suscripción
    Swal.fire({
      title: "Confirmación",
      text: "¿Estás seguro de que deseas suscribirte?",
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "Aceptar",
      cancelButtonText: "Cancelar",
      dangerMode: true,
    }).then((result) => {
      if (result.isConfirmed) {
        // Enviar la solicitud POST una vez confirmada la suscripción
        document.getElementById('SubscribirseForm').submit();
      }
    });
  });
});













