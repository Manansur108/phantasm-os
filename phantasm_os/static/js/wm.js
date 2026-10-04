/**
 * Phantasm-OS Window Manager (WM)
 * Draggable, resizable, minimizable, maximizable windows with taskbar binding.
 */

class WindowManager {
  constructor() {
    this.windows = new Map();
    this.activeWindow = null;
    this.topZ = 100;
    this.taskContainer = document.getElementById('task-items');
    this.desktop = document.getElementById('desktop');
  }

  createWindow({ id, title, iconSvg, width = 500, height = 350, x, y, contentHtml, onFocus, onClose }) {
    if (this.windows.has(id)) {
      this.restoreWindow(id);
      this.bringToFront(id);
      return this.windows.get(id);
    }

    // Default positioning cascading
    const count = this.windows.size;
    const posX = x !== undefined ? x : Math.min(60 + (count % 8) * 25, window.innerWidth - width - 20);
    const posY = y !== undefined ? y : Math.min(40 + (count % 8) * 25, window.innerHeight - height - 50);

    const winEl = document.createElement('div');
    winEl.className = 'win-window';
    winEl.id = `win-${id}`;
    winEl.style.width = `${width}px`;
    winEl.style.height = `${height}px`;
    winEl.style.left = `${Math.max(10, posX)}px`;
    winEl.style.top = `${Math.max(10, posY)}px`;
    winEl.style.zIndex = ++this.topZ;

    winEl.innerHTML = `
      <div class="win-titlebar">
        <div class="win-title-left">
          <span class="win-title-icon">${iconSvg || ''}</span>
          <span class="win-title-text">${title}</span>
        </div>
        <div class="win-controls">
          <button class="win-btn btn-min" title="Minimize">_</button>
          <button class="win-btn btn-max" title="Maximize">□</button>
          <button class="win-btn btn-close" title="Close">×</button>
        </div>
      </div>
      <div class="win-content">
        ${contentHtml || ''}
      </div>
    `;

    this.desktop.appendChild(winEl);

    // Create taskbar button
    const taskBtn = document.createElement('button');
    taskBtn.className = 'bevel-button task-btn pressed';
    taskBtn.id = `task-${id}`;
    taskBtn.innerHTML = `${iconSvg || ''} <span>${title}</span>`;
    this.taskContainer.appendChild(taskBtn);

    const winObj = {
      id,
      el: winEl,
      taskBtn,
      title,
      isMaximized: false,
      isMinimized: false,
      prevBounds: null,
      onFocus,
      onClose
    };

    this.windows.set(id, winObj);

    // Events
    this._attachWindowEvents(winObj);
    this.bringToFront(id);

    return winObj;
  }

  _attachWindowEvents(winObj) {
    const el = winObj.el;
    const titlebar = el.querySelector('.win-titlebar');
    const minBtn = el.querySelector('.btn-min');
    const maxBtn = el.querySelector('.btn-max');
    const closeBtn = el.querySelector('.btn-close');

    // Focus on click
    el.addEventListener('mousedown', () => {
      this.bringToFront(winObj.id);
    });

    // Minimize
    minBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.soundFx && window.soundFx.playClick();
      this.minimizeWindow(winObj.id);
    });

    // Maximize / Restore
    maxBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.soundFx && window.soundFx.playClick();
      this.toggleMaximize(winObj.id);
    });

    // Close
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      window.soundFx && window.soundFx.playClick();
      this.closeWindow(winObj.id);
    });

    // Taskbar button click
    winObj.taskBtn.addEventListener('click', () => {
      window.soundFx && window.soundFx.playClick();
      if (winObj.isMinimized) {
        this.restoreWindow(winObj.id);
        this.bringToFront(winObj.id);
      } else if (this.activeWindow === winObj.id) {
        this.minimizeWindow(winObj.id);
      } else {
        this.bringToFront(winObj.id);
      }
    });

    // Dragging Titlebar
    let isDragging = false;
    let startX = 0, startY = 0, initialLeft = 0, initialTop = 0;

    titlebar.addEventListener('mousedown', (e) => {
      if (e.target.closest('.win-controls')) return;
      if (winObj.isMaximized) return;

      isDragging = true;
      startX = e.clientX;
      startY = e.clientY;
      initialLeft = parseInt(el.style.left, 10);
      initialTop = parseInt(el.style.top, 10);

      const onMouseMove = (moveE) => {
        if (!isDragging) return;
        const dx = moveE.clientX - startX;
        const dy = moveE.clientY - startY;
        const newLeft = Math.max(0, Math.min(window.innerWidth - 100, initialLeft + dx));
        const newTop = Math.max(0, Math.min(window.innerHeight - 60, initialTop + dy));
        el.style.left = `${newLeft}px`;
        el.style.top = `${newTop}px`;
      };

      const onMouseUp = () => {
        isDragging = false;
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', onMouseUp);
      };

      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    });
  }

  bringToFront(id) {
    const target = this.windows.get(id);
    if (!target) return;

    this.windows.forEach((win, winId) => {
      if (winId === id) {
        win.el.classList.remove('inactive');
        win.taskBtn.classList.add('pressed');
      } else {
        win.el.classList.add('inactive');
        win.taskBtn.classList.remove('pressed');
      }
    });

    target.el.style.zIndex = ++this.topZ;
    this.activeWindow = id;
    if (target.onFocus) target.onFocus();
  }

  minimizeWindow(id) {
    const win = this.windows.get(id);
    if (!win) return;
    win.el.style.display = 'none';
    win.isMinimized = true;
    win.taskBtn.classList.remove('pressed');
    if (this.activeWindow === id) {
      this.activeWindow = null;
    }
  }

  restoreWindow(id) {
    const win = this.windows.get(id);
    if (!win) return;
    win.el.style.display = 'flex';
    win.isMinimized = false;
    win.taskBtn.classList.add('pressed');
  }

  toggleMaximize(id) {
    const win = this.windows.get(id);
    if (!win) return;

    if (!win.isMaximized) {
      win.prevBounds = {
        left: win.el.style.left,
        top: win.el.style.top,
        width: win.el.style.width,
        height: win.el.style.height
      };
      win.el.style.left = '0px';
      win.el.style.top = '0px';
      win.el.style.width = '100vw';
      win.el.style.height = 'calc(100vh - 28px)';
      win.isMaximized = true;
      win.el.querySelector('.btn-max').textContent = '❐';
    } else {
      if (win.prevBounds) {
        win.el.style.left = win.prevBounds.left;
        win.el.style.top = win.prevBounds.top;
        win.el.style.width = win.prevBounds.width;
        win.el.style.height = win.prevBounds.height;
      }
      win.isMaximized = false;
      win.el.querySelector('.btn-max').textContent = '□';
    }
  }

  closeWindow(id) {
    const win = this.windows.get(id);
    if (!win) return;
    if (win.onClose) win.onClose();
    win.el.remove();
    win.taskBtn.remove();
    this.windows.delete(id);
    if (this.activeWindow === id) {
      this.activeWindow = null;
    }
  }

  getWindow(id) {
    return this.windows.get(id);
  }
}

window.wm = new WindowManager();
