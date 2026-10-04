/**
 * Phantasm-OS Phantasm Navigator (Dial-Up Web Browser)
 */

window.openNavigator = function(initialUrl = 'http://www.geocities.com') {
  let currentUrl = initialUrl;
  let historyStack = [initialUrl];
  let historyIdx = 0;

  const contentHtml = `
    <div class="nav-container">
      <div class="win-menubar">
        <span class="menu-item">File</span>
        <span class="menu-item">Edit</span>
        <span class="menu-item">View</span>
        <span class="menu-item">Bookmarks</span>
        <span class="menu-item">Options</span>
        <span class="menu-item">Directory</span>
        <span class="menu-item">Help</span>
      </div>
      <div class="nav-toolbar">
        <button class="bevel-button nav-back" title="Back">&lt;&lt; Back</button>
        <button class="bevel-button nav-forward" title="Forward">Forward &gt;&gt;</button>
        <button class="bevel-button nav-home" title="Home">Home</button>
        <button class="bevel-button nav-reload" title="Reload">Reload</button>
        <button class="bevel-button nav-dialup" title="Dial-Up Sound" style="color:#000080;">56k Dial</button>
      </div>
      <div class="nav-toolbar">
        <div class="nav-url-bar">
          <span style="font-weight:bold;">Location:</span>
          <input type="text" class="bevel-inset nav-input" value="${currentUrl}" />
          <button class="bevel-button nav-go" style="font-weight:bold;">Go</button>
        </div>
      </div>
      <div class="nav-viewport" id="nav-viewport">
        <div style="padding:20px; font-family:'Times New Roman', serif;">
          Connecting to remote host...
        </div>
      </div>
      <div class="nav-status">
        <span class="nav-status-msg">Opening page...</span>
        <span class="nav-baud-indicator">28,800 bps V.34</span>
      </div>
    </div>
  `;

  const win = window.wm.createWindow({
    id: 'navigator',
    title: `Phantasm Navigator 2.0 - [${currentUrl}]`,
    iconSvg: '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="7" fill="#000080" stroke="#000"/><line x1="1" y1="8" x2="15" y2="8" stroke="#ffffff"/><line x1="8" y1="1" x2="8" y2="15" stroke="#ffffff"/><circle cx="8" cy="8" r="4" fill="none" stroke="#ffffff"/></svg>',
    width: 660,
    height: 480,
    contentHtml,
    onFocus: () => {
      window.clippy && window.clippy.interact({ action: 'open_navigator' });
    }
  });

  const urlInput = win.el.querySelector('.nav-input');
  const goBtn = win.el.querySelector('.nav-go');
  const backBtn = win.el.querySelector('.nav-back');
  const fwdBtn = win.el.querySelector('.nav-forward');
  const homeBtn = win.el.querySelector('.nav-home');
  const reloadBtn = win.el.querySelector('.nav-reload');
  const dialBtn = win.el.querySelector('.nav-dialup');
  const viewport = win.el.querySelector('#nav-viewport');
  const statusMsg = win.el.querySelector('.nav-status-msg');

  const loadUrl = async (url, withSound = false) => {
    currentUrl = url;
    urlInput.value = url;
    statusMsg.textContent = `Connecting to ${url}...`;

    if (withSound && window.soundFx) {
      statusMsg.textContent = 'Dialing ISP 555-0195 (V.90 Handshake)...';
      window.soundFx.playDialupSequence();
    }

    try {
      const res = await fetch('/api/navigator/browse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      if (!res.ok) throw new Error('Network error');
      const data = await res.json();

      win.el.querySelector('.win-title-text').textContent = `Phantasm Navigator 2.0 - [${data.title}]`;
      viewport.innerHTML = data.html_content;
      statusMsg.textContent = 'Document: Done';

      // Intercept in-page hyperlinks
      viewport.querySelectorAll('a').forEach(a => {
        a.addEventListener('click', (e) => {
          const href = a.getAttribute('href');
          if (href && !href.startsWith('mailto:')) {
            e.preventDefault();
            historyStack.push(href);
            historyIdx = historyStack.length - 1;
            loadUrl(href, false);
          }
        });
      });

    } catch (err) {
      viewport.innerHTML = `<div style="padding:20px; color:red;"><h3>Phantasm Navigator Server Error</h3><p>${err.message}</p></div>`;
      statusMsg.textContent = 'Connection failed';
    }
  };

  goBtn.addEventListener('click', () => {
    const u = urlInput.value.trim();
    if (u) {
      historyStack.push(u);
      historyIdx = historyStack.length - 1;
      loadUrl(u, false);
    }
  });

  urlInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const u = urlInput.value.trim();
      if (u) {
        historyStack.push(u);
        historyIdx = historyStack.length - 1;
        loadUrl(u, false);
      }
    }
  });

  backBtn.addEventListener('click', () => {
    if (historyIdx > 0) {
      historyIdx--;
      loadUrl(historyStack[historyIdx], false);
    }
  });

  fwdBtn.addEventListener('click', () => {
    if (historyIdx < historyStack.length - 1) {
      historyIdx++;
      loadUrl(historyStack[historyIdx], false);
    }
  });

  homeBtn.addEventListener('click', () => {
    const home = 'http://www.geocities.com';
    historyStack.push(home);
    historyIdx = historyStack.length - 1;
    loadUrl(home, false);
  });

  reloadBtn.addEventListener('click', () => {
    loadUrl(currentUrl, false);
  });

  dialBtn.addEventListener('click', () => {
    loadUrl(currentUrl, true);
  });

  // Initial load
  loadUrl(initialUrl, false);
};
