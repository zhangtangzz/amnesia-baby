// 知识库页面 JS

async function processKnowledge(event) {
    event.preventDefault();
    const characterId = document.getElementById('k-character-id').value.trim();
    const source = document.getElementById('k-source').value.trim();
    const text = document.getElementById('k-text').value.trim();

    if (!text) {
        showError('process-result', '请输入素材内容');
        return;
    }

    showLoading('process-result');
    document.getElementById('process-result').style.display = 'block';

    try {
        const data = await apiCall('/knowledge/process', {
            method: 'POST',
            body: JSON.stringify({
                text: text,
                source: source || 'user_input',
                character_id: characterId || null,
            }),
        });

        const el = document.getElementById('process-result');
        if (data.success) {
            el.innerHTML = '<strong>处理成功!</strong>\n\n' + formatJSON(data.data);
        } else {
            el.innerHTML = '<span style="color:var(--error)">处理失败: ' + (data.error || data.message) + '</span>';
        }
    } catch (e) {
        showError('process-result', e.message);
    }
}

async function uploadKnowledgeFile(event) {
    event.preventDefault();
    const characterId = document.getElementById('f-character-id').value.trim();
    const fileInput = document.getElementById('k-file');
    const file = fileInput.files[0];

    if (!file) {
        showError('process-result', '请选择一个文件');
        return;
    }

    // 检查文件大小 (5MB)
    if (file.size > 5 * 1024 * 1024) {
        showError('process-result', '文件过大，最大支持 5MB');
        return;
    }

    // 检查文件类型
    const allowedExts = ['.txt', '.md', '.csv'];
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!allowedExts.includes(ext)) {
        showError('process-result', '不支持的文件格式，仅支持 ' + allowedExts.join(', '));
        return;
    }

    showLoading('process-result');
    document.getElementById('process-result').style.display = 'block';

    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('source', file.name);
        if (characterId) {
            formData.append('character_id', characterId);
        }

        const response = await fetch(API_BASE + '/knowledge/upload', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();

        const el = document.getElementById('process-result');
        if (data.success) {
            el.innerHTML = '<strong>文件上传处理成功!</strong>\n' +
                '<div style="margin: 8px 0; font-size: 0.9em; color: var(--text-secondary);">' +
                '文件: ' + (data.data.filename || '') + ' | 大小: ' + formatFileSize(data.data.file_size || 0) +
                '</div>\n' + formatJSON(data.data);
        } else {
            el.innerHTML = '<span style="color:var(--error)">处理失败: ' + (data.error || data.message) + '</span>';
        }
    } catch (e) {
        showError('process-result', e.message);
    }
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

async function queryKnowledge() {
    const characterId = document.getElementById('q-character-id').value.trim();
    if (!characterId) {
        showError('knowledge-result', '请输入角色ID');
        return;
    }

    showLoading('knowledge-result');
    document.getElementById('knowledge-result').style.display = 'block';

    try {
        const data = await apiCall('/knowledge/base/' + characterId);

        const el = document.getElementById('knowledge-result');
        if (data.success) {
            el.innerHTML = '<strong>查询成功!</strong>\n\n' + formatJSON(data.data);
        } else {
            el.innerHTML = '<span style="color:var(--error)">查询失败: ' + (data.error || data.message) + '</span>';
        }
    } catch (e) {
        showError('knowledge-result', e.message);
    }
}

// ============ 知识库管理 ============

let selectedKBCharId = '';

document.addEventListener('DOMContentLoaded', () => {
    loadKnowledgeBases();
});

async function loadKnowledgeBases() {
    const container = document.getElementById('kb-list');
    try {
        const data = await apiCall('/knowledge/list');
        if (!data.success || !data.data.bases || data.data.bases.length === 0) {
            container.innerHTML = '<div class="placeholder">暂无知识库，请先上传素材</div>';
            return;
        }

        container.innerHTML = '';
        data.data.bases.forEach(base => {
            const item = document.createElement('div');
            item.className = 'kb-item' + (selectedKBCharId === base.character_id ? ' active' : '');
            item.onclick = function() { selectKB(this); };
            item.dataset.id = base.character_id;

            const name = (base.profile && base.profile.name) || base.character_id;
            item.innerHTML =
                '<div class="kb-item-main">' +
                    '<span class="kb-item-name">' + escapeHtml(name) + '</span>' +
                    '<span class="kb-item-id">' + escapeHtml(base.character_id) + '</span>' +
                '</div>' +
                '<div class="kb-item-stats">' +
                    '<span title="事实">📝 ' + base.facts_count + '</span>' +
                    '<span title="证据">📎 ' + base.evidence_count + '</span>' +
                    '<span title="关系">🤝 ' + base.relationships_count + '</span>' +
                '</div>';
            container.appendChild(item);
        });
    } catch (e) {
        container.innerHTML = '<div class="placeholder" style="color:var(--error)">加载失败: ' + e.message + '</div>';
    }
}

