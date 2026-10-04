/**
 * Phantasm-OS CyberMail 95 Client
 */

window.openMail = async function() {
  const contentHtml = `
    <div class="notepad-container">
      <div class="win-menubar">
        <span class="menu-item">File</span>
        <span class="menu-item">Edit</span>
        <span class="menu-item">View</span>
        <span class="menu-item">Mail</span>
        <span class="menu-item">Help</span>
      </div>
      <div class="nav-toolbar">
        <button class="bevel-button btn-compose">✉ New Message</button>
        <button class="bevel-button btn-reply">Reply</button>
        <button class="bevel-button btn-refresh-mail">Send/Receive</button>
      </div>
      <div class="mail-container">
        <div class="mail-sidebar">
          <div class="mail-folder-item active">📁 Inbox</div>
          <div class="mail-folder-item">📤 Outbox</div>
          <div class="mail-folder-item">✉ Sent Items</div>
          <div class="mail-folder-item">🗑 Deleted Items</div>
        </div>
        <div class="mail-main">
          <div class="mail-list">
            <table class="mail-table" id="mail-table">
              <thead>
                <tr>
                  <th style="width:24px;">!</th>
                  <th style="width:140px;">From</th>
                  <th>Subject</th>
                  <th style="width:130px;">Received</th>
                </tr>
              </thead>
              <tbody id="mail-tbody">
                <tr><td colspan="4" style="text-align:center;">Loading mail...</td></tr>
              </tbody>
            </table>
          </div>
          <div class="mail-preview" id="mail-preview">
            Select an email message from the list above to preview.
          </div>
        </div>
      </div>
      <div class="win-statusbar">
        <span id="mail-status-count">3 message(s)</span>
        <span>Phantasm POP3 / SMTP Online</span>
      </div>
    </div>
  `;

  const win = window.wm.createWindow({
    id: 'mail',
    title: 'CyberMail 95 - [Inbox]',
    iconSvg: '<svg viewBox="0 0 16 16"><rect x="1" y="3" width="14" height="10" fill="#ffffcc" stroke="#000"/><polygon points="1,3 8,9 15,3" fill="#eeeeaa" stroke="#000"/></svg>',
    width: 620,
    height: 420,
    contentHtml
  });

  const tbody = win.el.querySelector('#mail-tbody');
  const preview = win.el.querySelector('#mail-preview');
  const countEl = win.el.querySelector('#mail-status-count');
  const composeBtn = win.el.querySelector('.btn-compose');
  const replyBtn = win.el.querySelector('.btn-reply');
  const refreshBtn = win.el.querySelector('.btn-refresh-mail');

  let currentEmails = [];
  let selectedMail = null;

  const loadInbox = async () => {
    try {
      const res = await fetch('/api/mail/inbox');
      if (!res.ok) throw new Error('Failed to load mail');
      currentEmails = await res.json();
      renderTable();
    } catch (err) {
      tbody.innerHTML = `<tr><td colspan="4" style="color:red;">Error loading mail: ${err.message}</td></tr>`;
    }
  };

  const renderTable = () => {
    tbody.innerHTML = '';
    currentEmails.forEach(mail => {
      const tr = document.createElement('tr');
      if (!mail.is_read) tr.classList.add('unread');
      if (selectedMail && selectedMail.id === mail.id) tr.classList.add('selected');

      const flag = mail.is_arg_clue ? '★' : (mail.is_read ? ' ' : '•');
      tr.innerHTML = `
        <td style="color:${mail.is_arg_clue ? '#cc0000' : '#000080'}; font-weight:bold;">${flag}</td>
        <td>${mail.sender}</td>
        <td>${mail.subject}</td>
        <td>${mail.date}</td>
      `;

      tr.addEventListener('click', () => {
        selectedMail = mail;
        mail.is_read = true;
        renderTable();
        preview.textContent = `From: ${mail.sender}\nTo: ${mail.recipient}\nDate: ${mail.date}\nSubject: ${mail.subject}\n\n${mail.body}`;
      });

      tbody.appendChild(tr);
    });

    countEl.textContent = `${currentEmails.length} message(s)`;
  };

  composeBtn.addEventListener('click', () => {
    window.openComposeMail();
  });

  replyBtn.addEventListener('click', () => {
    if (selectedMail) {
      window.openComposeMail(selectedMail.sender, `RE: ${selectedMail.subject}`);
    }
  });

  refreshBtn.addEventListener('click', () => {
    window.soundFx && window.soundFx.playClick();
    loadInbox();
  });

  loadInbox();
};

window.openComposeMail = function(toDefault = 'sysop@phantasm.net', subjectDefault = '') {
  const contentHtml = `
    <div style="display:flex; flex-direction:column; height:100%; padding:6px; background-color:var(--win-gray); gap:6px;">
      <div style="display:flex; align-items:center; gap:6px;">
        <span style="width:50px;">To:</span>
        <input type="text" class="bevel-inset compose-to" value="${toDefault}" style="flex:1; padding:2px 4px;" />
      </div>
      <div style="display:flex; align-items:center; gap:6px;">
        <span style="width:50px;">Subject:</span>
        <input type="text" class="bevel-inset compose-subject" value="${subjectDefault}" style="flex:1; padding:2px 4px;" />
      </div>
      <textarea class="bevel-inset compose-body" style="flex:1; font-family:var(--dos-font); font-size:12px; padding:6px; resize:none;"></textarea>
      <div style="display:flex; justify-content:flex-end; gap:6px;">
        <button class="bevel-button btn-send-now" style="font-weight:bold;">Send</button>
      </div>
    </div>
  `;

  const win = window.wm.createWindow({
    id: 'compose_mail',
    title: 'New Message - CyberMail 95',
    iconSvg: '<svg viewBox="0 0 16 16"><rect x="1" y="3" width="14" height="10" fill="#ffffcc" stroke="#000"/></svg>',
    width: 450,
    height: 320,
    contentHtml
  });

  const sendBtn = win.el.querySelector('.btn-send-now');
  const toInput = win.el.querySelector('.compose-to');
  const subInput = win.el.querySelector('.compose-subject');
  const bodyInput = win.el.querySelector('.compose-body');

  sendBtn.addEventListener('click', async () => {
    const to = toInput.value.trim();
    const subject = subInput.value.trim();
    const body = bodyInput.value.trim();
    if (!to || !body) {
      alert('Please specify recipient and message body.');
      return;
    }

    sendBtn.disabled = true;
    sendBtn.textContent = 'Transmitting...';

    try {
      await fetch('/api/mail/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ to, subject, body })
      });
      window.wm.closeWindow('compose_mail');
      window.soundFx && window.soundFx.playClick();
      // If mail client open, refresh
      const mailWin = window.wm.getWindow('mail');
      if (mailWin) {
        mailWin.el.querySelector('.btn-refresh-mail').click();
      }
    } catch (err) {
      alert(`Send failed: ${err.message}`);
      sendBtn.disabled = false;
      sendBtn.textContent = 'Send';
    }
  });
};
