const BASE = 'http://127.0.0.1:5000';

function switchTab(name) {
    const tabs = ['submit', 'appeal', 'log'];
    document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', tabs[i] === name));
    document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
    document.getElementById('tab-' + name).classList.add('active');
}

function badgeFor(attr) {
    if (attr === 'likely_ai') return '<span class="badge badge-ai">likely AI</span>';
    if (attr === 'likely_human') return '<span class="badge badge-human">likely human</span>';
    return '<span class="badge badge-uncertain">uncertain</span>';
}

async function doSubmit() {
    const text = document.getElementById('sub-text').value.trim();
    const creator = document.getElementById('sub-creator').value.trim() || 'anonymous';
    const status = document.getElementById('sub-status');
    const result = document.getElementById('sub-result');
    if (!text) { status.innerHTML = '<p class="status-error">Enter some text first.</p>'; return; }
    status.innerHTML = '<p class="status-loading">Analyzing… this may take a few seconds.</p>';
    result.classList.remove('show');
    try {
        const res = await fetch(BASE + '/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, creator_id: creator })
        });
        const data = await res.json();
        if (!res.ok) { status.innerHTML = '<p class="status-error">Error: ' + (data.error || res.status) + '</p>'; return; }
        status.innerHTML = '';
        document.getElementById('r-attr').innerHTML = data.attribution + badgeFor(data.attribution);
        document.getElementById('r-conf').textContent = (data.confidence * 100).toFixed(1) + '%';
        document.getElementById('r-llm').textContent = (data.llm_score * 100).toFixed(1) + '%';
        document.getElementById('r-stylo').textContent = (data.stylometric_score * 100).toFixed(1) + '%';
        document.getElementById('r-cid').textContent = data.content_id;
        document.getElementById('r-label').textContent = data.label;
        result.classList.add('show');
        document.getElementById('app-cid').value = data.content_id;
    } catch (e) {
        status.innerHTML = '<p class="status-error">Could not reach server. Is app.py running?</p>';
    }
}

async function doAppeal() {
    const cid = document.getElementById('app-cid').value.trim();
    const reason = document.getElementById('app-reason').value.trim();
    const status = document.getElementById('app-status');
    const result = document.getElementById('app-result');
    if (!cid || !reason) { status.innerHTML = '<p class="status-error">Fill in both fields.</p>'; return; }
    status.innerHTML = '<p class="status-loading">Submitting appeal…</p>';
    result.classList.remove('show');
    try {
        const res = await fetch(BASE + '/appeal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content_id: cid, creator_reasoning: reason })
        });
        const data = await res.json();
        if (!res.ok) { status.innerHTML = '<p class="status-error">Error: ' + (data.error || res.status) + '</p>'; return; }
        status.innerHTML = '';
        document.getElementById('a-status').textContent = data.status;
        document.getElementById('a-msg').textContent = data.message;
        result.classList.add('show');
    } catch (e) {
        status.innerHTML = '<p class="status-error">Could not reach server. Is app.py running?</p>';
    }
}

async function doLog() {
    const status = document.getElementById('log-status');
    const result = document.getElementById('log-result');
    status.innerHTML = '<p class="status-loading">Fetching log…</p>';
    result.innerHTML = '';
    try {
        const res = await fetch(BASE + '/log');
        const data = await res.json();
        status.innerHTML = '';
        if (!data.entries || data.entries.length === 0) {
            result.innerHTML = '<p style="color:#999;font-size:13px;">No entries yet — submit something first.</p>';
            return;
        }
        result.innerHTML = data.entries.slice().reverse().map(e => `
          <div class="log-entry">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
              <span style="font-size:13px;font-weight:500;">${e.attribution}${badgeFor(e.attribution)}</span>
              <span style="font-size:12px;color:#999;">${e.status}</span>
            </div>
            <p class="attr">Confidence: <span>${(e.confidence * 100).toFixed(1)}%</span> &nbsp;|&nbsp; LLM: <span>${(e.llm_score * 100).toFixed(1)}%</span> &nbsp;|&nbsp; Stylo: <span>${(e.stylometric_score * 100).toFixed(1)}%</span></p>
            ${e.appeal_reasoning ? `<p class="attr" style="margin-top:6px;">Appeal: <span>${e.appeal_reasoning}</span></p>` : ''}
            <p class="cid" style="margin-top:6px;">${e.content_id}</p>
            <p style="font-size:11px;color:#bbb;margin-top:4px;">${e.timestamp}</p>
          </div>
        `).join('');
    } catch (e) {
        status.innerHTML = '<p class="status-error">Could not reach server. Is app.py running?</p>';
    }
}