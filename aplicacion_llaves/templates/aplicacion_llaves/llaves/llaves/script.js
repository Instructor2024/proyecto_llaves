// Lista de usuarios disponibles para asignación
const users = [
  { id: 1, name: "Diego Mendez", role: "Administrador" },
  { id: 2, name: "Ana García", role: "Docente" },
  { id: 3, name: "Carlos López", role: "Conserje" },
  { id: 4, name: "María Rodríguez", role: "Secretaria" },
  { id: 5, name: "Juan Pérez", role: "Vigilante" },
  { id: 6, name: "Laura Martínez", role: "Docente" },
  { id: 7, name: "Roberto Silva", role: "Mantenimiento" },
  { id: 8, name: "Carmen Vega", role: "Coordinadora" },
]

// Datos de ejemplo para las llaves
let keys = [
  {
    id: 1,
    key_code: "A101",
    description: "Aula de Sistemas 1",
    module: 1,
    position: 5,
    key_type: "PHYSICAL",
    status: "disponible",
  },
  {
    id: 2,
    key_code: "LAB201",
    description: "Aula de Química",
    module: 2,
    position: 12,
    key_type: "PHYSICAL",
    status: "asignada",
    assigned_to: "Ana García",
    assigned_at: "2024-01-15T08:30:00",
    expected_return: "2024-01-15T17:00:00",
  },
  {
    id: 3,
    key_code: "AUD301",
    description: "Auditorio Principal",
    module: 1,
    position: 18,
    key_type: "PHYSICAL",
    status: "disponible",
  },
]

// Función para mostrar el modal de agregar llave
function showAddKeyModal() {
  Swal.fire({
    title: "Agregar Nueva Llave",
    html: `
            <div style="text-align: left; margin: 20px 0;">
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Código de Llave:</label>
                <input type="text" id="keyCode" class="swal2-input" placeholder="Ej: A104" style="margin: 0 0 15px 0;">
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Descripción:</label>
                <input type="text" id="keyDescription" class="swal2-input" placeholder="Ej: Oficina de Administración" style="margin: 0 0 15px 0;">
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Módulo del Dispensador (1-4):</label>
                <select id="keyModule" class="swal2-input" style="margin: 0 0 15px 0;">
                    <option value="">Seleccionar módulo</option>
                    <option value="1">Módulo 1</option>
                    <option value="2">Módulo 2</option>
                    <option value="3">Módulo 3</option>
                    <option value="4">Módulo 4</option>
                </select>
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Posición en el Módulo (1-25):</label>
                <select id="keyPosition" class="swal2-input" style="margin: 0 0 15px 0;">
                    <option value="">Seleccionar posición</option>
                </select>
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Tipo de Llave:</label>
                <select id="keyType" class="swal2-input" style="margin: 0 0 15px 0;">
                    <option value="PHYSICAL">Física</option>
                    <option value="DIGITAL">Digital</option>
                    <option value="MASTER">Maestra</option>
                </select>
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Notas (opcional):</label>
                <textarea id="keyNotes" class="swal2-textarea" placeholder="Información adicional sobre la llave" style="margin: 0; min-height: 80px;"></textarea>
            </div>
        `,
    showCancelButton: true,
    confirmButtonText: "Agregar Llave",
    cancelButtonText: "Cancelar",
    width: "500px",
    didOpen: () => {
      // Llenar las posiciones cuando se selecciona un módulo
      const moduleSelect = document.getElementById("keyModule")
      const positionSelect = document.getElementById("keyPosition")

      moduleSelect.addEventListener("change", function () {
        const selectedModule = this.value
        positionSelect.innerHTML = '<option value="">Seleccionar posición</option>'

        if (selectedModule) {
          // Obtener posiciones ocupadas en este módulo
          const occupiedPositions = keys.filter((key) => key.module == selectedModule).map((key) => key.position)

          // Generar opciones para posiciones 1-25
          for (let i = 1; i <= 25; i++) {
            const option = document.createElement("option")
            option.value = i

            if (occupiedPositions.includes(i)) {
              option.text = `Posición ${i} (Ocupada)`
              option.disabled = true
              option.style.color = "#ccc"
            } else {
              option.text = `Posición ${i}`
            }

            positionSelect.appendChild(option)
          }
        }
      })
    },
    preConfirm: () => {
      const keyCode = document.getElementById("keyCode").value
      const keyDescription = document.getElementById("keyDescription").value
      const keyModule = document.getElementById("keyModule").value
      const keyPosition = document.getElementById("keyPosition").value
      const keyType = document.getElementById("keyType").value
      const keyNotes = document.getElementById("keyNotes").value

      if (!keyCode || !keyDescription || !keyModule || !keyPosition) {
        Swal.showValidationMessage("Por favor completa todos los campos obligatorios")
        return false
      }

      // Verificar si el código de llave ya existe
      if (keys.some((key) => key.key_code === keyCode)) {
        Swal.showValidationMessage("El código de llave ya existe")
        return false
      }

      // Verificar si la posición ya está ocupada
      if (keys.some((key) => key.module == keyModule && key.position == keyPosition)) {
        Swal.showValidationMessage("La posición seleccionada ya está ocupada en el dispensador")
        return false
      }

      return {
        keyCode,
        keyDescription,
        keyModule: Number.parseInt(keyModule),
        keyPosition: Number.parseInt(keyPosition),
        keyType,
        keyNotes,
      }
    },
  }).then((result) => {
    if (result.isConfirmed) {
      addNewKey(result.value)
    }
  })
}

