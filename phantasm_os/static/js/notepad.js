/**
 * Phantasm-OS Notepad Text Editor
 */

window.openNotepad = async function(filePath = null) {
  let activePath = filePath || 'C:\\MYDOCS\\UNTITLED.TXT';
  let initialContent = '';

  if (filePath) {
    try {
      const node = await window.vfsClient.getNode(filePath);
      initialContent = node.content || '';
    } catch (err) {
      initialContent = `[Error loading file: ${err.message}]`;
    }
  }

  const contentHtml = `
    <div class="notepad-container">
      <div class="win-menubar">
        <span class="menu-item menu-save">File: Save</span>
        <span class="menu-item menu-glitch" style="color:#aa0000;">Glitch File</span>
        <span class="menu-item menu-clear">Clear</span>
      </div>
      <div class="nav-toolbar">
        <span>File:</span>
        <input type="text" class="bevel-inset np-path" value="${activePath}" style="flex:1; padding:2px 4px;" />
        <button class="bevel-button btn-np-save">💾 Save</button>
      </div>
      <textarea class="notepad-textarea bevel-inset" id="np-text" spellcheck="false">${initialContent}</textarea>
      <div class="win-statusbar">
        <span class="np-status">Ready</span>
        <span>Phantasm Text Editor</span>
      </div>
    </div>
  `;

  const win = window.wm.createWindow({
    id: `notepad_${Date.now()}`,
    title: `Notepad - [${activePath.split('\\').pop()}]`,
    iconSvg: '<svg viewBox="0 0 16 16"><rect x="2" y="1" width="12" height="14" fill="#fff" stroke="#000"/><line x1="4" y1="4" x2="12" y2="4" stroke="#888"/><line x1="4" y1="7" x2="12" y2="7" stroke="#888"/></svg>',
    width: 520,
    height: 380,
    contentHtml,
    onFocus: () => {
      window.clippy && window.clippy.interact({ action: 'open_notepad' });
    }
  });

  const textArea = win.el.querySelector('#np-text');
  const pathInput = win.el.querySelector('.np-path');
  const saveBtn = win.el.querySelector('.btn-np-save');
  const saveMenu = win.el.querySelector('.menu-save');
  const glitchMenu = win.el.querySelector('.menu-glitch');
  const clearMenu = win.el.querySelector('.menu-clear');
  const statusEl = win.el.querySelector('.np-status');

  const doSave = async () => {
    const p = pathInput.value.trim();
    const c = textArea.value;
    try {
      await window.vfsClient.writeFile(p, c);
      statusEl.textContent = 'Saved successfully to VFS.';
      win.el.querySelector('.win-title-text').textContent = `Notepad - [${p.split('\\').pop()}]`;
      window.soundFx && window.soundFx.playClick();
    } catch (err) {
      statusEl.textContent = `Save failed: ${err.message}`;
      window.soundFx && window.soundFx.playErrorChord();
    }
  };

  saveBtn.addEventListener('click', doSave);
  saveMenu.addEventListener('click', doSave);

  glitchMenu.addEventListener('click', async () => {
    const p = pathInput.value.trim();
    try {
      const gNode = await window.vfsClient.glitchFile(p, 0.4);
      textArea.value = gNode.content;
      statusEl.textContent = 'File corrupted with glitch noise.';
      window.soundFx && window.soundFx.playDegauss();
      document.body.classList.add('crt-glitch');
      setTimeout(() => document.body.classList.remove('crt-glitch'), 1000);
      window.clippy && window.clippy.interact({ action: 'glitch_file' });
    } catch (err) {
      statusEl.textContent = `Glitch error: ${err.message}`;
    }
  });

  clearMenu.addEventListener('click', () => {
    textArea.value = '';
    statusEl.textContent = 'Buffer cleared.';
  });
};
