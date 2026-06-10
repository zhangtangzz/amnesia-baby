// 聊天页面 JS

let currentCharacterId = '';

// 页面加载时获取角色列表
document.addEventListener('DOMContentLoaded', () => {
    loadCharacters();
});

async function loadCharacters() {
    try {
        const data = await apiCall('/characters/list');
        if (data.success && data.data) {
            renderCharacterList(data.data);
        }
    } catch (e) {
        console.error('加载角色失败:', e);
    }
}

function renderCharacterList(characters) {
    const container = document.getElementById('character-list');
    container.innerHTML = '';

    characters.forEach((char, index) => {
        const item = document.createElement('div');
        item.className = 'character-item' + (index === 0 ? ' active' : '');
        item.dataset.id = char.character_id;
        item.onclick = function(e) {
            // 点击按钮时不切换角色
            if (e.target.closest('.char-actions')) return;
            selectCharacter(this);
        };
        item.innerHTML =
            '<span class="char-avatar">' + (char.avatar || '👤') + '</span>' +
            '<span class="char-name">' + escapeHtml(char.name) + '</span>' +
            '<span class="char-actions">' +
                '<button class="char-btn edit-btn" onclick="editCharacter(\'' + char.character_id + '\')" title="编辑">✏️</button>' +
                '<button class="char-btn delete-btn" onclick="deleteCharacter(\'' + char.character_id + '\')" title="删除">🗑️</button>' +
            '</span>';
        container.appendChild(item);
    });

    // 默认选中第一个
    if (characters.length > 0) {
        currentCharacterId = characters[0].character_id;
        document.getElementById('current-character').textContent = characters[0].name;
    }
}

function selectCharacter(element) {
    document.querySelectorAll('.character-item').forEach(el => el.classList.remove('active'));
    element.classList.add('active');
    currentCharacterId = element.dataset.id;
    document.getElementById('current-character').textContent = element.querySelector('.char-name').textContent;

    // 清空聊天区域
    document.getElementById('chat-messages').innerHTML =
        '<div class="message system"><div class="message-content">已切换到 ' +
        escapeHtml(element.querySelector('.char-name').textContent) + '</div></div>';
}

function showCreateForm() {
    document.getElementById('create-form').style.display = 'block';
    document.getElementById('edit-form').style.display = 'none';
}

function hideCreateForm() {
    document.getElementById('create-form').style.display = 'none';
}

async function createCharacter() {
    const id = document.getElementById('new-char-id').value.trim();
    const name = document.getElementById('new-char-name').value.trim();
    const avatar = document.getElementById('new-char-avatar').value.trim() || '👤';
    const desc = document.getElementById('new-char-desc').value.trim();

    if (!id || !name) {
        alert('请输入角色ID和名称');
        return;
    }

    try {
        const data = await apiCall('/characters/create', {
            method: 'POST',
            body: JSON.stringify({
                character_id: id,
                name: name,
                avatar: avatar,
                description: desc,
            }),
        });

        if (data.success) {
            hideCreateForm();
            document.getElementById('new-char-id').value = '';
            document.getElementById('new-char-name').value = '';
            document.getElementById('new-char-avatar').value = '';
            document.getElementById('new-char-desc').value = '';
            loadCharacters(); // 刷新列表
        } else {
            alert(data.message || '创建失败');
        }
    } catch (e) {
        alert('创建失败: ' + e.message);
    }
}

