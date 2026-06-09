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
