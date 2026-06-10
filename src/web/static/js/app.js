// 失忆宝宝 - 全局 JS

const API_BASE = '/api';

async function apiCall(url, options = {}) {
    const defaultOptions = {
        headers: { 'Content-Type': 'application/json' },
    };
    const response = await fetch(API_BASE + url, { ...defaultOptions, ...options });
    return response.json();
}

function showLoading(elementId) {
    const el = document.getElementById(elementId);
    if (el) el.innerHTML = '<div class="loading"></div> 处理中...';
}

function showError(elementId, message) {
    const el = document.getElementById(elementId);
    if (el) {
        el.style.display = 'block';
        el.innerHTML = '<span style="color:var(--error)">错误: ' + message + '</span>';
    }
}

function formatJSON(obj) {
    return JSON.stringify(obj, null, 2);
}

function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = String(text);
    return div.innerHTML;
}
