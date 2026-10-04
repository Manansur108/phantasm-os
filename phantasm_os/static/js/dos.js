/**
 * Phantasm-OS Phantasm DOS Prompt
 */

window.openDOS = function() {
  let currentDir = 'C:\\';
  const history = [];
  let historyIdx = -1;

  const contentHtml = `
    <div class="dos-container" id="dos-container">
      <div class="dos-output" id="dos-output">Phantasm-OS(R) DOS Version 6.22
(C)Copyright Phantasm Virtual Systems Corp 1981-1995.

Type 'HELP' for a list of available commands.
Type 'DIR' to inspect current directory.
</div>
      <div class="dos-input-line">
        <span class="dos-prompt" id="dos-prompt">${currentDir}&gt;</span>
        <input type="text" class="dos-input" id="dos-input" autofocus spellcheck="false" autocomplete="off" />
      </div>
    </div>
  `;

  const win = window.wm.createWindow({
    id: 'dos',
    title: 'Phantasm DOS Prompt',
    iconSvg: '<svg viewBox="0 0 16 16"><rect x="1" y="2" width="14" height="12" fill="#000" stroke="#888"/><text x="3" y="11" font-size="8" fill="#00ff00">&gt;_</text></svg>',
    width: 600,
    height: 400,
    contentHtml,
    onFocus: () => {
      const input = win.el.querySelector('#dos-input');
      if (input) input.focus();
      window.clippy && window.clippy.interact({ action: 'open_dos' });
    }
  });

  const outputEl = win.el.querySelector('#dos-output');
  const inputEl = win.el.querySelector('#dos-input');
  const promptEl = win.el.querySelector('#dos-prompt');
  const containerEl = win.el.querySelector('#dos-container');

  containerEl.addEventListener('click', () => {
    inputEl.focus();
  });

  inputEl.addEventListener('keydown', async (e) => {
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (historyIdx > 0) {
        historyIdx--;
        inputEl.value = history[historyIdx];
      }
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (historyIdx < history.length - 1) {
        historyIdx++;
        inputEl.value = history[historyIdx];
      } else {
        historyIdx = history.length;
        inputEl.value = '';
      }
    } else if (e.key === 'Enter') {
      const cmd = inputEl.value;
      inputEl.value = '';
      if (cmd.trim()) {
        history.push(cmd);
        historyIdx = history.length;
      }

      outputEl.textContent += `\n${currentDir}>${cmd}`;

      try {
        const res = await fetch('/api/dos/execute', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ command: cmd, current_dir: currentDir })
        });
        const data = await res.json();

        if (data.output === '__CLS__') {
          outputEl.textContent = '';
        } else if (data.output) {
          outputEl.textContent += `\n${data.output}`;
        }

        currentDir = data.new_dir;
        promptEl.textContent = `${currentDir}>`;

        if (data.trigger_glitch) {
          document.body.classList.add('crt-glitch');
          setTimeout(() => document.body.classList.remove('crt-glitch'), 2000);
          window.soundFx && window.soundFx.playDegauss();
        }

      } catch (err) {
        outputEl.textContent += `\nCommand execution error: ${err.message}`;
      }

      containerEl.scrollTop = containerEl.scrollHeight;
    }
  });

  inputEl.focus();
};
