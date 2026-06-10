// 对话历史页面 JS

let selectedHistoryCharId = '';

document.addEventListener('DOMContentLoaded', () => {
    loadHistoryCharacters();
});

async function loadHistoryCharacters() {
    const container = document.getElementById('history-char-list');
    try {
        const data = await apiCall('/memory/list');
        if (!data.success || !data.data.characters || data.data.characters.length === 0) {
            container.innerHTML = '<div class="placeholder">暂无对话记录</div>';
            return;
        }

        container.innerHTML = '';
        data.data.characters.forEach((char, index) => {
            const item = document.createElement('div');
            item.className = 'character-item' + (selectedHistoryCharId === char.character_id ? ' active' : '');
            item.dataset.id = char.character_id;
            item.onclick = function() { selectHistoryCharacter(this); };
            item.innerHTML =
                '<span class="char-avatar">💬</span>' +
                '<span class="char-name">' + escapeHtml(char.character_id) + '</span>' +
                '<span class="char-count">' + char.count + '条</span>';
            container.appendChild(item);
        });

        // 自动选中第一个（如果没有已选中的）
        if (!selectedHistoryCharId && data.data.characters.length > 0) {
            const first = container.querySelector('.character-item');
            if (first) selectHistoryCharacter(first);
        }
    } catch (e) {
        container.innerHTML = '<div class="placeholder" style="color:var(--error)">加载失败: ' + e.message + '</div>';
    }
}

async function selectHistoryCharacter(element) {
    document.querySelectorAll('#history-char-list .character-item').forEach(el => el.classList.remove('active'));
    element.classList.add('active');
    selectedHistoryCharId = element.dataset.id;

    document.getElementById('history-char-name').textContent = '💬 ' + selectedHistoryCharId;
    document.getElementById('clear-btn').style.display = 'inline-block';

    await loadHistory(selectedHistoryCharId);
}

async function loadHistory(characterId) {
    const container = document.getElementById('history-messages');
    const meta = document.getElementById('history-meta');
    container.innerHTML = '<div class="loading"></div> 加载中...';
    meta.textContent = '';

    try {
        const data = await apiCall('/memory/history/' + characterId);
        if (!data.success) {
            container.innerHTML = '<div class="placeholder" style="color:var(--error)">' + escapeHtml(data.message) + '</div>';
            return;
        }

        const history = data.data.history || [];
        if (history.length === 0) {
            container.innerHTML = '<div class="placeholder">该角色暂无对话记录</div>';
            meta.textContent = '';
            return;
        }

        container.innerHTML = '';
        history.forEach(item => {
            const msg = document.createElement('div');
            const content = item.content || '';

            if (content.startsWith('用户:')) {
                msg.className = 'message user';
                msg.innerHTML = '<div class="message-content">' + escapeHtml(content.substring(3).trim()) + '</div>' +
                    '<div class="message-meta">' + formatTime(item.timestamp) + '</div>';
            } else if (content.startsWith('助手:')) {
                msg.className = 'message assistant';
                msg.innerHTML = '<div class="message-content">' + escapeHtml(content.substring(3).trim()) + '</div>' +
                    '<div class="message-meta">' + formatTime(item.timestamp) + '</div>';
            } else {
                msg.className = 'message system';
                msg.innerHTML = '<div class="message-content">' + escapeHtml(content) + '</div>';
            }
            container.appendChild(msg);
        });

        // 滚动到底部
        container.scrollTop = container.scrollHeight;
        meta.textContent = '共 ' + history.length + ' 条记忆';
    } catch (e) {
        container.innerHTML = '<div class="placeholder" style="color:var(--error)">加载失败: ' + e.message + '</div>';
    }
}

async function clearHistory() {
    if (!selectedHistoryCharId) return;
    if (!confirm('确定要清空角色 "' + selectedHistoryCharId + '" 的所有对话历史吗？')) return;

    try {
        const data = await apiCall('/memory/' + selectedHistoryCharId, { method: 'DELETE' });
        if (data.success) {
            document.getElementById('history-messages').innerHTML =
                '<div class="placeholder">已清空 ' + (data.data.removed_count || 0) + ' 条记忆</div>';
            document.getElementById('history-meta').textContent = '';
            loadHistoryCharacters(); // 刷新列表
        } else {
            alert(data.message || '清空失败');
        }
    } catch (e) {
        alert('清空失败: ' + e.message);
    }
}

function formatTime(timestamp) {
    if (!timestamp) return '';
    try {
        const d = new Date(timestamp);
        return d.toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' });
    } catch (e) {
        return timestamp;
    }
}

