// PicoPanda WebSerial bridge for the WASM Studio build.
// Loaded before PicoPanda_Studio.js from wasm/index.html.

(function () {
  'use strict';

  const VID = 0x2e8a;
  const PID = 0x000a;
  const SLOT_SIZE = 131072;
  const PROTOCOL_VERSION = 'PICOPANDA V1';

  const PHASE = {
    IDLE: 0,
    REFRESHING: 1,
    CONNECTING: 2,
    UPLOADING: 3,
    RECONNECTING: 4,
    DONE: 5,
    ERROR: 6,
  };

  const enc = new TextEncoder();
  const dec = new TextDecoder();
  const encode = (s) => enc.encode(s);
  const decode = (b) => dec.decode(b);

  function indexOf(hay, needle) {
    outer: for (let i = 0; i <= hay.length - needle.length; i++) {
      for (let j = 0; j < needle.length; j++) {
        if (hay[i + j] !== needle[j]) continue outer;
      }
      return i;
    }
    return -1;
  }

  const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

  function withTimeout(promise, ms) {
    return new Promise((resolve, reject) => {
      const t = setTimeout(() => reject(new Error('timeout')), ms);
      promise.then(
        (v) => {
          clearTimeout(t);
          resolve(v);
        },
        (e) => {
          clearTimeout(t);
          reject(e);
        }
      );
    });
  }

  class FramedReader {
    constructor(reader) {
      this.reader = reader;
      this.buf = new Uint8Array(0);
    }

    async pump() {
      const { value, done } = await this.reader.read();
      if (done || !value) throw new Error('serial port closed');
      const merged = new Uint8Array(this.buf.length + value.length);
      merged.set(this.buf, 0);
      merged.set(value, this.buf.length);
      this.buf = merged;
    }

    async readUntil(needle, timeoutMs) {
      const deadline = performance.now() + timeoutMs;
      while (true) {
        const idx = indexOf(this.buf, needle);
        if (idx >= 0) {
          const end = idx + needle.length;
          const out = this.buf.slice(0, end);
          this.buf = this.buf.slice(end);
          return out;
        }
        const errIdx = indexOf(this.buf, encode('ERR '));
        if (errIdx >= 0) {
          const tail = decode(this.buf.slice(errIdx));
          const nl = tail.indexOf('\n');
          if (nl >= 0) throw new Error(tail.slice(0, nl).trim());
        }
        const remaining = deadline - performance.now();
        if (remaining <= 0) {
          throw new Error('timeout waiting for ' + decode(needle));
        }
        await withTimeout(this.pump(), remaining);
      }
    }
  }

  function defaultStatus() {
    return { phase: PHASE.IDLE, progress: 0, status: 'Ready', error: '', busy: false };
  }

  function setStatus(patch) {
    const base = Module._ppTransferStatus || defaultStatus();
    Module._ppTransferStatus = Object.assign(base, patch);
  }

  async function pingOnPort(port) {
    await port.open({ baudRate: 115200 });
    const reader = port.readable.getReader();
    const writer = port.writable.getWriter();
    const framed = new FramedReader(reader);
    try {
      await writer.write(encode('PING\n'));
      const resp = await framed.readUntil(encode('\n'), 2000);
      return decode(resp).trim() === PROTOCOL_VERSION;
    } finally {
      try { reader.releaseLock(); } catch (_) {}
      try { writer.releaseLock(); } catch (_) {}
      try { await port.close(); } catch (_) {}
    }
  }

  async function uploadOnPort(port, slot, image, onProgress) {
    await port.open({ baudRate: 115200 });
    const reader = port.readable.getReader();
    const writer = port.writable.getWriter();
    const framed = new FramedReader(reader);
    try {
      // upload_game.py main(): PING once on the open port, then upload().
      await writer.write(encode('PING\n'));
      const pingResp = await framed.readUntil(encode('\n'), 2000);
      if (decode(pingResp).trim() !== PROTOCOL_VERSION) {
        throw new Error('PING failed');
      }

      await writer.write(encode('UPLOAD\n'));
      await framed.readUntil(encode('Enter Game Slot: '), 2000);
      await writer.write(encode(String(slot) + '\n'));
      const readyOrErr = await framed.readUntil(encode('READY\n'), 10000);
      const line = decode(readyOrErr).trim();
      if (line.startsWith('ERR ')) throw new Error(line);

      const CHUNK = 4096;
      for (let off = 0; off < image.length; off += CHUNK) {
        const slice = image.subarray(off, Math.min(off + CHUNK, image.length));
        await writer.write(slice);
        if (onProgress) onProgress(off + slice.length, image.length);
      }

      const ok = await framed.readUntil(encode('OK\n'), 30000);
      if (decode(ok).trim() !== 'OK') throw new Error('expected OK, got ' + decode(ok));
    } finally {
      try { reader.releaseLock(); } catch (_) {}
      try { writer.releaseLock(); } catch (_) {}
      try { await port.close(); } catch (_) {}
    }
  }

  async function waitForReconnect(timeoutMs) {
    const deadline = performance.now() + timeoutMs;
    while (performance.now() < deadline) {
      const ports = await navigator.serial.getPorts();
      for (const p of ports) {
        const info = p.getInfo();
        if (info.usbVendorId === VID && info.usbProductId === PID) {
          try {
            if (await pingOnPort(p)) return p;
          } catch (_) {}
        }
      }
      await sleep(100);
    }
    throw new Error('device did not come back online within 5 s');
  }

  const state = {
    ports: [],
    labels: [],
    selectedIndex: 0,
    connectedPort: null,
    refreshPromise: null,
    uploadPromise: null,
  };

  function portLabel(port, index) {
    const info = port.getInfo();
    const vid = info.usbVendorId != null ? info.usbVendorId.toString(16) : '????';
    const pid = info.usbProductId != null ? info.usbProductId.toString(16) : '????';
    return 'PicoPanda #' + (index + 1) + ' (' + vid + ':' + pid + ')';
  }

  async function refreshDevicesInternal() {
    setStatus({ phase: PHASE.REFRESHING, busy: true, status: 'Scanning for devices...', error: '' });
    const ports = await navigator.serial.getPorts();
    const filtered = [];
    const labels = [];
    let idx = 0;
    for (const p of ports) {
      const info = p.getInfo();
      if (info.usbVendorId === VID && info.usbProductId === PID) {
        filtered.push(p);
        labels.push(portLabel(p, idx));
        idx++;
      }
    }
    state.ports = filtered;
    state.labels = labels;
    if (state.selectedIndex >= state.ports.length) state.selectedIndex = 0;
    setStatus({
      phase: PHASE.IDLE,
      busy: false,
      status: labels.length ? 'Found ' + labels.length + ' device(s).' : 'No PicoPanda devices found.',
      error: '',
    });
  }

  const PicoPandaWebSerial = {
    isSupported() {
      return 'serial' in navigator;
    },

  getDeviceCount() {
      return state.labels.length;
    },

    getDeviceLabel(index) {
      return state.labels[index] || '';
    },

    selectDevice(index) {
      if (index < 0) index = 0;
      state.selectedIndex = index;
    },

    async refreshDevices() {
      if (state.refreshPromise) return state.refreshPromise;
      state.refreshPromise = refreshDevicesInternal().finally(() => {
        state.refreshPromise = null;
      });
      return state.refreshPromise;
    },

    async requestDevice() {
      if (!this.isSupported()) return false;
      setStatus({ phase: PHASE.REFRESHING, busy: true, status: 'Waiting for device permission...', error: '' });
      try {
        const port = await navigator.serial.requestPort({
          filters: [{ usbVendorId: VID, usbProductId: PID }],
        });
        const ports = await navigator.serial.getPorts();
        if (!ports.includes(port)) {
          // Browser should remember the grant; refresh rebuilds labels.
        }
        await this.refreshDevices();
        return true;
      } catch (err) {
        setStatus({
          phase: PHASE.ERROR,
          busy: false,
          status: 'Device permission denied.',
          error: String(err),
        });
        return false;
      }
    },

    getStatus() {
      return Module._ppTransferStatus || defaultStatus();
    },

    async startUpload(slot, heapPtr, length) {
      if (state.uploadPromise) return false;
      if (!state.ports.length) {
        setStatus({
          phase: PHASE.ERROR,
          busy: false,
          status: 'Upload failed.',
          error: 'No PicoPanda device selected.',
        });
        return false;
      }
      if (length !== SLOT_SIZE) {
        setStatus({
          phase: PHASE.ERROR,
          busy: false,
          status: 'Upload failed.',
          error: 'image must be exactly 131072 bytes',
        });
        return false;
      }

      const image = Module.HEAPU8.slice(heapPtr, heapPtr + length);
      const port = state.ports[state.selectedIndex];
      if (!port) {
        setStatus({
          phase: PHASE.ERROR,
          busy: false,
          status: 'Upload failed.',
          error: 'No PicoPanda device selected.',
        });
        return false;
      }

      state.uploadPromise = (async () => {
        try {
          setStatus({ phase: PHASE.UPLOADING, busy: true, progress: 0, status: 'Uploading...', error: '' });
          await uploadOnPort(port, slot, image, (sent, total) => {
            setStatus({
              phase: PHASE.UPLOADING,
              busy: true,
              progress: sent / total,
              status: 'Sending image... ' + Math.round((sent / total) * 100) + '%',
              error: '',
            });
          });
          setStatus({
            phase: PHASE.RECONNECTING,
            busy: true,
            progress: 1,
            status: 'Device reset — reconnecting...',
            error: '',
          });
          await waitForReconnect(5000);
          await refreshDevicesInternal();
          setStatus({
            phase: PHASE.DONE,
            busy: false,
            progress: 1,
            status: 'Upload complete.',
            error: '',
          });
        } catch (err) {
          setStatus({
            phase: PHASE.ERROR,
            busy: false,
            status: 'Upload failed.',
            error: String(err),
          });
        } finally {
          state.uploadPromise = null;
        }
      })();
      return true;
    },

    poll() {
      // Status is updated directly by async tasks.
    },
  };

  if (typeof Module === 'undefined') {
    window.Module = {};
  }
  Module._ppTransferStatus = defaultStatus();
  window.PicoPandaWebSerial = PicoPandaWebSerial;
  globalThis.PicoPandaWebSerial = PicoPandaWebSerial;
})();
