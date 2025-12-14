document.addEventListener('DOMContentLoaded', () => {
  const path = location.pathname;
  if (path.startsWith('/ui/preguntas')) initPreguntas();
  if (path.startsWith('/ui/sesiones')) initSesiones();
  if (path.startsWith('/ui/estadisticas')) initEstadisticas();
  if (path.startsWith('/ui/quiz')) initQuiz();
});

// ==================== QUIZ FLOW ====================
async function initQuiz(){
  const startBtn = document.getElementById('startQuiz');
  const cantidadInput = document.getElementById('cantidad');
  const setupMsg = document.getElementById('setupMsg');
  const questionArea = document.getElementById('questionArea');
  const questionEl = document.getElementById('enunciado');
  const optionsEl = document.getElementById('options');
  const progressCur = document.getElementById('curIdx');
  const progressTotal = document.getElementById('totalCount');
  const feedback = document.getElementById('feedback');
  const nextBtn = document.getElementById('nextBtn');
  const resultArea = document.getElementById('resultArea');
  const scoreEl = document.getElementById('score');
  const percentageEl = document.getElementById('percentage');
  const resultMsg = document.getElementById('resultMessage');
  const progressFill = document.getElementById('progressFill');
  const correctCountEl = document.getElementById('correctCount');

  let preguntas = [];
  let respuestas_usuario = []; // Guardar respuestas para el resumen
  let cur = 0;
  let sesionId = null;
  let correctas = 0;
  let respondida = false; // Flag para saber si la pregunta actual fue respondida

  startBtn?.addEventListener('click', async ()=>{
    const cantidad = parseInt(cantidadInput.value||5,10);
    setupMsg.textContent = 'Creando sesión y cargando preguntas...';
    
    // crear sesion
    const s = await fetch('/sesiones/', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify({usuario_nombre:null})});
    if (!s.ok){ setupMsg.textContent = 'Error creando sesión'; return }
    const sjson = await s.json(); 
    sesionId = sjson.id;
    
    // fetch preguntas aleatorias
    const pq = await fetch(`/preguntas/aleatorias?cantidad=${cantidad}`);
    if (!pq.ok){ setupMsg.textContent = 'Error cargando preguntas'; return }
    preguntas = await pq.json();
    if (!preguntas.length){ setupMsg.textContent = 'No hay preguntas disponibles'; return }
    
    // Inicializar
    cur = 0; 
    correctas = 0;
    respondida = false;
    respuestas_usuario = [];
    progressTotal.textContent = preguntas.length; 
    setupMsg.textContent = '';
    document.getElementById('setup').style.display='none';
    questionArea.style.display='block';
    nextBtn.style.display='none';
    renderQuestion();
  });

  function renderQuestion(){
    if (cur >= preguntas.length){ finishQuiz(); return }
    
    const p = preguntas[cur];
    respondida = false;
    
    // Actualizar progreso
    progressCur.textContent = (cur+1).toString();
    progressFill.style.width = ((cur / preguntas.length) * 100) + '%';
    correctCountEl.textContent = correctas.toString();
    
    questionEl.textContent = p.enunciado;
    optionsEl.innerHTML = '';
    feedback.textContent = '';
    feedback.style.display = 'none';
    nextBtn.style.display = 'none';
    
    // Crear botones de opciones
    p.opciones.forEach((opt, idx)=>{
      const b = document.createElement('button');
      b.className = 'option-btn';
      b.textContent = opt;
      b.addEventListener('click', async ()=>{
        if(respondida) return; // Evitar múltiples respuestas
        respondida = true;
        
        // Deshabilitar todos los botones
        Array.from(optionsEl.children).forEach(x=>x.disabled=true);
        
        // Enviar respuesta
        const body = { sesion_id: sesionId, pregunta_id: p.id, opcion_seleccionada: idx };
        const r = await fetch('/respuestas/', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
        
        if (!r.ok){ 
          feedback.textContent = 'Error enviando respuesta'; 
          feedback.style.display = 'block';
          return 
        }
        
        const rr = await r.json();
        
        // Feedback visual
        if (rr.correcta){ 
          b.classList.add('correct'); 
          feedback.textContent = '✓ ¡Correcto!';
          feedback.classList.add('correct');
          correctas++;
          correctCountEl.textContent = correctas.toString();
        } else { 
          b.classList.add('wrong'); 
          feedback.textContent = '✗ Incorrecto';
          feedback.classList.add('wrong');
          
          // Highlight correct option
          const correctIdx = p.respuesta_correcta;
          if (optionsEl.children[correctIdx]) {
            optionsEl.children[correctIdx].classList.add('correct');
          }
        }
        
        feedback.style.display = 'block';
        nextBtn.style.display = 'block';
        
        // Guardar respuesta del usuario para el resumen
        respuestas_usuario.push({
          pregunta: p.enunciado,
          respuesta_usuario: p.opciones[idx],
          respuesta_correcta: p.opciones[p.respuesta_correcta],
          correcta: rr.correcta
        });
      });
      optionsEl.appendChild(b);
    });
  }

  nextBtn?.addEventListener('click', ()=>{
    cur++;
    renderQuestion();
  });

  async function finishQuiz(){
    // Finalizar sesion
    const f = await fetch(`/sesiones/${sesionId}/finalizar`, {method:'POST'});
    let resumen = {};
    if (f.ok) resumen = await f.json();
    
    // Mostrar resultados
    document.getElementById('questionArea').style.display='none';
    resultArea.style.display='block';
    
    const total = preguntas.length;
    const porcentaje = Math.round((correctas / total) * 100);
    
    scoreEl.textContent = `${correctas}/${total}`;
    percentageEl.textContent = `${porcentaje}%`;
    
    // Mensaje personalizado según el resultado
    if (porcentaje === 100) {
      resultMsg.textContent = '🎉 ¡Perfecto! ¡Todas las respuestas correctas!';
    } else if (porcentaje >= 80) {
      resultMsg.textContent = '🌟 ¡Excelente! Muy buen desempeño.';
    } else if (porcentaje >= 60) {
      resultMsg.textContent = '👍 ¡Bien! Sigue practicando.';
    } else if (porcentaje >= 40) {
      resultMsg.textContent = '💪 Necesitas practicar más.';
    } else {
      resultMsg.textContent = '📚 Revisa los conceptos y vuelve a intentar.';
    }
    
    // Mostrar resumen de respuestas
    const summaryContainer = document.getElementById('summaryContainer');
    summaryContainer.innerHTML = '';
    respuestas_usuario.forEach((resp, idx) => {
      const div = document.createElement('div');
      div.style.cssText = 'margin-bottom: 20px; padding: 16px; border-left: 4px solid ' + 
        (resp.correcta ? '#10b981' : '#ef4444') + '; background: ' + 
        (resp.correcta ? '#f0fdf4' : '#fef2f2') + '; border-radius: 4px;';
      div.innerHTML = `
        <div style="font-weight: 600; color: #1f2937; margin-bottom: 8px;">
          ${idx + 1}. ${resp.pregunta}
        </div>
        <div style="font-size: 14px; margin-bottom: 6px;">
          <strong>Tu respuesta:</strong> ${resp.respuesta_usuario}
          ${resp.correcta ? ' ✓' : ' ✗'}
        </div>
        ${!resp.correcta ? `<div style="font-size: 14px; color: #10b981;">
          <strong>Respuesta correcta:</strong> ${resp.respuesta_correcta}
        </div>` : ''}
      `;
      summaryContainer.appendChild(div);
    });
  }
}

