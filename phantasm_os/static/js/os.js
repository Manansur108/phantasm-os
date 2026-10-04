/**
 * Phantasm-OS Main Desktop Shell
 * Manages desktop shortcuts, start menu, system tray clock, and boot sequence.
 */

document.addEventListener('DOMContentLoaded', () => {
  const startButton = document.getElementById('start-button');
  const startMenu = document.getElementById('start-menu');
  const clockEl = document.getElementById('tray-clock');
  const crtToggleBtn = document.getElementById('toggle-crt');
  const soundToggleBtn = document.getElementById('toggle-sound');

  // 1. Clock Updates
  const updateClock = () => {
    const now = new Date();
    let hours = now.getHours();
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12 || 12;
    if (clockEl) clockEl.textContent = `${hours}:${minutes} ${ampm}`;
  };
  setInterval(updateClock, 1000);
  updateClock();

  // 2. Start Menu Toggle
  startButton.addEventListener('click', (e) => {
    e.stopPropagation();
    window.soundFx && window.soundFx.playClick();
    const isVisible = startMenu.style.display === 'flex';
    startMenu.style.display = isVisible ? 'none' : 'flex';
    if (!isVisible) {
      startButton.classList.add('pressed');
    } else {
      startButton.classList.remove('pressed');
    }
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('#start-menu') && !e.target.closest('#start-button')) {
      startMenu.style.display = 'none';
      startButton.classList.remove('pressed');
    }
    // Deselect desktop icons
    if (!e.target.closest('.desktop-icon')) {
      document.querySelectorAll('.desktop-icon').forEach(icon => icon.classList.remove('selected'));
    }
  });

  // 3. Desktop Shortcuts Binding
  const setupShortcut = (id, onLaunch) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.addEventListener('click', (e) => {
      e.stopPropagation();
      document.querySelectorAll('.desktop-icon').forEach(icon => icon.classList.remove('selected'));
      el.classList.add('selected');
    });
    el.addEventListener('dblclick', (e) => {
      e.stopPropagation();
      window.soundFx && window.soundFx.playClick();
      onLaunch();
    });
  };

  setupShortcut('icon-my-computer', () => window.openExplorer('C:\\'));
  setupShortcut('icon-navigator', () => window.openNavigator());
  setupShortcut('icon-mail', () => window.openMail());
  setupShortcut('icon-dos', () => window.openDOS());
  setupShortcut('icon-notepad', () => window.openNotepad());
  setupShortcut('icon-arg', () => window.openARGStation());

  // 4. Start Menu Items
  const smPrograms = {
    'sm-nav': () => window.openNavigator(),
    'sm-mail': () => window.openMail(),
    'sm-dos': () => window.openDOS(),
    'sm-notepad': () => window.openNotepad(),
    'sm-arg': () => window.openARGStation(),
    'sm-clippy': () => window.clippy && window.clippy.toggle(),
    'sm-restart': async () => {
      if (confirm('Reboot Phantasm-OS 95? Virtual state will be re-seeded.')) {
        await fetch('/api/system/reset', { method: 'POST' });
        window.location.reload();
      }
    }
  };

  Object.entries(smPrograms).forEach(([itemId, action]) => {
    const item = document.getElementById(itemId);
    if (item) {
      item.addEventListener('click', () => {
        window.soundFx && window.soundFx.playClick();
        startMenu.style.display = 'none';
        startButton.classList.remove('pressed');
        action();
      });
    }
  });

  // 5. CRT Mode Toggle
  if (crtToggleBtn) {
    crtToggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('crt-mode');
      const isCrt = document.body.classList.contains('crt-mode');
      crtToggleBtn.textContent = isCrt ? '📺 CRT: ON' : '📺 CRT: OFF';
      window.soundFx && window.soundFx.playDegauss();
    });
  }

  // 6. Sound FX Toggle
  if (soundToggleBtn) {
    soundToggleBtn.addEventListener('click', () => {
      const isMuted = window.soundFx ? window.soundFx.toggleMute() : false;
      soundToggleBtn.textContent = isMuted ? '🔇 Audio: OFF' : '🔊 Audio: ON';
    });
  }

  // 7. Initial Welcome Boot Sequence
  setTimeout(() => {
    // Play boot chime on first user interaction if audio context suspended
    const playBoot = () => {
      window.soundFx && window.soundFx.playStartupChime();
      document.removeEventListener('click', playBoot);
    };
    document.addEventListener('click', playBoot, { once: true });

    // Open README / Welcome Notepad
    window.openNotepad('C:\\README.TXT');
  }, 300);
});
