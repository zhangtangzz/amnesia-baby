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
        item.onclick = function() { selectCharacter(this); };
        item.innerHTML = '<span class="char-avatar">' + (char.avatar || '👤') + '</span>' +
            '<span class="char-name">' + escapeHtml(char.name) + '</span>';
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
    document.getElementById('chat-status').textContent = '思考中...';

    try {
        const data = await apiCall('/chat/send', {
            method: 'POST',
            body: JSON.stringify({
                character_id: currentCharacterId,
                message: message,
                provider: provider || undefined,
            }),
        });

        if (data.success) {
            const meta = data.data.provider + ' | ' + data.data.model;
            addMessage('assistant', data.data.reply, meta);
        } else {
            addMessage('system', '发送失败: ' + (data.error || data.message));
        }
    } catch (e) {
        addMessage('system', '网络错误: ' + e.message);
    } finally {
        sendBtn.disabled = false;
        document.getElementById('chat-status').textContent = '就绪';
    }
}

function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}
