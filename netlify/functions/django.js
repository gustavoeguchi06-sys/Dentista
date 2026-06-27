const { spawn } = require('child_process');
const http = require('http');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..', '..');
const host = process.env.DJANGO_HOST || '127.0.0.1';
const port = Number(process.env.DJANGO_PORT || 8001);

let djangoProcess = null;
let djangoReadyPromise = null;

function getPythonCommand() {
  if (process.env.VIRTUAL_ENV) {
    const executable = process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python';
    return path.join(process.env.VIRTUAL_ENV, executable);
  }

  return process.platform === 'win32' ? 'python' : 'python3';
}

function startDjangoIfNeeded() {
  if (djangoProcess && !djangoProcess.killed) {
    return djangoReadyPromise;
  }

  djangoReadyPromise = new Promise((resolve, reject) => {
    const env = {
      ...process.env,
      PYTHONPATH: projectRoot,
      DJANGO_SETTINGS_MODULE: 'mxodontologia.settings',
      PORT: String(port),
    };

    const pythonCommand = getPythonCommand();
    const child = spawn(
      pythonCommand,
      ['-m', 'waitress', '--listen', `${host}:${port}`, 'mxodontologia.wsgi:application'],
      {
        cwd: projectRoot,
        env,
        stdio: ['ignore', 'pipe', 'pipe'],
      }
    );

    djangoProcess = child;

    let settled = false;
    let output = '';

    const finish = (callback, value) => {
      if (settled) return;
      settled = true;
      callback(value);
    };

    const onData = (chunk) => {
      output += chunk.toString();
      if (output.includes('Listening at:') || output.includes('Booting') || output.includes('Worker exiting')) {
        finish(resolve, true);
      }
    };

    child.stdout.on('data', onData);
    child.stderr.on('data', onData);

    child.once('exit', (code, signal) => {
      if (!settled) {
        finish(reject, new Error(`Django process exited early (code=${code}, signal=${signal}). Output: ${output}`));
      }
    });

    setTimeout(() => {
      if (!settled) {
        finish(resolve, true);
      }
    }, 15000);
  });

  return djangoReadyPromise;
}

function proxyToDjango(event) {
  return new Promise((resolve, reject) => {
    const method = event.httpMethod || 'GET';
    const rawPath = event.path || '/';
    const query = event.rawQuery || '';
    const targetPath = query ? `${rawPath}?${query}` : rawPath;

    const headers = { ...(event.headers || {}) };
    if (!headers.host) {
      headers.host = `${host}:${port}`;
    }

    const body = event.body ? (event.isBase64Encoded ? Buffer.from(event.body, 'base64') : Buffer.from(event.body)) : undefined;

    const req = http.request(
      {
        hostname: host,
        port,
        path: targetPath,
        method,
        headers,
      },
      (res) => {
        const chunks = [];
        res.on('data', (chunk) => chunks.push(Buffer.from(chunk)));
        res.on('end', () => {
          const responseBody = Buffer.concat(chunks).toString('utf8');
          const responseHeaders = { ...(res.headers || {}) };
          delete responseHeaders['transfer-encoding'];
          delete responseHeaders['content-length'];
          if (!responseHeaders['content-type']) {
            responseHeaders['content-type'] = 'text/plain; charset=utf-8';
          }

          resolve({
            statusCode: res.statusCode || 502,
            headers: responseHeaders,
            body: responseBody,
          });
        });
      }
    );

    req.on('error', reject);

    if (body && body.length) {
      req.write(body);
    }

    req.end();
  });
}

exports.handler = async function handler(event) {
  try {
    await startDjangoIfNeeded();
    return await proxyToDjango(event);
  } catch (error) {
    return {
      statusCode: 500,
      headers: { 'content-type': 'text/plain; charset=utf-8' },
      body: `Django Netlify adapter failed: ${error.message}`,
    };
  }
};