// Función para agregar una nueva llave
function addNewKey(keyData) {
  const newKey = {
    id: keys.length + 1,
    key_code: keyData.keyCode,
    description: keyData.keyDescription,
    module: keyData.keyModule,
    position: keyData.keyPosition,
    key_type: keyData.keyType,
    status: "disponible",
    notes: keyData.keyNotes,
  }

  keys.push(newKey)
  renderKeys()

  Swal.fire({
    title: "¡Llave agregada!",
    text: `La llave ${keyData.keyCode} ha sido agregada exitosamente en el Módulo ${keyData.keyModule}, Posición ${keyData.keyPosition} del dispensador`,
    icon: "success",
    confirmButtonText: "Entendido",
  })
}

// Función para renderizar las llaves
function renderKeys() {
  const keysGrid = document.getElementById("keysGrid")
  keysGrid.innerHTML = ""

  keys.forEach((key) => {
    const keyCard = document.createElement("div")
    keyCard.className = "key-card"
    keyCard.onclick = () => showKeyDetails(key)

    const statusClass = `status-${key.status}`
    const statusText = {
      disponible: "Disponible",
      asignada: "Asignada",
      mantenimiento: "Mantenimiento",
    }[key.status]

    keyCard.innerHTML = `
            <div class="key-code">${key.key_code}</div>
            <div class="key-description">${key.description}</div>
            <div class="key-location">Módulo ${key.module} - Posición ${key.position}</div>
            <div class="key-status ${statusClass}">${statusText}</div>
        `

    keysGrid.appendChild(keyCard)
  })
}

// Función para mostrar detalles de una llave
function showKeyDetails(key) {
  const statusText = {
    disponible: "Disponible",
    asignada: "Asignada",
    mantenimiento: "Mantenimiento",
  }[key.status]

  let assignmentInfo = ""
  if (key.status === "asignada") {
    const assignedDate = new Date(key.assigned_at).toLocaleString("es-ES")
    const expectedReturn = key.expected_return
      ? new Date(key.expected_return).toLocaleString("es-ES")
      : "No especificada"
    assignmentInfo = `
            <p><strong>Asignada a:</strong> ${key.assigned_to}</p>
            <p><strong>Fecha de asignación:</strong> ${assignedDate}</p>
            <p><strong>Devolución esperada:</strong> ${expectedReturn}</p>
        `
  }

  Swal.fire({
    title: `Detalles de ${key.key_code}`,
    html: `
            <div style="text-align: left; margin: 20px 0;">
                <p><strong>Descripción:</strong> ${key.description}</p>
                <p><strong>Ubicación en Dispensador:</strong> Módulo ${key.module}, Posición ${key.position}</p>
                <p><strong>Tipo:</strong> ${key.key_type}</p>
                <p><strong>Estado:</strong> ${statusText}</p>
                ${assignmentInfo}
                ${key.notes ? `<p><strong>Notas:</strong> ${key.notes}</p>` : ""}
            </div>
        `,
    showCancelButton: true,
    confirmButtonText:
      key.status === "disponible" ? "Asignar Llave" : key.status === "asignada" ? "Devolver Llave" : "Ver Detalles",
    cancelButtonText: "Cerrar",
    showDenyButton: true,
    denyButtonText: "Editar",
  }).then((result) => {
    if (result.isConfirmed) {
      if (key.status === "disponible") {
        showAssignKeyModal(key)
      } else if (key.status === "asignada") {
        returnKey(key)
      }
    } else if (result.isDenied) {
      showEditKeyModal(key)
    }
  })
}

