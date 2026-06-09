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
