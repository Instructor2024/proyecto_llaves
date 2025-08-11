document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('changeNameForm');
    const menuItems = document.querySelectorAll('.menu-item');
    
    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const nuevoNombre = document.getElementById('nuevoNombre').value.trim();
        const codigo = document.getElementById('codigo').value.trim();
        
        // Validation
        if (!nuevoNombre) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Por favor ingrese el nuevo nombre',
                confirmButtonColor: '#22c55e'
            });
            return;
        }
        
        if (!codigo) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Por favor ingrese el código de verificación',
                confirmButtonColor: '#22c55e'
            });
            return;
        }
        
        // Show loading
        Swal.fire({
            title: 'Enviando correo...',
            text: 'Por favor espere',
            allowOutsideClick: false,
            showConfirmButton: false,
            willOpen: () => {
                Swal.showLoading();
            }
        });
        
        // Simulate API call
        setTimeout(() => {
            // Simulate success
            if (Math.random() > 0.3) {
                Swal.fire({
                    icon: 'success',
                    title: '¡Éxito!',
                    text: 'El correo de verificación ha sido enviado correctamente',
                    confirmButtonColor: '#22c55e'
                }).then(() => {
                    // Reset form
                    document.getElementById('nuevoNombre').value = '';
                    document.getElementById('codigo').value = '';
                });
            } else {
                // Simulate error
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'No se pudo enviar el correo. Verifique el código e intente nuevamente',
                    confirmButtonColor: '#22c55e'
                });
            }
        }, 2000);
    });
    
    // Handle menu item clicks
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const text = this.querySelector('span').textContent;
            
            if (text === 'Cambiar Contraseña') {
                Swal.fire({
                    title: 'Cambiar Contraseña',
                    html: `
                        <input type="password" id="currentPassword" class="swal2-input" placeholder="Contraseña actual">
                        <input type="password" id="newPassword" class="swal2-input" placeholder="Nueva contraseña">
                        <input type="password" id="confirmPassword" class="swal2-input" placeholder="Confirmar contraseña">
                    `,
                    confirmButtonText: 'Cambiar',
                    confirmButtonColor: '#22c55e',
                    showCancelButton: true,
                    cancelButtonText: 'Cancelar',
                    preConfirm: () => {
                        const current = document.getElementById('currentPassword').value;
                        const newPass = document.getElementById('newPassword').value;
                        const confirm = document.getElementById('confirmPassword').value;
                        
                        if (!current || !newPass || !confirm) {
                            Swal.showValidationMessage('Todos los campos son obligatorios');
                            return false;
                        }
                        
                        if (newPass !== confirm) {
                            Swal.showValidationMessage('Las contraseñas no coinciden');
                            return false;
                        }
                        
                        if (newPass.length < 6) {
                            Swal.showValidationMessage('La contraseña debe tener al menos 6 caracteres');
                            return false;
                        }
                        
                        return { current, newPass };
                    }
                }).then((result) => {
                    if (result.isConfirmed) {
                        Swal.fire({
                            icon: 'success',
                            title: '¡Contraseña actualizada!',
                            text: 'Su contraseña ha sido cambiada exitosamente',
                            confirmButtonColor: '#22c55e'
                        });
                    }
                });
            } else if (text === 'Cerrar Sesion') {
                Swal.fire({
                    title: '¿Cerrar sesión?',
                    text: '¿Está seguro que desea cerrar la sesión?',
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonColor: '#22c55e',
                    cancelButtonColor: '#ef4444',
                    confirmButtonText: 'Sí, cerrar sesión',
                    cancelButtonText: 'Cancelar'
                }).then((result) => {
                    if (result.isConfirmed) {
                        Swal.fire({
                            icon: 'success',
                            title: 'Sesión cerrada',
                            text: 'Hasta luego, Diego Mendez',
                            confirmButtonColor: '#22c55e'
                        }).then(() => {
                            // Redirect to login page
                            window.location.href = 'login.html';
                        });
                    }
                });
            }
        });
    });
    
    // Handle back button
    document.querySelector('.back-button').addEventListener('click', function() {
        Swal.fire({
            title: '¿Regresar?',
            text: '¿Desea regresar al menú principal?',
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#22c55e',
            cancelButtonColor: '#6b7280',
            confirmButtonText: 'Sí, regresar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                window.history.back();
            }
        });
    });
    
    // Add some interactive effects
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"]');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'translateY(-2px)';
            this.parentElement.style.transition = 'transform 0.3s ease';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'translateY(0)';
        });
    });
});