// Función para mostrar modal de asignación con menú desplegable de usuarios
function showAssignKeyModal(key) {
  const userOptions = users.map((user) => `<option value="${user.id}">${user.name} - ${user.role}</option>`).join("")

  Swal.fire({
    title: `Asignar ${key.key_code}`,
    html: `
            <div style="text-align: left; margin: 20px 0;">
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Seleccionar Usuario:</label>
                <select id="assignUser" class="swal2-input" style="margin: 0 0 15px 0;">
                    <option value="">Seleccionar usuario</option>
                    ${userOptions}
                </select>
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Fecha y hora de devolución esperada:</label>
                <input type="datetime-local" id="returnDate" class="swal2-input" style="margin: 0 0 15px 0;">
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Motivo de asignación:</label>
                <textarea id="assignNotes" class="swal2-textarea" placeholder="Describe el motivo de la asignación" style="margin: 0;"></textarea>
            </div>
        `,
    showCancelButton: true,
    confirmButtonText: "Asignar Llave",
    cancelButtonText: "Cancelar",
    width: "500px",
    didOpen: () => {
      // Establecer fecha mínima como ahora
      const now = new Date()
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
      document.getElementById("returnDate").min = now.toISOString().slice(0, 16)
    },
    preConfirm: () => {
      const userId = document.getElementById("assignUser").value
      const returnDate = document.getElementById("returnDate").value
      const notes = document.getElementById("assignNotes").value

      if (!userId) {
        Swal.showValidationMessage("Por favor selecciona un usuario")
        return false
      }

      if (!returnDate) {
        Swal.showValidationMessage("Por favor especifica la fecha de devolución")
        return false
      }

      const selectedUser = users.find((user) => user.id == userId)

      return {
        userId: Number.parseInt(userId),
        userName: selectedUser.name,
        returnDate,
        notes,
      }
    },
  }).then((result) => {
    if (result.isConfirmed) {
      // Actualizar el estado de la llave
      key.status = "asignada"
      key.assigned_to = result.value.userName
      key.assigned_user_id = result.value.userId
      key.assigned_at = new Date().toISOString()
      key.expected_return = result.value.returnDate
      key.assignment_notes = result.value.notes

      renderKeys()

      Swal.fire({
        title: "¡Llave asignada!",
        html: `
                    <p>La llave <strong>${key.key_code}</strong> ha sido asignada exitosamente.</p>
                    <p><strong>Usuario:</strong> ${result.value.userName}</p>
                    <p><strong>Devolución esperada:</strong> ${new Date(result.value.returnDate).toLocaleString("es-ES")}</p>
                    <p style="margin-top: 15px; padding: 10px; background: #E8F5E8; border-radius: 8px; font-size: 14px;">
                        💡 La llave será dispensada automáticamente del Módulo ${key.module}, Posición ${key.position}
                    </p>
                `,
        icon: "success",
        confirmButtonText: "Entendido",
      })
    }
  })
}

// Función para devolver una llave
function returnKey(key) {
  Swal.fire({
    title: `¿Devolver ${key.key_code}?`,
    html: `
            <p>¿Confirmas que <strong>${key.assigned_to}</strong> ha devuelto la llave?</p>
            <div style="margin: 15px 0; padding: 10px; background: #FFF3E0; border-radius: 8px; font-size: 14px;">
                <strong>Información de asignación:</strong><br>
                Asignada: ${new Date(key.assigned_at).toLocaleString("es-ES")}<br>
                Devolución esperada: ${new Date(key.expected_return).toLocaleString("es-ES")}
            </div>
            <textarea id="returnNotes" class="swal2-textarea" placeholder="Notas sobre la devolución (opcional)" style="margin-top: 10px;"></textarea>
        `,
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "Sí, devolver",
    cancelButtonText: "Cancelar",
    preConfirm: () => {
      return {
        returnNotes: document.getElementById("returnNotes").value,
      }
    },
  }).then((result) => {
    if (result.isConfirmed) {
      // Actualizar el estado de la llave
      key.status = "disponible"
      key.returned_at = new Date().toISOString()
      key.return_notes = result.value.returnNotes

      // Limpiar datos de asignación pero mantener historial
      delete key.assigned_to
      delete key.assigned_user_id
      delete key.assigned_at
      delete key.expected_return
      delete key.assignment_notes

      renderKeys()

      Swal.fire({
        title: "¡Llave devuelta!",
        html: `
                    <p>La llave <strong>${key.key_code}</strong> ha sido marcada como devuelta.</p>
                    <p style="margin-top: 15px; padding: 10px; background: #E8F5E8; border-radius: 8px; font-size: 14px;">
                        💡 La llave ha sido devuelta al Módulo ${key.module}, Posición ${key.position} del dispensador
                    </p>
                `,
        icon: "success",
        confirmButtonText: "Entendido",
      })
    }
  })
}

