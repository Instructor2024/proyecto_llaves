class KeyDispenserSystem {
  constructor() {
    this.initializeClock()
    this.initializeCountdown()
    this.initializeFingerprintButton()
    this.startAnimations()
  }

  // Reloj en tiempo real
  initializeClock() {
    this.updateClock()
    setInterval(() => this.updateClock(), 1000)
  }

  updateClock() {
    const now = new Date()
    const hours = now.getHours() % 12
    const minutes = now.getMinutes()
    const seconds = now.getSeconds()

    // Calcular ángulos
    const hourAngle = hours * 30 + minutes * 0.5
    const minuteAngle = minutes * 6
    const secondAngle = seconds * 6

    // Aplicar rotaciones al reloj analógico
    const hourHand = document.getElementById("hourHand")
    const minuteHand = document.getElementById("minuteHand")
    const secondHand = document.getElementById("secondHand")

    if (hourHand) hourHand.style.transform = `rotate(${hourAngle}deg)`
    if (minuteHand) minuteHand.style.transform = `rotate(${minuteAngle}deg)`
    if (secondHand) secondHand.style.transform = `rotate(${secondAngle}deg)`
  }

  // Contador regresivo funcional
  initializeCountdown() {
    // Establecer valores específicos para coincidir con la imagen: 30 días, 12 horas, 33 minutos, 39 segundos
    const now = new Date()
    this.targetDate = new Date()
    this.targetDate.setDate(this.targetDate.getDate() + 30)
    this.targetDate.setHours(now.getHours() + 12)
    this.targetDate.setMinutes(now.getMinutes() + 33)
    this.targetDate.setSeconds(now.getSeconds() + 39)

    this.updateCountdown()
    setInterval(() => this.updateCountdown(), 1000)
  }

  updateCountdown() {
    const now = new Date().getTime()
    const distance = this.targetDate.getTime() - now

    if (distance > 0) {
      const days = Math.floor(distance / (1000 * 60 * 60 * 24))
      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60))
      const seconds = Math.floor((distance % (1000 * 60)) / 1000)

      // Actualizar números
      const daysEl = document.getElementById("days")
      const hoursEl = document.getElementById("hours")
      const minutesEl = document.getElementById("minutes")
      const secondsEl = document.getElementById("seconds")

      if (daysEl) daysEl.textContent = days
      if (hoursEl) hoursEl.textContent = hours
      if (minutesEl) minutesEl.textContent = minutes
      if (secondsEl) secondsEl.textContent = seconds

      // Actualizar barras de progreso circulares (se llenan según el progreso)
      this.updateProgressCircle("daysProgress", days, 30)
      this.updateProgressCircle("hoursProgress", hours, 24)
      this.updateProgressCircle("minutesProgress", minutes, 60)
      this.updateProgressCircle("secondsProgress", seconds, 60)

      // Efectos especiales cuando quedan pocos segundos
      if (days === 0 && hours === 0 && minutes === 0 && seconds <= 10) {
        this.addUrgencyEffects()
      }
    } else {
      this.onCountdownComplete()
    }
  }

  // Actualizar la función updateProgressCircle para que se llene de derecha a izquierda
  updateProgressCircle(elementId, current, max) {
    const circle = document.getElementById(elementId)
    if (!circle) return

    const circumference = 2 * Math.PI * 35 // radio = 35

    // Nueva lógica: se llena de derecha a izquierda (sentido horario)
    // Para segundos: se llena cada segundo (0-59)
    // Para minutos: se llena cada minuto (0-59)
    // Para horas: se llena cada hora (0-23)
    // Para días: se llena según el progreso hacia el objetivo

    let progress

    if (elementId === "secondsProgress") {
      // Para segundos: se llena completamente cada 60 segundos
      progress = current / 60
    } else if (elementId === "minutesProgress") {
      // Para minutos: se llena completamente cada 60 minutos
      progress = current / 60
    } else if (elementId === "hoursProgress") {
      // Para horas: se llena completamente cada 24 horas
      progress = current / 24
    } else if (elementId === "daysProgress") {
      // Para días: se llena según el progreso hacia el objetivo
      progress = current / max
    }

    // Calcular offset para llenar de derecha a izquierda (sentido horario)
    const offset = circumference * (1 - progress)

    circle.style.strokeDasharray = circumference
    circle.style.strokeDashoffset = offset

    // Añadir efecto de brillo más intenso cuando está más lleno
    if (progress > 0.8) {
      circle.style.filter = "drop-shadow(0 0 15px rgba(0, 229, 255, 1)) drop-shadow(0 0 25px rgba(0, 229, 255, 0.8))"
      circle.style.stroke = "#00f5ff"
    } else if (progress > 0.5) {
      circle.style.filter = "drop-shadow(0 0 12px rgba(0, 229, 255, 0.9))"
      circle.style.stroke = "#00e5ff"
    } else {
      circle.style.filter = "drop-shadow(0 0 8px rgba(0, 229, 255, 0.6))"
      circle.style.stroke = "#00e5ff"
    }

    // Añadir animación de pulso cuando está casi completo
    if (progress > 0.9) {
      circle.parentElement.style.animation = "progressPulse 0.5s ease-in-out infinite"
    } else {
      circle.parentElement.style.animation = "none"
    }
  }

  addUrgencyEffects() {
    document.body.style.animation = "urgentPulse 0.5s ease-in-out infinite"
  }

  onCountdownComplete() {
    document.querySelectorAll(".countdown-number").forEach((el) => {
      el.textContent = "00"
    })
    this.showCompletionMessage()
  }

  showCompletionMessage() {
    const message = document.createElement("div")
    message.className = "completion-message"
    message.innerHTML = `
            <h2>¡Tiempo Completado!</h2>
            <p>El dispensador está listo para usar</p>
        `
    document.body.appendChild(message)

    setTimeout(() => {
      message.remove()
    }, 5000)
  }

  // Sistema de huella dactilar
  initializeFingerprintButton() {
    const button = document.getElementById("fingerprintBtn")
    const modal = document.getElementById("scanModal")
    const closeBtn = document.getElementById("closeModal")

    if (button) {
      button.addEventListener("click", () => this.startFingerprintScan())
    }

    if (closeBtn) {
      closeBtn.addEventListener("click", () => this.closeScanModal())
    }

    if (modal) {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) this.closeScanModal()
      })
    }
  }

  startFingerprintScan() {
    const modal = document.getElementById("scanModal")
    if (modal) {
      modal.classList.add("active")
      this.simulateScanProcess()
    }
  }

  simulateScanProcess() {
    const statusEl = document.getElementById("scanStatus")
    const progressBar = document.getElementById("scanBar")

    const scanSteps = [
      { text: "Detectando dedo...", progress: 20, delay: 1000 },
      { text: "Escaneando huella...", progress: 50, delay: 2000 },
      { text: "Analizando patrones...", progress: 80, delay: 1500 },
      { text: "Verificando identidad...", progress: 95, delay: 1000 },
      { text: "¡Acceso autorizado!", progress: 100, delay: 1000 },
    ]

    let currentStep = 0

    const processStep = () => {
      if (currentStep < scanSteps.length) {
        const step = scanSteps[currentStep]
        if (statusEl) statusEl.textContent = step.text
        if (progressBar) progressBar.style.width = step.progress + "%"

        if (step.progress === 100) {
          if (statusEl) statusEl.style.color = "#27ae60"
          this.showSuccessEffects()
          setTimeout(() => this.closeScanModal(), 2000)
        } else {
          setTimeout(() => {
            currentStep++
            processStep()
          }, step.delay)
        }
      }
    }

    processStep()
  }

  showSuccessEffects() {
    for (let i = 0; i < 30; i++) {
      this.createSuccessParticle()
    }
  }

  createSuccessParticle() {
    const particle = document.createElement("div")
    particle.className = "success-particle"
    particle.style.cssText = `
            position: fixed;
            width: 8px;
            height: 8px;
            background: #27ae60;
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            left: 50%;
            top: 50%;
            animation: particleExplode 1.5s ease-out forwards;
        `

    const angle = Math.random() * 360
    const velocity = 150 + Math.random() * 150

    particle.style.setProperty("--angle", angle + "deg")
    particle.style.setProperty("--velocity", velocity + "px")

    document.body.appendChild(particle)

    setTimeout(() => particle.remove(), 1500)
  }

  closeScanModal() {
    const modal = document.getElementById("scanModal")
    if (modal) {
      modal.classList.remove("active")

      setTimeout(() => {
        const statusEl = document.getElementById("scanStatus")
        const progressBar = document.getElementById("scanBar")

        if (statusEl) {
          statusEl.textContent = "Coloque su dedo en el escáner"
          statusEl.style.color = "#2c3e50"
        }
        if (progressBar) {
          progressBar.style.width = "0%"
        }
      }, 300)
    }
  }

  // Agregar la animación de pulso para cuando las barras están casi completas
  startAnimations() {
    const style = document.createElement("style")
    style.textContent = `
            @keyframes urgentPulse {
                0%, 100% { filter: brightness(1); }
                50% { filter: brightness(1.3) hue-rotate(15deg); }
            }
            
            @keyframes progressPulse {
                0%, 100% { 
                    transform: scale(1);
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1), 0 0 0 2px rgba(0, 229, 255, 0.3);
                }
                50% { 
                    transform: scale(1.05);
                    box-shadow: 0 15px 40px rgba(0, 229, 255, 0.3), 0 0 0 3px rgba(0, 229, 255, 0.6);
                }
            }
            
            @keyframes particleExplode {
                0% {
                    transform: translate(-50%, -50%) rotate(var(--angle)) translateX(0);
                    opacity: 1;
                    scale: 1;
                }
                100% {
                    transform: translate(-50%, -50%) rotate(var(--angle)) translateX(var(--velocity));
                    opacity: 0;
                    scale: 0.3;
                }
            }
            
            .completion-message {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #27ae60, #2ecc71);
                color: white;
                padding: 40px;
                border-radius: 20px;
                text-align: center;
                z-index: 10000;
                box-shadow: 0 25px 80px rgba(0, 0, 0, 0.3);
                animation: messageAppear 0.6s ease-out;
            }
            
            @keyframes messageAppear {
                0% {
                    opacity: 0;
                    transform: translate(-50%, -50%) scale(0.3);
                }
                100% {
                    opacity: 1;
                    transform: translate(-50%, -50%) scale(1);
                }
            }
            
            .success-particle {
                box-shadow: 0 0 15px #27ae60;
            }
        `
    document.head.appendChild(style)

    this.addInteractiveEffects()
  }

  addInteractiveEffects() {
    document.querySelectorAll(".countdown-circle").forEach((circle) => {
      circle.addEventListener("mouseenter", () => {
        circle.style.transform = "scale(1.15)"
        circle.style.boxShadow = "0 20px 40px rgba(0, 229, 255, 0.4)"
      })

      circle.addEventListener("mouseleave", () => {
        circle.style.transform = "scale(1)"
        circle.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.1)"
      })
    })

    const clock = document.querySelector(".clock")
    if (clock) {
      clock.addEventListener("click", () => {
        this.showTimeInfo()
      })
    }
  }

  showTimeInfo() {
    const now = new Date()
    const timeInfo = document.createElement("div")
    timeInfo.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                left: 20px;
                background: rgba(0, 0, 0, 0.9);
                color: #00e5ff;
                padding: 20px;
                border-radius: 15px;
                z-index: 1000;
                font-family: 'Roboto', sans-serif;
                backdrop-filter: blur(15px);
                border: 1px solid rgba(0, 229, 255, 0.3);
            ">
                <div style="font-size: 18px; margin-bottom: 5px;">Hora actual: ${now.toLocaleTimeString()}</div>
                <div style="font-size: 16px;">Fecha: ${now.toLocaleDateString()}</div>
            </div>
        `

    document.body.appendChild(timeInfo)

    setTimeout(() => {
      timeInfo.remove()
    }, 4000)
  }
}

// Inicializar el sistema cuando se carga la página
document.addEventListener("DOMContentLoaded", () => {
  new KeyDispenserSystem()

  document.body.style.opacity = "0"
  setTimeout(() => {
    document.body.style.transition = "opacity 1.5s ease"
    document.body.style.opacity = "1"
  }, 100)
})

// Efectos adicionales de teclado
document.addEventListener("keydown", (e) => {
  if (e.code === "Space") {
    e.preventDefault()
    const btn = document.getElementById("fingerprintBtn")
    if (btn) btn.click()
  }

  if (e.code === "Escape") {
    const closeBtn = document.getElementById("closeModal")
    if (closeBtn) closeBtn.click()
  }
})