function selectKB(element) {
    document.querySelectorAll('.kb-item').forEach(el => el.classList.remove('active'));
    element.classList.add('active');
    selectedKBCharId = element.dataset.id;
    loadKBDetail(selectedKBCharId);
}

async function loadKBDetail(characterId) {
    const panel = document.getElementById('kb-detail-panel');
    const content = document.getElementById('kb-detail-content');
    const title = document.getElementById('kb-detail-title');

    panel.style.display = 'block';
    title.textContent = '📚 ' + characterId + ' 知识库详情';
    content.innerHTML = '<div class="loading"></div> 加载中...';

    try {
        const data = await apiCall('/knowledge/detail/' + characterId);
        if (!data.success) {
            content.innerHTML = '<div class="placeholder" style="color:var(--error)">' + escapeHtml(data.message) + '</div>';
            return;
        }

        const d = data.data;
        let html = '';

        // 基础信息
        if (d.profile) {
            html += '<div class="kb-section"><h4>👤 基础信息</h4><div class="kb-kv">';
            for (const [k, v] of Object.entries(d.profile)) {
                if (v && v !== '' && (!Array.isArray(v) || v.length > 0)) {
                    html += '<div class="kb-kv-row"><span class="kb-kv-key">' + escapeHtml(k) + '</span><span class="kb-kv-val">' + escapeHtml(Array.isArray(v) ? v.join(', ') : String(v)) + '</span></div>';
                }
            }
            html += '</div></div>';
        }

        // 事实
        if (d.facts && d.facts.length > 0) {
            html += '<div class="kb-section"><h4>📝 事实 (' + d.facts.length + ')</h4><div class="kb-list-items">';
            d.facts.forEach(f => {
                html += '<div class="kb-list-item"><span class="kb-item-text">' + escapeHtml(f.fact) + '</span>' +
                    '<span class="kb-item-badge">' + escapeHtml(f.category) + '</span>' +
                    '<span class="kb-item-conf">' + Math.round(f.confidence * 100) + '%</span></div>';
            });
            html += '</div></div>';
        }

        // 证据
        if (d.evidence && d.evidence.length > 0) {
            html += '<div class="kb-section"><h4>📎 证据 (' + d.evidence.length + ')</h4><div class="kb-list-items">';
            d.evidence.forEach(e => {
                html += '<div class="kb-list-item"><span class="kb-item-text">' + escapeHtml(e.content) + '</span>' +
                    '<span class="kb-item-badge">' + escapeHtml(e.source_name) + '</span></div>';
            });
            html += '</div></div>';
        }

        // 关系
        if (d.relationships && d.relationships.length > 0) {
            html += '<div class="kb-section"><h4>🤝 人物关系 (' + d.relationships.length + ')</h4><div class="kb-list-items">';
            d.relationships.forEach(r => {
                html += '<div class="kb-list-item"><span class="kb-item-text">' + escapeHtml(r.name) + ' - ' + escapeHtml(r.relationship) + '</span></div>';
            });
            html += '</div></div>';
        }

        content.innerHTML = html || '<div class="placeholder">知识库为空</div>';
    } catch (e) {
        content.innerHTML = '<div class="placeholder" style="color:var(--error)">加载失败: ' + e.message + '</div>';
    }
}

function closeDetail() {
    document.getElementById('kb-detail-panel').style.display = 'none';
    document.querySelectorAll('.kb-item').forEach(el => el.classList.remove('active'));
    selectedKBCharId = '';
}

async function deleteKnowledgeBase() {
    if (!selectedKBCharId) return;
    if (!confirm('确定要删除知识库 "' + selectedKBCharId + '" 吗？此操作不可恢复。')) return;

    try {
        const data = await apiCall('/knowledge/' + selectedKBCharId, { method: 'DELETE' });
        if (data.success) {
            closeDetail();
            loadKnowledgeBases();
        } else {
            alert(data.message || '删除失败');
        }
    } catch (e) {
        alert('删除失败: ' + e.message);
    }
}

