from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app import app

router = APIRouter()

_DOCS_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
:root {
  --bg: #0f172a; --bg-card: #1e293b; --bg-soft: #334155; --border: #334155;
  --text: #e2e8f0; --text-muted: #94a3b8; --accent: #38bdf8; --accent-hover: #7dd3fc;
  --green: #4ade80; --red: #f87171;
  --shadow: rgba(0,0,0,0.4); --grad: linear-gradient(135deg,#1e293b,#0f172a);
}
:root.light {
  --bg: #f1f5f9; --bg-card: #ffffff; --bg-soft: #e2e8f0; --border: #cbd5e1;
  --text: #1e293b; --text-muted: #64748b; --accent: #0284c7; --accent-hover: #38bdf8;
  --shadow: rgba(0,0,0,0.1); --grad: linear-gradient(135deg,#ffffff,#f1f5f9);
}
body { font-family:'Segoe UI',system-ui,Arial,sans-serif; background:var(--bg); color:var(--text); min-height:100vh; transition:background .3s,color .3s; }

header { background:var(--grad); border-bottom:1px solid var(--border); padding:28px 24px; text-align:center; position:relative; }
header h1 { font-size:2rem; color:var(--accent); letter-spacing:.5px; }
header .subtitle { font-size:.85rem; color:var(--text-muted); margin-top:4px; font-style:italic; }

.header-btns { position:absolute; top:20px; right:24px; display:flex; gap:10px; }
.header-btn { background:var(--bg-card); border:1px solid var(--border); color:var(--text); width:42px; height:42px; border-radius:50%; cursor:pointer; font-size:1.2rem; display:flex; align-items:center; justify-content:center; transition:all .25s; }
.header-btn:hover { border-color:var(--accent); color:var(--accent); transform:scale(1.08); }
.pin-btn { display:none; }
.pin-btn.active { background:var(--accent); color:var(--bg); border-color:var(--accent); }

.content { max-width:1100px; margin:0 auto; padding:0 20px 40px; }

.tab-bar { display:flex; gap:8px; max-width:600px; margin:24px auto; }
.tab { flex:1; background:var(--bg-card); border:1px solid var(--border); color:var(--text-muted); padding:12px 20px; border-radius:12px; cursor:pointer; font-size:1rem; font-weight:600; transition:all .2s; }
.tab:hover { color:var(--text); }
.tab.active { background:var(--accent); color:var(--bg); border-color:var(--accent); }
.tab-content { display:none; }
.tab-content.active { display:block; animation:fadeUp .3s ease; }

.search-box { display:flex; gap:10px; max-width:600px; margin:30px auto; }
.search-box input { flex:1; background:var(--bg-card); border:1px solid var(--border); color:var(--text); padding:14px 18px; border-radius:12px; font-size:1rem; outline:none; transition:border .2s; }
.search-box input:focus { border-color:var(--accent); box-shadow:0 0 0 3px rgba(56,189,248,.18); }
.search-box input::placeholder { color:var(--text-muted); }
.search-box button { background:var(--accent); color:var(--bg); border:none; padding:14px 28px; border-radius:12px; font-size:1rem; font-weight:700; cursor:pointer; transition:all .2s; }
.search-box button:hover { background:var(--accent-hover); transform:translateY(-1px); box-shadow:0 6px 18px var(--shadow); }
.search-box button:disabled { opacity:.5; cursor:wait; }

.weather-result { display:none; }
.weather-result.show { display:block; animation:fadeUp .4s ease; }
@keyframes fadeUp { from{opacity:0;transform:translateY(16px);} to{opacity:1;transform:translateY(0);} }

.weather-card { background:var(--grad); border:1px solid var(--border); border-radius:20px; padding:36px; max-width:700px; margin:0 auto; box-shadow:0 12px 40px var(--shadow); }
.wc-header { display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; }
.wc-city { font-size:1.6rem; font-weight:700; color:var(--accent); }
.wc-country { font-size:1rem; color:var(--text-muted); }
.wc-icon { font-size:4rem; line-height:1; }
.wc-temp { font-size:3.4rem; font-weight:800; color:var(--text); margin:12px 0 4px; }
.wc-desc { font-size:1.15rem; color:var(--text-muted); margin-bottom:24px; }
.wc-feels { font-size:.9rem; color:var(--text-muted); }

.wc-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:14px; margin-top:24px; }
.wc-item { background:var(--bg-soft); border-radius:12px; padding:16px; text-align:center; }
.wc-item .label { font-size:.75rem; color:var(--text-muted); text-transform:uppercase; letter-spacing:.5px; }
.wc-item .value { font-size:1.2rem; font-weight:700; color:var(--text); margin-top:6px; }
.wc-item .emoji { font-size:1.4rem; }

.error-msg { background:var(--bg-card); border:1px solid var(--red); border-radius:14px; padding:24px; text-align:center; color:var(--red); max-width:600px; margin:20px auto; font-size:1.05rem; }
.loader { text-align:center; padding:40px; color:var(--text-muted); font-size:1.1rem; }
.loader .spin { display:inline-block; width:28px; height:28px; border:3px solid var(--border); border-top-color:var(--accent); border-radius:50%; animation:spin .8s linear infinite; margin-right:10px; vertical-align:middle; }
@keyframes spin { to { transform:rotate(360deg); } }

.wc-sun { display:flex; justify-content:space-around; margin-top:20px; padding-top:20px; border-top:1px solid var(--border); }
.wc-sun-item { text-align:center; }
.wc-sun-item .emoji { font-size:1.6rem; }
.wc-sun-item .val { font-size:.95rem; color:var(--text); margin-top:4px; font-weight:600; }
.wc-sun-item .lbl { font-size:.72rem; color:var(--text-muted); }

.suggestions { max-width:600px; margin:20px auto; text-align:center; }
.suggestions p { color:var(--text-muted); margin-bottom:12px; font-size:.95rem; }
.suggestion-list { display:flex; flex-wrap:wrap; gap:10px; justify-content:center; }
.suggestion-btn { background:var(--bg-card); border:1px solid var(--border); color:var(--accent); padding:10px 20px; border-radius:10px; cursor:pointer; font-size:.95rem; font-weight:600; transition:all .2s; }
.suggestion-btn:hover { background:var(--accent); color:var(--bg); border-color:var(--accent); transform:translateY(-2px); box-shadow:0 4px 12px var(--shadow); }

.pinned-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:18px; max-width:1100px; margin:0 auto; }
.pinned-card { background:var(--grad); border:1px solid var(--border); border-radius:16px; padding:22px; box-shadow:0 8px 24px var(--shadow); position:relative; cursor:pointer; transition:transform .2s, box-shadow .2s; }
.pinned-card:hover { transform:translateY(-3px); box-shadow:0 12px 32px var(--shadow); }
.pinned-card .pc-header { display:flex; align-items:center; justify-content:space-between; padding-right:36px; }
.pinned-card .pc-city { font-size:1.25rem; font-weight:700; color:var(--accent); }
.pinned-card .pc-loc { font-size:.85rem; color:var(--text-muted); margin-top:2px; }
.pinned-card .pc-icon { font-size:2.4rem; }
.pinned-card .pc-temp { font-size:2rem; font-weight:800; margin:8px 0 2px; }
.pinned-card .pc-desc { font-size:.95rem; color:var(--text-muted); margin-bottom:6px; }
.pinned-card .pc-feels { font-size:.8rem; color:var(--text-muted); }
.pinned-card .pc-remove { position:absolute; top:12px; right:12px; background:var(--bg-soft); border:1px solid var(--border); color:var(--text-muted); width:30px; height:30px; border-radius:50%; cursor:pointer; font-size:.85rem; display:flex; align-items:center; justify-content:center; transition:all .2s; }
.pinned-card .pc-remove:hover { border-color:var(--red); color:var(--red); }
.pinned-empty { text-align:center; padding:60px 20px; color:var(--text-muted); max-width:500px; margin:0 auto; }
.pinned-empty .emoji { font-size:3rem; }
.pinned-empty p { margin-top:12px; font-size:1.05rem; line-height:1.5; }
"""


@router.get("/docs", include_in_schema=False, tags=["🏠 Início"])
def docs_page():
    return HTMLResponse(f"""
    <!DOCTYPE html>
    <html lang="pt-BR" data-theme="dark">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>☁️ API Clima · Consultar Clima</title>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>☁️</text></svg>">
        <style>{_DOCS_CSS}</style>
      </head>
      <body>
        <header>
          <h1>☁️ API Clima</h1>
          <div class="subtitle">by bobabi</div>
          <div class="header-btns">
            <button class="header-btn pin-btn" id="pinBtn" title="Fixar cidade" onclick="toggleFixar()">📌</button>
            <button class="header-btn" id="themeBtn" title="Alternar tema">🌙</button>
          </div>
        </header>

        <div class="content">
          <div class="tab-bar">
            <button class="tab active" data-tab="buscar" onclick="switchTab('buscar')">🔍 Buscar</button>
            <button class="tab" data-tab="fixadas" onclick="switchTab('fixadas')">📌 Fixadas <span id="fixadasCount"></span></button>
          </div>

          <div class="tab-content active" id="tab-buscar">
            <div class="search-box">
              <input type="text" id="cityInput" placeholder="Digite o nome da cidade (ex: São Paulo, London, Tokyo)..." onkeydown="if(event.key==='Enter')buscarClima()">
              <button id="searchBtn" onclick="buscarClima()">🔍 Buscar</button>
            </div>
            <div id="weatherArea"></div>
          </div>

          <div class="tab-content" id="tab-fixadas">
            <div id="pinnedArea"></div>
          </div>
        </div>

        <script>
          /* === Tema claro/escuro === */
          const root = document.documentElement;
          const themeBtn = document.getElementById('themeBtn');
          function applyTheme(t){{
            root.classList.toggle('light', t==='light');
            themeBtn.textContent = t==='light' ? '☀️' : '🌙';
            localStorage.setItem('clima-theme', t);
          }}
          applyTheme(localStorage.getItem('clima-theme') || 'dark');
          themeBtn.addEventListener('click', () => {{
            applyTheme(root.classList.contains('light') ? 'dark' : 'light');
          }});

          /* === Abas === */
          let abaAtual = 'buscar';
          let refreshTimer = null;
          const REFRESH_MS = 5 * 60 * 1000;
          function switchTab(name) {{
            abaAtual = name;
            document.querySelectorAll('.tab').forEach(function(t) {{ t.classList.toggle('active', t.getAttribute('data-tab') === name); }});
            document.querySelectorAll('.tab-content').forEach(function(c) {{ c.classList.toggle('active', c.id === 'tab-' + name); }});
            if (name === 'fixadas') renderFixadas();
            atualizarRefreshTimer();
          }}
          function atualizarRefreshTimer() {{
            if (refreshTimer) {{ clearInterval(refreshTimer); refreshTimer = null; }}
            if (abaAtual === 'fixadas' && getFixadas().length > 0) {{
              refreshTimer = setInterval(function() {{
                if (abaAtual === 'fixadas') renderFixadas();
              }}, REFRESH_MS);
            }}
          }}

          /* === Cidades fixadas === */
          function getFixadas() {{ return JSON.parse(localStorage.getItem('clima-fixadas') || '[]'); }}
          function salvarFixadas(arr) {{ localStorage.setItem('clima-fixadas', JSON.stringify(arr)); }}
          function chaveFixa(c) {{ return (c.cidade || '') + '|' + (c.estado || '') + '|' + (c.pais || ''); }}
          function isFixada(cidade, estado, pais) {{
            return getFixadas().some(function(c) {{ return chaveFixa(c) === chaveFixa({{cidade:cidade, estado:estado, pais:pais}}); }});
          }}
          function atualizarContador() {{
            const n = getFixadas().length;
            document.getElementById('fixadasCount').textContent = n > 0 ? '(' + n + ')' : '';
          }}
          function atualizarBtnFixar() {{
            const btn = document.getElementById('pinBtn');
            if (!cidadeAtual) {{ btn.style.display = 'none'; btn.classList.remove('active'); return; }}
            btn.style.display = 'flex';
            if (isFixada(cidadeAtual.cidade, cidadeAtual.estado, cidadeAtual.pais)) {{
              btn.classList.add('active');
              btn.textContent = '📌';
              btn.title = 'Desfixar cidade';
            }} else {{
              btn.classList.remove('active');
              btn.textContent = '📍';
              btn.title = 'Fixar cidade';
            }}
          }}
          function toggleFixar() {{
            if (!cidadeAtual) return;
            let arr = getFixadas();
            const k = chaveFixa(cidadeAtual);
            const idx = arr.findIndex(function(c) {{ return chaveFixa(c) === k; }});
            if (idx >= 0) {{
              arr.splice(idx, 1);
            }} else {{
              arr.push({{cidade: cidadeAtual.cidade, estado: cidadeAtual.estado, pais: cidadeAtual.pais}});
            }}
            salvarFixadas(arr);
            atualizarBtnFixar();
            atualizarContador();
            atualizarRefreshTimer();
          }}
          function removerFixada(cidade, estado, pais) {{
            let arr = getFixadas();
            const k = chaveFixa({{cidade:cidade, estado:estado, pais:pais}});
            arr = arr.filter(function(c) {{ return chaveFixa(c) !== k; }});
            salvarFixadas(arr);
            atualizarBtnFixar();
            atualizarContador();
            atualizarRefreshTimer();
            renderFixadas();
          }}

          function renderFixadas() {{
            const area = document.getElementById('pinnedArea');
            const arr = getFixadas();
            atualizarContador();
            if (arr.length === 0) {{
              area.innerHTML = '<div class="pinned-empty"><div class="emoji">📌</div><p>Nenhuma cidade fixada ainda.<br>Pesquise uma cidade e clique no botão 📌 para fixá-la aqui.</p></div>';
              return;
            }}
            area.innerHTML = '<div class="loader"><span class="spin"></span>Carregando cidades fixadas...</div>';
            const cards = new Array(arr.length);
            let done = 0;
            arr.forEach(function(f, i) {{
              let url = '/clima?cidade=' + encodeURIComponent(f.cidade);
              if (f.estado) url += '&estado=' + encodeURIComponent(f.estado);
              fetch(url).then(r => r.json()).then(d => {{
                if (d.dados) {{
                  const dd = d.dados;
                  const t = dd.temperatura;
                  const local = dd.estado ? (dd.pais + ' - ' + dd.estado) : dd.pais;
                  cards[i] = '<div class="pinned-card" data-cidade="' + dd.cidade + '" data-estado="' + (dd.estado||'') + '" data-pais="' + dd.pais + '">'
                    + '<button class="pc-remove" title="Desfixar">✕</button>'
                    + '<div class="pc-header"><div><div class="pc-city">' + dd.cidade + '</div><div class="pc-loc">' + local + '</div></div>'
                    + '<div class="pc-icon">' + dd.clima.icone + '</div></div>'
                    + '<div class="pc-temp">' + t.atual_c + '°C</div>'
                    + '<div class="pc-desc">' + dd.clima.descricao + '</div>'
                    + '<div class="pc-feels">Min ' + t.minima_c + '° / Max ' + t.maxima_c + '° · 💧 ' + t.umidade_pct + '%</div>'
                    + '</div>';
                }} else {{
                  cards[i] = '<div class="pinned-card" data-cidade="' + f.cidade + '" data-estado="' + (f.estado||'') + '">'
                    + '<button class="pc-remove" title="Desfixar">✕</button>'
                    + '<div class="pc-city">' + f.cidade + '</div><div class="pc-desc">Não foi possível carregar o clima.</div></div>';
                }}
              }}).catch(() => {{
                cards[i] = '<div class="pinned-card" data-cidade="' + f.cidade + '"><div class="pc-city">' + f.cidade + '</div><div class="pc-desc">Erro de conexão.</div></div>';
              }}).finally(() => {{
                done++;
                if (done === arr.length) {{
                  area.innerHTML = '<div class="pinned-grid">' + cards.join('') + '</div>';
                  area.querySelectorAll('.pc-remove').forEach(function(btn) {{
                    btn.addEventListener('click', function(e) {{
                      e.stopPropagation();
                      const card = this.closest('.pinned-card');
                      removerFixada(card.getAttribute('data-cidade'), card.getAttribute('data-estado'), card.getAttribute('data-pais'));
                    }});
                  }});
                  area.querySelectorAll('.pinned-card').forEach(function(card) {{
                    card.addEventListener('click', function() {{
                      const c = this.getAttribute('data-cidade');
                      const est = this.getAttribute('data-estado');
                      switchTab('buscar');
                      document.getElementById('cityInput').value = c;
                      buscarClima(est || undefined);
                    }});
                  }});
                }}
              }});
            }});
          }}
          atualizarContador();

          /* === Explorador de Clima === */
          let cidadeAtual = null;
          function buscarClima(estadoSel) {{
            const cidade = document.getElementById('cityInput').value.trim();
            const area = document.getElementById('weatherArea');
            if (!cidade) {{ area.innerHTML = '<div class="error-msg">⚠️ Digite o nome de uma cidade.</div>'; return; }}
            document.getElementById('searchBtn').disabled = true;
            area.innerHTML = '<div class="loader"><span class="spin"></span>Consultando o clima...</div>';
            cidadeAtual = null;
            atualizarBtnFixar();
            let url = '/clima?cidade=' + encodeURIComponent(cidade);
            if (estadoSel) {{ url += '&estado=' + encodeURIComponent(estadoSel); }}
            fetch(url)
              .then(r => r.json().then(d => ({{ok: r.ok, d}})))
              .then(({{ok, d}}) => {{
                document.getElementById('searchBtn').disabled = false;
                if (!ok) {{
                  let html = '<div class="error-msg">❌ ' + (d.detail || 'Erro ao consultar cidade.') + '</div>';
                  if (d.sugestoes && d.sugestoes.length > 0) {{
                    html += '<div class="suggestions"><p>🔍 Você quis dizer:</p><div class="suggestion-list">';
                    d.sugestoes.forEach(function(s) {{
                      html += '<button class="suggestion-btn" data-cidade="' + s + '">' + s + '</button>';
                    }});
                    html += '</div></div>';
                  }}
                  area.innerHTML = html;
                  area.querySelectorAll('.suggestion-btn').forEach(function(btn) {{
                    btn.addEventListener('click', function() {{
                      document.getElementById('cityInput').value = this.getAttribute('data-cidade');
                      buscarClima();
                    }});
                  }});
                  return;
                }}
                if (d.acao === 'selecionar' && d.cidades) {{
                  let html = '<div class="suggestions"><p>' + (d.mensagem || '🔍 Selecione a cidade desejada:') + '</p><div class="suggestion-list">';
                  d.cidades.forEach(function(c) {{
                    let etiqueta = c.nome + (c.estado ? ' — ' + c.pais + ' / ' + c.estado + (c.estado_nome ? ' (' + c.estado_nome + ')' : '') : ' — ' + c.pais);
                    html += '<button class="suggestion-btn" data-estado="' + c.estado + '">' + etiqueta + '</button>';
                  }});
                  html += '</div></div>';
                  area.innerHTML = html;
                  area.querySelectorAll('.suggestion-btn').forEach(function(btn) {{
                    btn.addEventListener('click', function() {{
                      buscarClima(this.getAttribute('data-estado'));
                    }});
                  }});
                  return;
                }}
                renderClima(d);
              }})
              .catch(() => {{
                document.getElementById('searchBtn').disabled = false;
                area.innerHTML = '<div class="error-msg">❌ Erro de conexão com a API.</div>';
              }});
          }}

          function fmtHora(ts) {{
            if (!ts) return '--:--';
            return new Date(ts * 1000).toLocaleTimeString('pt-BR', {{hour:'2-digit',minute:'2-digit'}});
          }}
          function dirVento(deg) {{
            if (deg==null) return '--';
            const dirs=['N','NNE','NE','LNE','L','LSE','SE','SSE','S','SSO','SO','OSO','O','ONO','NO','NNO'];
            return dirs[Math.round(deg/22.5)%16];
          }}

          function renderClima(r) {{
            const d = r.dados;
            const t = d.temperatura;
            const local = d.estado ? (d.pais + ' - ' + d.estado) : d.pais;
            cidadeAtual = {{cidade: d.cidade, estado: d.estado, pais: d.pais}};
            atualizarBtnFixar();
            document.getElementById('weatherArea').innerHTML = `
            <div class="weather-result show">
              <div class="weather-card">
                <div class="wc-header">
                  <div>
                    <div class="wc-city">${{d.cidade}}</div>
                    <div class="wc-country">${{local}} · ${{d.coordenadas.latitude}}, ${{d.coordenadas.longitude}}</div>
                  </div>
                  <div class="wc-icon">${{d.clima.icone}}</div>
                </div>
                <div class="wc-temp">${{t.atual_c}}°C</div>
                <div class="wc-desc">${{d.clima.descricao}}</div>
                <div class="wc-feels">Sensação térmica: ${{t.sensacao_termica_c}}°C · Min ${{t.minima_c}}°C / Max ${{t.maxima_c}}°C</div>
                <div class="wc-grid">
                  <div class="wc-item"><div class="emoji">💧</div><div class="label">Umidade</div><div class="value">${{t.umidade_pct}}%</div></div>
                  <div class="wc-item"><div class="emoji">🧭</div><div class="label">Pressão</div><div class="value">${{t.pressao_hpa}} hPa</div></div>
                  <div class="wc-item"><div class="emoji">🌬️</div><div class="label">Vento</div><div class="value">${{d.vento.velocidade_mps}} m/s ${{dirVento(d.vento.direcao_graus)}}</div></div>
                  <div class="wc-item"><div class="emoji">☁️</div><div class="label">Nuvens</div><div class="value">${{d.nuvens_pct}}%</div></div>
                  <div class="wc-item"><div class="emoji">👁️</div><div class="label">Visibilidade</div><div class="value">${{(d.visibilidade_metros/1000).toFixed(1)}} km</div></div>
                </div>
                <div class="wc-sun">
                  <div class="wc-sun-item"><div class="emoji">🌅</div><div class="val">${{fmtHora(d.sol.nascer)}}</div><div class="lbl">Nascer do sol</div></div>
                  <div class="wc-sun-item"><div class="emoji">🌇</div><div class="val">${{fmtHora(d.sol.por)}}</div><div class="lbl">Pôr do sol</div></div>
                </div>
              </div>
            </div>`;
          }}
        </script>
      </body>
    </html>
    """)