// ==================== PREGUNTAS ====================
async function initPreguntas(){
  const cont = document.getElementById('preguntasContainer');
  const res = await fetch('/preguntas/');
  const preguntas = await res.json();
  cont.innerHTML = '';
  preguntas.forEach(p => {
    const el = document.createElement('div');
    el.className = 'pregunta';
    el.innerHTML = `<strong>#${p.id}</strong> ${p.enunciado} <em>(${p.categoria || 'sin categoría'})</em>`;
    cont.appendChild(el);
  });

  const form = document.getElementById('formCrear');
  if (form) form.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const data = new FormData(form);
    const opciones = data.get('opciones').split('|').map(s=>s.trim()).filter(s=>s.length);
    const body = {
      enunciado: data.get('enunciado'),
      opciones,
      respuesta_correcta: parseInt(data.get('respuesta_correcta')||0,10),
      categoria: data.get('categoria')||null,
      dificultad: data.get('dificultad')?parseInt(data.get('dificultad'),10):null
    };
    const r = await fetch('/preguntas/', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
    const text = document.getElementById('crearMsg');
    if (r.ok){ text.textContent = 'Pregunta creada'; form.reset(); initPreguntas(); }
    else { const err = await r.text(); text.textContent = 'Error: '+err }
  });
}

// ==================== SESIONES ====================
async function initSesiones(){
  const f = document.getElementById('formCrearSesion');
  if (f) f.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const data = new FormData(f);
    const body = { usuario_nombre: data.get('usuario_nombre') || null };
    const r = await fetch('/sesiones/', {method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
    const msg = document.getElementById('crearSesionMsg');
    if (r.ok){ const j = await r.json(); msg.textContent = 'Sesión creada id='+j.id } else { msg.textContent = 'Error creando sesión' }
  });

  const ff = document.getElementById('formFinalizar');
  if (ff) ff.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const data = new FormData(ff);
    const sid = data.get('sesion_id');
    const r = await fetch(`/sesiones/${sid}/finalizar`, {method:'POST'});
    const msg = document.getElementById('finalizarMsg');
    if (r.ok) { const j = await r.json(); msg.textContent = 'Finalizada: ' + JSON.stringify(j) } else { msg.textContent = 'Error finalizando' }
  });
}

// ==================== ESTADÍSTICAS ====================
async function initEstadisticas(){
  const g = document.getElementById('globalStats');
  const res = await fetch('/estadisticas/global');
  const j = await res.json();
  g.textContent = JSON.stringify(j);

  const f = document.getElementById('formStatsSesion');
  if (f) f.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const sid = new FormData(f).get('sesion_id');
    const r = await fetch(`/estadisticas/sesion/${sid}`);
    const target = document.getElementById('sesionStats');
    if (r.ok){ const js = await r.json(); target.textContent = JSON.stringify(js); } else { target.textContent = 'Sesión no encontrada' }
  });
}
