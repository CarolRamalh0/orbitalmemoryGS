const statusEl       = document.getElementById("status-sistema");
const qtdEventosEl   = document.getElementById("qtd-eventos");
const qtdSensoresEl  = document.getElementById("qtd-sensores");
const historicoEl    = document.querySelector(".historico-container");
const alertasCritico = document.querySelector(".alertas-coluna--critico .alertas-lista");
const statusLabel    = document.querySelector(".status-label");

const btnEnchente   = document.getElementById("btn-enchente");
const btnIncendio   = document.getElementById("btn-incendio");
const btnFalha      = document.getElementById("btn-falha");
const btnSincronizar= document.getElementById("btn-sincronizar");
const btnRestaurar  = document.getElementById("btn-restaurar");

const estado = {
  eventos: 247,
  sensores: 84,
  status: "SINCRONIZADO",
  sincronizando: false
};

function horaAtual() {
  const agora = new Date();
  const h = String(agora.getHours()).padStart(2, "0");
  const m = String(agora.getMinutes()).padStart(2, "0");
  return `${h}:${m}`;
}

function setStatus(texto, classe) {
  statusEl.textContent = texto;
  statusEl.className = "card-value card-value--status";
  if (classe) statusEl.classList.add(classe);
}

function adicionarAlertaCritico(mensagem) {
  const item = document.createElement("li");
  item.className = "alerta-item alerta-item--critico";
  item.setAttribute("role", "alert");
  item.innerHTML = `
    <span class="alerta-hora">${horaAtual()}</span>
    <p class="alerta-msg">${mensagem}</p>
  `;
  alertasCritico.prepend(item);
}

function adicionarEvento(tipo, titulo, desc, classeCard) {
  const card = document.createElement("article");
  card.className = `evento-card evento-card--${classeCard}`;
  card.innerHTML = `
    <header class="evento-header">
      <span class="evento-tipo-badge">${tipo}</span>
      <time class="evento-data">${horaAtual()} — Agora</time>
    </header>
    <h3 class="evento-titulo">${titulo}</h3>
    <p class="evento-desc">${desc}</p>
    <footer class="evento-footer">
      <span class="evento-status evento-status--monitorando">Monitorando</span>
      <span class="evento-sensores">sensores acionados</span>
    </footer>
  `;
  historicoEl.prepend(card);
}

function bloquearBotoes(estado) {
  [btnEnchente, btnIncendio, btnFalha, btnSincronizar].forEach(btn => {
    btn.disabled = estado;
  });
}

btnEnchente.addEventListener("click", function () {
  estado.eventos += 1;
  qtdEventosEl.textContent = estado.eventos;
  setStatus("ALERTA CRÍTICO", "status--critico");
  statusLabel.textContent = "Emergência Ativa";
  adicionarAlertaCritico("Nível do Rio Gravataí crítico — Zona Sul em risco imediato");
  adicionarEvento("Enchente", "Nova ocorrência — Rio Gravataí", "Nível do rio acima do limite operacional. Zona Sul em risco imediato.", "enchente");
  alert("⚠ ALERTA CRÍTICO\nEnchente detectada — Zona Sul.\nEquipes de resposta notificadas.");
});

btnIncendio.addEventListener("click", function () {
  estado.eventos += 1;
  qtdEventosEl.textContent = estado.eventos;
  setStatus("ALERTA", "status--alerta");
  adicionarAlertaCritico("Incêndio detectado — Área Industrial Leste");
  adicionarEvento("Incêndio", "Foco de incêndio — Área Industrial", "Temperatura acima de 400°C detectada por sensor térmico orbital. Risco de expansão.", "incendio");
  alert("⚠ ALERTA\nIncêndio detectado na Área Industrial.\nDados preservados pelo sistema orbital.");
});

btnFalha.addEventListener("click", function () {
  bloquearBotoes(true);
  setStatus("INSTÁVEL", "status--alerta");
  statusLabel.textContent = "Falha de Comunicação";
  estado.sensores -= 6;
  qtdSensoresEl.innerHTML = `${estado.sensores} <span class="card-value-unit">/ 90</span>`;
  adicionarAlertaCritico("Falha de comunicação — Estação Beta-7 sem resposta");
  alert("⚠ FALHA DE COMUNICAÇÃO\nEstação Beta-7 offline.\nSistema orbital assumindo redundância.");

  setTimeout(function () {
    setStatus("RECONECTADO", "status--ok");
    statusLabel.textContent = "Reconexão Estabelecida";
    estado.sensores += 6;
    qtdSensoresEl.innerHTML = `${estado.sensores} <span class="card-value-unit">/ 90</span>`;
    bloquearBotoes(false);
    alert("✓ RECONEXÃO ESTABELECIDA\nEstação Beta-7 restaurada via satélite.");
  }, 4000);
});

btnSincronizar.addEventListener("click", function () {
  if (estado.sincronizando) return;
  estado.sincronizando = true;
  bloquearBotoes(true);

  let contador = 5;
  setStatus(`SINCRONIZANDO ${contador}s`);

  const intervalo = setInterval(function () {
    contador -= 1;
    if (contador > 0) {
      setStatus(`SINCRONIZANDO ${contador}s`);
    } else {
      clearInterval(intervalo);
      estado.sincronizando = false;
      estado.status = "SINCRONIZADO";
      setStatus("SINCRONIZADO");
      statusLabel.textContent = "Sistema Operacional";
      bloquearBotoes(false);
    }
  }, 1000);
});

btnRestaurar.addEventListener("click", function () {
  estado.eventos  = 247;
  estado.sensores = 84;
  estado.status   = "SINCRONIZADO";
  estado.sincronizando = false;

  qtdEventosEl.textContent = estado.eventos;
  qtdSensoresEl.innerHTML  = `${estado.sensores} <span class="card-value-unit">/ 90</span>`;
  setStatus("SINCRONIZADO");
  statusLabel.textContent = "Sistema Operacional";
  bloquearBotoes(false);
});