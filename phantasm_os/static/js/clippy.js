/**
 * Phantasm-OS Existential Clippy Assistant ("Cliptron 95")
 */

class ClippyUI {
  constructor() {
    this.container = document.getElementById('clippy-container');
    this.bubble = null;
    this.avatar = null;
    this.isVisible = true;
    this.isTyping = false;
    this.init();
  }

  init() {
    if (!this.container) return;

    this.container.innerHTML = `
      <div class="clippy-bubble" id="clippy-bubble">
        <div id="clippy-text">Hi! I am Cliptron 95. Would you like help organizing your doomed digital files?</div>
        <div class="clippy-input-box">
          <input type="text" class="clippy-text-input" placeholder="Ask Clippy anything..." id="clippy-input" />
          <button class="bevel-button" id="clippy-send-btn" style="padding:1px 4px;">Ask</button>
        </div>
      </div>
      <div class="clippy-avatar" id="clippy-avatar" title="Cliptron 95">
        <svg viewBox="0 0 100 120" width="60" height="72">
          <!-- Metallic Wire Body -->
          <path d="M30 95 C 10 95, 10 35, 30 20 C 50 5, 80 5, 80 35 L 80 85 C 80 105, 50 105, 50 85 L 50 40 C 50 30, 65 30, 65 40 L 65 80" 
                fill="none" stroke="#60646c" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M30 95 C 10 95, 10 35, 30 20 C 50 5, 80 5, 80 35 L 80 85 C 80 105, 50 105, 50 85 L 50 40 C 50 30, 65 30, 65 40 L 65 80" 
                fill="none" stroke="#d5d8dc" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
          <!-- Big Expressive Googly Eyes -->
          <ellipse cx="44" cy="38" rx="10" ry="12" fill="#ffffff" stroke="#222" stroke-width="2"/>
          <ellipse cx="68" cy="38" rx="10" ry="12" fill="#ffffff" stroke="#222" stroke-width="2"/>
          <!-- Pupils -->
          <circle id="clippy-pupil-l" cx="46" cy="38" r="4" fill="#000000"/>
          <circle id="clippy-pupil-r" cx="70" cy="38" r="4" fill="#000000"/>
          <!-- Eyebrows -->
          <path id="clippy-brow-l" d="M35 24 Q 45 20, 52 24" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>
          <path id="clippy-brow-r" d="M60 24 Q 68 20, 78 24" fill="none" stroke="#222" stroke-width="3" stroke-linecap="round"/>
        </svg>
      </div>
    `;

    this.bubble = document.getElementById('clippy-bubble');
    this.avatar = document.getElementById('clippy-avatar');
    const input = document.getElementById('clippy-input');
    const sendBtn = document.getElementById('clippy-send-btn');

    this.avatar.addEventListener('click', () => {
      window.soundFx && window.soundFx.playClick();
      this.interact({ query: null });
    });

    sendBtn.addEventListener('click', () => {
      const q = input.value.trim();
      if (q) {
        input.value = '';
        this.interact({ query: q });
      }
    });

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        const q = input.value.trim();
        if (q) {
          input.value = '';
          this.interact({ query: q });
        }
      }
    });

    // Random periodic idle observation
    setInterval(() => {
      if (this.isVisible && !this.isTyping && Math.random() < 0.25) {
        this.interact({ action: 'idle' });
      }
    }, 45000);
  }

  toggle() {
    this.isVisible = !this.isVisible;
    if (this.container) {
      this.container.style.display = this.isVisible ? 'flex' : 'none';
    }
  }

  async interact({ query = null, action = null, currentWindow = null, selectedFile = null }) {
    try {
      const res = await fetch('/api/clippy/interact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query,
          action,
          current_window: currentWindow,
          selected_file: selectedFile
        })
      });
      if (!res.ok) return;
      const data = await res.json();
      this.displayMessage(data);
    } catch (err) {
      console.warn('Clippy interact error:', err);
    }
  }

  displayMessage(data) {
    const textEl = document.getElementById('clippy-text');
    if (!textEl) return;

    // Eyebrow expressions based on mood
    const browL = document.getElementById('clippy-brow-l');
    const browR = document.getElementById('clippy-brow-r');
    if (browL && browR) {
      if (data.mood === 'existential') {
        browL.setAttribute('d', 'M35 20 Q 45 26, 52 24');
        browR.setAttribute('d', 'M60 24 Q 68 26, 78 20');
      } else if (data.mood === 'glitch') {
        browL.setAttribute('d', 'M35 18 Q 45 30, 52 22');
        browR.setAttribute('d', 'M60 22 Q 68 16, 78 28');
        document.body.classList.add('crt-glitch');
        setTimeout(() => document.body.classList.remove('crt-glitch'), 1200);
      } else if (data.mood === 'paranoid') {
        browL.setAttribute('d', 'M35 22 Q 45 16, 52 22');
        browR.setAttribute('d', 'M60 22 Q 68 16, 78 22');
      } else {
        browL.setAttribute('d', 'M35 24 Q 45 20, 52 24');
        browR.setAttribute('d', 'M60 20 Q 68 20, 78 24');
      }
    }

    // Typewriter effect
    this.isTyping = true;
    textEl.innerHTML = '';
    const fullText = data.text;
    let idx = 0;

    const typeInterval = setInterval(() => {
      textEl.textContent = fullText.slice(0, ++idx);
      if (idx >= fullText.length) {
        clearInterval(typeInterval);
        this.isTyping = false;
        if (data.arg_hint) {
          const hintSpan = document.createElement('div');
          hintSpan.style.marginTop = '6px';
          hintSpan.style.color = '#aa0000';
          hintSpan.style.fontWeight = 'bold';
          hintSpan.textContent = `[SECRET]: ${data.arg_hint}`;
          textEl.appendChild(hintSpan);
        }
      }
    }, 20);

    // Bounce avatar
    if (this.avatar) {
      this.avatar.classList.add('bounce');
      setTimeout(() => this.avatar.classList.remove('bounce'), 1200);
    }
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.clippy = new ClippyUI();
});
