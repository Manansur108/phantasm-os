/**
 * Phantasm-OS Web Audio Synthesizer
 * Authentic client-side synthesis for 56k dialup handshake,
 * Win95 boot chord, CRT degauss, and UI sound effects.
 */

class PhantasmAudio {
  constructor() {
    this.ctx = null;
    this.muted = false;
    this.isDialing = false;
  }

  init() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  toggleMute() {
    this.muted = !this.muted;
    return this.muted;
  }

  // Windows 95 Startup Chime (Polyphonic Ambient FM/Additive Synthesis)
  playStartupChime() {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    const notes = [130.81, 196.00, 261.63, 329.63, 392.00, 523.25]; // C3, G3, C4, E4, G4, C5
    const now = this.ctx.currentTime;

    notes.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = idx % 2 === 0 ? 'sine' : 'triangle';
      osc.frequency.setValueAtTime(freq, now + idx * 0.08);

      gain.gain.setValueAtTime(0, now);
      gain.gain.linearRampToValueAtTime(0.12 / (idx + 1), now + idx * 0.08 + 0.1);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 3.8);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(now + idx * 0.08);
      osc.stop(now + 4.0);
    });
  }

  // 56k Dial-Up Modem Handshake Synthesis
  playDialupSequence(onComplete) {
    if (this.muted) {
      if (onComplete) onComplete();
      return;
    }
    this.init();
    if (!this.ctx || this.isDialing) {
      if (onComplete) onComplete();
      return;
    }

    this.isDialing = true;
    const now = this.ctx.currentTime;
    let t = now;

    // 1. Dial tone (350Hz + 440Hz dual sine)
    const dtOsc1 = this.ctx.createOscillator();
    const dtOsc2 = this.ctx.createOscillator();
    const dtGain = this.ctx.createGain();
    dtOsc1.frequency.value = 350;
    dtOsc2.frequency.value = 440;
    dtGain.gain.setValueAtTime(0.08, t);
    dtGain.gain.setValueAtTime(0.08, t + 0.8);
    dtGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.9);
    dtOsc1.connect(dtGain);
    dtOsc2.connect(dtGain);
    dtGain.connect(this.ctx.destination);
    dtOsc1.start(t);
    dtOsc2.start(t);
    dtOsc1.stop(t + 0.9);
    dtOsc2.stop(t + 0.9);

    t += 0.95;

    // 2. DTMF Tones (555-0195)
    const dtmfPairs = [
      [770, 1336], [770, 1336], [770, 1336],
      [941, 1336], [697, 1209], [852, 1477], [770, 1336]
    ];
    dtmfPairs.forEach((pair) => {
      const o1 = this.ctx.createOscillator();
      const o2 = this.ctx.createOscillator();
      const g = this.ctx.createGain();
      o1.frequency.value = pair[0];
      o2.frequency.value = pair[1];
      g.gain.setValueAtTime(0.07, t);
      g.gain.setValueAtTime(0.0001, t + 0.08);
      o1.connect(g);
      o2.connect(g);
      g.connect(this.ctx.destination);
      o1.start(t);
      o2.start(t);
      o1.stop(t + 0.09);
      o2.stop(t + 0.09);
      t += 0.12;
    });

    t += 0.5;

    // 3. Answer Tone (2100Hz with phase wobble)
    const ansOsc = this.ctx.createOscillator();
    const ansGain = this.ctx.createGain();
    ansOsc.frequency.setValueAtTime(2100, t);
    ansGain.gain.setValueAtTime(0.09, t);
    ansGain.gain.exponentialRampToValueAtTime(0.0001, t + 1.2);
    ansOsc.connect(ansGain);
    ansGain.connect(this.ctx.destination);
    ansOsc.start(t);
    ansOsc.stop(t + 1.25);

    t += 1.3;

    // 4. Baudot Line Probing Chirps (FSK frequencies hopping)
    const fskOsc = this.ctx.createOscillator();
    const fskGain = this.ctx.createGain();
    fskOsc.type = 'sawtooth';
    fskOsc.frequency.setValueAtTime(980, t);
    fskOsc.frequency.linearRampToValueAtTime(1850, t + 0.3);
    fskOsc.frequency.linearRampToValueAtTime(1200, t + 0.6);
    fskOsc.frequency.linearRampToValueAtTime(2400, t + 0.9);
    fskGain.gain.setValueAtTime(0.06, t);
    fskGain.gain.exponentialRampToValueAtTime(0.0001, t + 1.1);
    fskOsc.connect(fskGain);
    fskGain.connect(this.ctx.destination);
    fskOsc.start(t);
    fskOsc.stop(t + 1.15);

    t += 1.2;

    // 5. White Noise Burst (Carrier training squelch)
    const bufferSize = this.ctx.sampleRate * 1.5;
    const noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }
    const whiteNoise = this.ctx.createBufferSource();
    whiteNoise.buffer = noiseBuffer;
    const filter = this.ctx.createBiquadFilter();
    filter.type = 'bandpass';
    filter.frequency.value = 1600;
    filter.Q.value = 1.8;
    const noiseGain = this.ctx.createGain();
    noiseGain.gain.setValueAtTime(0.08, t);
    noiseGain.gain.exponentialRampToValueAtTime(0.0001, t + 1.4);
    whiteNoise.connect(filter);
    filter.connect(noiseGain);
    noiseGain.connect(this.ctx.destination);
    whiteNoise.start(t);
    whiteNoise.stop(t + 1.45);

    t += 1.5;

    // Complete callback
    const totalDurationMs = (t - now) * 1000;
    setTimeout(() => {
      this.isDialing = false;
      if (onComplete) onComplete();
    }, totalDurationMs);
  }

  // Windows Classic Chord Error Tone
  playErrorChord() {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    const freqs = [523.25, 659.25, 783.99]; // C5, E5, G5
    const now = this.ctx.currentTime;
    freqs.forEach((f) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(f, now);
      gain.gain.setValueAtTime(0.1, now);
      gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.35);
      osc.connect(gain);
      gain.connect(this.ctx.destination);
      osc.start(now);
      osc.stop(now + 0.4);
    });
  }

  // Click Sound
  playClick() {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.frequency.setValueAtTime(1200, now);
    osc.frequency.exponentialRampToValueAtTime(200, now + 0.03);
    gain.gain.setValueAtTime(0.05, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.03);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(now);
    osc.stop(now + 0.04);
  }

  // CRT Degauss Heavy Coil Hum
  playDegauss() {
    if (this.muted) return;
    this.init();
    if (!this.ctx) return;

    const now = this.ctx.currentTime;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(80, now);
    osc.frequency.exponentialRampToValueAtTime(15, now + 0.8);
    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.85);
    osc.connect(gain);
    gain.connect(this.ctx.destination);
    osc.start(now);
    osc.stop(now + 0.9);
  }
}

// Global audio instance
window.soundFx = new PhantasmAudio();