function addMessage(role, content, meta = '') {
    const container = document.getElementById('chat-messages');
    const msg = document.createElement('div');
    msg.className = 'message ' + role;
    let html = '<div class="message-content">' + escapeHtml(content) + '</div>';
    if (meta) html += '<div class="message-meta">' + meta + '</div>';
    msg.innerHTML = html;
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (!message || !currentCharacterId) return;

    const provider = document.getElementById('provider-select').value;
    addMessage('user', message);
    input.value = '';

    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    document.getElementById('chat-status').textContent = '生成中...';

    // 创建空的 assistant 消息容器
    const msgEl = createStreamMessage();
    const contentEl = msgEl.querySelector('.message-content');

    try {
        const params = new URLSearchParams({
            character_id: currentCharacterId,
            message: message,
        });
        if (provider) params.set('provider', provider);

        const response = await fetch(API_BASE + '/chat/stream?' + params.toString());

        if (!response.ok) {
            throw new Error('HTTP ' + response.status);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        let fullReply = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            buffer += decoder.decode(value, { stream: true });

            // 解析 SSE 事件
            const lines = buffer.split('\n');
            buffer = lines.pop(); // 保留不完整的行

            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                const dataStr = line.slice(6).trim();
                if (dataStr === '[DONE]') {
                    // 流结束，移除光标
                    const cursor = contentEl.querySelector('.stream-cursor');
                    if (cursor) cursor.remove();
                    continue;
                }
                try {
                    const data = JSON.parse(dataStr);
                    if (data.type === 'chunk' && data.content) {
                        fullReply += data.content;
                        contentEl.textContent = fullReply;
                        // 自动滚动到底部
                        const container = document.getElementById('chat-messages');
                        container.scrollTop = container.scrollHeight;
                    } else if (data.type === 'done') {
                        // 添加元信息
                        if (data.provider) {
                            const meta = document.createElement('div');
                            meta.className = 'message-meta';
                            meta.textContent = data.provider + (data.model ? ' | ' + data.model : '');
                            msgEl.appendChild(meta);
                        }
                    } else if (data.type === 'error') {
                        contentEl.innerHTML = '<span style="color:var(--error)">错误: ' + escapeHtml(data.message) + '</span>';
                    }
                } catch (e) {
                    // JSON 解析失败，忽略
                }
            }
        }
    } catch (e) {
        // 移除光标后显示错误
        const cursor = contentEl.querySelector('.stream-cursor');
        if (cursor) cursor.remove();
        contentEl.innerHTML = '<span style="color:var(--error)">网络错误: ' + escapeHtml(e.message) + '</span>';
    } finally {
        // 确保光标被移除
        const cursor = contentEl.querySelector('.stream-cursor');
        if (cursor) cursor.remove();
        sendBtn.disabled = false;
        document.getElementById('chat-status').textContent = '就绪';
    }
}

function createStreamMessage() {
    const container = document.getElementById('chat-messages');
    const msg = document.createElement('div');
    msg.className = 'message assistant';
    msg.innerHTML = '<div class="message-content"><span class="stream-cursor">▌</span></div>';
    container.appendChild(msg);
    container.scrollTop = container.scrollHeight;
    return msg;
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// ============ 角色编辑/删除 ============

async function editCharacter(characterId) {
    try {
        const data = await apiCall('/characters/' + characterId);
        if (!data.success) {
            alert('获取角色信息失败: ' + data.message);
            return;
        }

        const char = data.data;
        document.getElementById('edit-char-id').value = char.character_id;
        document.getElementById('edit-char-name').value = char.name || '';
        document.getElementById('edit-char-avatar').value = char.avatar || '';
        document.getElementById('edit-char-desc').value = char.description || '';
        document.getElementById('edit-form').style.display = 'block';
        document.getElementById('create-form').style.display = 'none';
    } catch (e) {
        alert('获取角色信息失败: ' + e.message);
    }
}

function hideEditForm() {
    document.getElementById('edit-form').style.display = 'none';
}

async function saveEditCharacter() {
    const id = document.getElementById('edit-char-id').value;
    const name = document.getElementById('edit-char-name').value.trim();
    const avatar = document.getElementById('edit-char-avatar').value.trim();
    const desc = document.getElementById('edit-char-desc').value.trim();

    if (!name) {
        alert('角色名称不能为空');
        return;
    }

    try {
        const data = await apiCall('/characters/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                name: name,
                avatar: avatar || '👤',
                description: desc,
            }),
        });

        if (data.success) {
            hideEditForm();
            loadCharacters(); // 刷新列表
        } else {
            alert(data.message || '更新失败');
        }
    } catch (e) {
        alert('更新失败: ' + e.message);
    }
}

async function deleteCharacter(characterId) {
    if (!confirm('确定要删除角色 "' + characterId + '" 吗？')) {
        return;
    }

    try {
        const data = await apiCall('/characters/' + characterId, {
            method: 'DELETE',
        });

        if (data.success) {
            loadCharacters(); // 刷新列表
            // 清空聊天区域
            document.getElementById('chat-messages').innerHTML =
                '<div class="message system"><div class="message-content">角色已删除，请选择其他角色</div></div>';
            currentCharacterId = '';
            document.getElementById('current-character').textContent = '请选择角色';
        } else {
            alert(data.message || '删除失败');
        }
    } catch (e) {
        alert('删除失败: ' + e.message);
    }
}
