// 聊天页面 JS

let currentCharacterId = 'elon';

function selectCharacter(element) {
    document.querySelectorAll('.character-item').forEach(el => el.classList.remove('active'));
    element.classList.add('active');
    currentCharacterId = element.dataset.id;
    document.getElementById('current-character').textContent = element.querySelector('.char-name').textContent;
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
    if (!message) return;

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
