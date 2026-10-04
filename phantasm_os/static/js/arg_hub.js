/**
 * Phantasm-OS Sector 7G ARG Investigation Station
 */

window.openARGStation = async function() {
  const contentHtml = `
    <div class="arg-container">
      <div>
        <span class="arg-badge">PROJECT CHIMERA // SECTOR 7G</span>
        <h2 style="color:#00ffcc; font-size:14px; margin-bottom:4px;">Cyber Mystery Investigation Hub</h2>
        <p style="color:#a0e0c0; font-size:11px;">Track anomalies, crack ciphers, and unlock the Phantasm Core simulation secret.</p>
      </div>

      <div class="arg-box">
        <h4 style="color:#ffff66;">ACTIVE STAGE:</h4>
        <div id="arg-stage-title" style="font-size:12px; font-weight:bold; color:#ffffff; margin:4px 0;">Loading...</div>
        <div id="arg-last-secret" style="color:#00ff99; font-size:11px;"></div>
      </div>

      <div class="arg-box">
        <h4 style="color:#ffff66;">CLUES & DISCOVERED ANOMALIES:</h4>
        <ul id="arg-clues-list" style="padding-left:18px; font-size:11px; margin-top:4px;"></ul>
      </div>

      <div class="arg-box">
        <h4 style="color:#ffff66;">SUBMIT SOLUTION / OVERRIDE PHRASE:</h4>
        <div class="arg-input-row">
          <input type="text" class="bevel-inset" id="arg-solution-input" placeholder="Enter decoded pass-phrase..." style="flex:1; padding:3px 6px; font-family:var(--dos-font);" />
          <button class="bevel-button" id="arg-submit-btn" style="color:#008000; font-weight:bold;">Submit</button>
        </div>
        <div id="arg-submit-result" style="margin-top:6px; font-size:11px; min-height:16px;"></div>
      </div>

      <div class="arg-box">
        <h4 style="color:#ffff66;">SECTOR CIPHER LAB:</h4>
        <div style="display:flex; gap:6px; margin-top:4px;">
          <input type="text" class="bevel-inset" id="cipher-in" placeholder="Ciphertext..." style="flex:1; padding:2px 4px; font-size:11px;" />
          <input type="number" class="bevel-inset" id="cipher-shift" value="7" style="width:45px; padding:2px 4px; font-size:11px;" />
          <button class="bevel-button" id="btn-caesar-dec">Caesar -Shift</button>
        </div>
        <div id="cipher-out" style="margin-top:4px; color:#ffffff; font-size:11px;"></div>
      </div>
    </div>
  `;

  const win = window.wm.createWindow({
    id: 'arg_hub',
    title: 'Sector 7G - Cyber Investigation Hub',
    iconSvg: '<svg viewBox="0 0 16 16"><rect x="1" y="1" width="14" height="14" fill="#000" stroke="#00ffcc"/><circle cx="8" cy="8" r="4" fill="none" stroke="#00ffcc"/><line x1="8" y1="2" x2="8" y2="14" stroke="#00ffcc"/></svg>',
    width: 580,
    height: 480,
    contentHtml
  });

  const stageTitleEl = win.el.querySelector('#arg-stage-title');
  const secretEl = win.el.querySelector('#arg-last-secret');
  const cluesListEl = win.el.querySelector('#arg-clues-list');
  const solInput = win.el.querySelector('#arg-solution-input');
  const submitBtn = win.el.querySelector('#arg-submit-btn');
  const resultEl = win.el.querySelector('#arg-submit-result');

  const cipherIn = win.el.querySelector('#cipher-in');
  const cipherShift = win.el.querySelector('#cipher-shift');
  const cipherBtn = win.el.querySelector('#btn-caesar-dec');
  const cipherOut = win.el.querySelector('#cipher-out');

  const refreshStatus = async () => {
    try {
      const res = await fetch('/api/arg/status');
      const data = await res.json();
      stageTitleEl.textContent = data.stage_title;
      secretEl.textContent = data.last_unlocked_secret ? `[UNLOCKED]: ${data.last_unlocked_secret}` : '';
      cluesListEl.innerHTML = '';
      data.clues_found.forEach(clue => {
        const li = document.createElement('li');
        li.textContent = clue;
        cluesListEl.appendChild(li);
      });
    } catch (err) {
      stageTitleEl.textContent = 'Offline';
    }
  };

  submitBtn.addEventListener('click', async () => {
    const sol = solInput.value.trim();
    if (!sol) return;

    resultEl.textContent = 'Verifying with Sector 7G core...';
    try {
      const res = await fetch('/api/arg/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ solution: sol })
      });
      const data = await res.json();

      if (data.success) {
        resultEl.style.color = '#38ef7d';
        resultEl.textContent = `✔ ${data.message}`;
        window.soundFx && window.soundFx.playStartupChime();
        document.body.classList.add('crt-glitch');
        setTimeout(() => document.body.classList.remove('crt-glitch'), 2000);
        window.clippy && window.clippy.interact({ action: 'solve_stage' });
        refreshStatus();
      } else {
        resultEl.style.color = '#ff4444';
        resultEl.textContent = `✖ ${data.message}`;
        window.soundFx && window.soundFx.playErrorChord();
      }
    } catch (err) {
      resultEl.textContent = `Error: ${err.message}`;
    }
  });

  cipherBtn.addEventListener('click', async () => {
    const txt = cipherIn.value.trim();
    const shift = parseInt(cipherShift.value, 10) || 7;
    if (!txt) return;

    try {
      const res = await fetch(`/api/arg/cipher/caesar?text=${encodeURIComponent(txt)}&shift=${shift}&decrypt=true`, {
        method: 'POST'
      });
      const data = await res.json();
      cipherOut.textContent = `Decrypted: "${data.output}"`;
    } catch (err) {
      cipherOut.textContent = `Cipher error: ${err.message}`;
    }
  });

  refreshStatus();
};