// Función para editar una llave
function showEditKeyModal(key) {
  Swal.fire({
    title: `Editar ${key.key_code}`,
    html: `
            <div style="text-align: left; margin: 20px 0;">
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Descripción:</label>
                <input type="text" id="editDescription" class="swal2-input" value="${key.description}" style="margin: 0 0 15px 0;">
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Tipo de Llave:</label>
                <select id="editKeyType" class="swal2-input" style="margin: 0 0 15px 0;">
                    <option value="PHYSICAL" ${key.key_type === "PHYSICAL" ? "selected" : ""}>Física</option>
                    <option value="DIGITAL" ${key.key_type === "DIGITAL" ? "selected" : ""}>Digital</option>
                    <option value="MASTER" ${key.key_type === "MASTER" ? "selected" : ""}>Maestra</option>
                </select>
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Estado:</label>
                <select id="editStatus" class="swal2-input" style="margin: 0 0 15px 0;" ${key.status === "asignada" ? "disabled" : ""}>
                    <option value="disponible" ${key.status === "disponible" ? "selected" : ""}>Disponible</option>
                    <option value="mantenimiento" ${key.status === "mantenimiento" ? "selected" : ""}>Mantenimiento</option>
                    ${key.status === "asignada" ? '<option value="asignada" selected>Asignada (No editable)</option>' : ""}
                </select>
                
                <label style="display: block; margin-bottom: 5px; font-weight: 600; color: #333;">Notas:</label>
                <textarea id="editNotes" class="swal2-textarea" style="margin: 0;">${key.notes || ""}</textarea>
            </div>
        `,
    showCancelButton: true,
    confirmButtonText: "Guardar Cambios",
    cancelButtonText: "Cancelar",
    showDenyButton: key.status !== "asignada",
    denyButtonText: "Eliminar Llave",
    denyButtonColor: "#F44336",
    preConfirm: () => {
      const description = document.getElementById("editDescription").value
      const keyType = document.getElementById("editKeyType").value
      const status = document.getElementById("editStatus").value
      const notes = document.getElementById("editNotes").value

      if (!description) {
        Swal.showValidationMessage("La descripción es obligatoria")
        return false
      }

      return { description, keyType, status, notes }
    },
  }).then((result) => {
    if (result.isConfirmed) {
      key.description = result.value.description
      key.key_type = result.value.keyType
      if (key.status !== "asignada") {
        key.status = result.value.status
      }
      key.notes = result.value.notes

      renderKeys()

      Swal.fire({
        title: "¡Cambios guardados!",
        text: `La llave ${key.key_code} ha sido actualizada`,
        icon: "success",
      })
    } else if (result.isDenied) {
      Swal.fire({
        title: "¿Estás seguro?",
        text: `¿Deseas eliminar la llave ${key.key_code}? Esta acción liberará la posición ${key.position} del módulo ${key.module} en el dispensador.`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#F44336",
        cancelButtonColor: "#4CAF50",
        confirmButtonText: "Sí, eliminar",
        cancelButtonText: "Cancelar",
      }).then((deleteResult) => {
        if (deleteResult.isConfirmed) {
          keys = keys.filter((k) => k.id !== key.id)
          renderKeys()

          Swal.fire({
            title: "¡Eliminada!",
            text: `La llave ${key.key_code} ha sido eliminada del sistema`,
            icon: "success",
          })
        }
      })
    }
  })
}

// Inicializar la aplicación
document.addEventListener("DOMContentLoaded", () => {
  renderKeys()
})
