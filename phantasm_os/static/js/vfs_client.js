/**
 * Phantasm-OS VFS Client & File Explorer
 */

class VFSClient {
  constructor() {
    this.currentPath = 'C:\\';
  }

  async listDir(path = 'C:\\') {
    try {
      const res = await fetch(`/api/vfs/list?path=${encodeURIComponent(path)}`);
      if (!res.ok) throw new Error('Failed to load directory');
      return await res.json();
    } catch (err) {
      console.warn('VFS list error, fallback:', err);
      return [];
    }
  }

  async getNode(path) {
    const res = await fetch(`/api/vfs/node?path=${encodeURIComponent(path)}`);
    if (!res.ok) throw new Error('File not found');
    return await res.json();
  }

  async writeFile(path, content, corrupt = false, corruptLevel = 0.0) {
    const res = await fetch('/api/vfs/write', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path, content, corrupt, corrupt_level: corruptLevel })
    });
    if (!res.ok) throw new Error('Failed to write file');
    return await res.json();
  }

  async deleteFile(path) {
    const res = await fetch(`/api/vfs/node?path=${encodeURIComponent(path)}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error('Failed to delete file');
    return await res.json();
  }

  async glitchFile(path, intensity = 0.5) {
    const res = await fetch(`/api/vfs/glitch?path=${encodeURIComponent(path)}&intensity=${intensity}`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error('Failed to glitch file');
    return await res.json();
  }

  async hallucinateFile(path, theme = null) {
    const res = await fetch('/api/vfs/hallucinate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path, theme })
    });
    if (!res.ok) throw new Error('Failed to hallucinate file');
    return await res.json();
  }
}

window.vfsClient = new VFSClient();

// Open My Computer / File Explorer Window
window.openExplorer = async function(startPath = 'C:\\') {
  let path = startPath;

  const renderFolder = async (folderPath, winEl) => {
    path = folderPath;
    const titleEl = winEl.querySelector('.win-title-text');
    if (titleEl) titleEl.textContent = `Exploring - ${path}`;

    const pathInput = winEl.querySelector('.explorer-path-input');
    if (pathInput) pathInput.value = path;

    const grid = winEl.querySelector('.explorer-grid');
    grid.innerHTML = '<div style="padding:10px;">Loading directory...</div>';

    const nodes = await window.vfsClient.listDir(path);
    grid.innerHTML = '';

    // If not root, show [..] Up Directory
    if (path !== 'C:\\') {
      const upItem = document.createElement('div');
      upItem.className = 'explorer-item';
      upItem.innerHTML = `
        <svg viewBox="0 0 32 32"><path d="M4 10 L12 10 L14 12 L28 12 L28 26 L4 26 Z" fill="#e8a838" stroke="#000"/><path d="M16 16 L16 22 M13 19 L16 16 L19 19" stroke="#000" stroke-width="2" fill="none"/></svg>
        <span>[Up ..]</span>
      `;
      upItem.addEventListener('dblclick', () => {
        window.soundFx && window.soundFx.playClick();
        const parts = path.split('\\').filter(p => p);
        if (parts.length > 1) {
          parts.pop();
          renderFolder(parts[0] + '\\' + parts.slice(1).join('\\'), winEl);
        } else {
          renderFolder('C:\\', winEl);
        }
      });
      grid.appendChild(upItem);
    }

    nodes.forEach(node => {
      const item = document.createElement('div');
      item.className = 'explorer-item';

      let iconSvg = '';
      if (node.is_dir) {
        iconSvg = '<svg viewBox="0 0 32 32"><path d="M4 8 L12 8 L14 11 L28 11 L28 25 L4 25 Z" fill="#ffd040" stroke="#000"/></svg>';
      } else if (node.corrupted) {
        iconSvg = '<svg viewBox="0 0 32 32"><rect x="6" y="4" width="20" height="24" fill="#ff4444" stroke="#000"/><text x="10" y="20" font-size="12" fill="#fff" font-weight="bold">!</text></svg>';
      } else if (node.file_type === 'exe' || node.file_type === 'bat') {
        iconSvg = '<svg viewBox="0 0 32 32"><rect x="4" y="6" width="24" height="20" fill="#3333aa" stroke="#000"/><rect x="6" y="8" width="20" height="4" fill="#fff"/><text x="8" y="20" font-size="8" fill="#fff">EXE</text></svg>';
      } else {
        iconSvg = '<svg viewBox="0 0 32 32"><rect x="6" y="4" width="20" height="24" fill="#ffffff" stroke="#000"/><line x1="10" y1="10" x2="22" y2="10" stroke="#888"/><line x1="10" y1="14" x2="22" y2="14" stroke="#888"/><line x1="10" y1="18" x2="18" y2="18" stroke="#888"/></svg>';
      }

      item.innerHTML = `${iconSvg}<span>${node.name}</span>`;

      item.addEventListener('click', () => {
        grid.querySelectorAll('.explorer-item').forEach(el => el.classList.remove('selected'));
        item.classList.add('selected');
      });

      item.addEventListener('dblclick', async () => {
        window.soundFx && window.soundFx.playClick();
        if (node.is_dir) {
          renderFolder(node.path, winEl);
        } else {
          // Open in Notepad
          window.openNotepad(node.path);
        }
      });

      grid.appendChild(item);
    });

    const statusEl = winEl.querySelector('.explorer-count');
    if (statusEl) statusEl.textContent = `${nodes.length} object(s)`;
  };

  const contentHtml = `
    <div class="explorer-container">
      <div class="nav-toolbar">
        <span>Address:</span>
        <input type="text" class="bevel-inset explorer-path-input" value="${path}" style="flex:1; padding:2px 4px;">
        <button class="bevel-button btn-go">Go</button>
      </div>
      <div class="explorer-grid bevel-inset" style="flex:1;"></div>
      <div class="win-statusbar">
        <span class="explorer-count">0 object(s)</span>
        <span>Phantasm-OS FAT16</span>
      </div>
    </div>
  `;

  const win = window.wm.createWindow({
    id: 'explorer',
    title: `Exploring - ${path}`,
    iconSvg: '<svg viewBox="0 0 16 16"><rect x="1" y="2" width="14" height="12" fill="#ffd040" stroke="#000"/></svg>',
    width: 480,
    height: 340,
    contentHtml
  });

  const goBtn = win.el.querySelector('.btn-go');
  const pathInput = win.el.querySelector('.explorer-path-input');
  goBtn.addEventListener('click', () => {
    renderFolder(pathInput.value, win.el);
  });
  pathInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') renderFolder(pathInput.value, win.el);
  });

  renderFolder(path, win.el);
};
