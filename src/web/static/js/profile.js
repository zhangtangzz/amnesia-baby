// 角色画像页面 JS

async function loadProfile() {
    const characterId = document.getElementById('p-character-id').value.trim();
    if (!characterId) return;

    try {
        const data = await apiCall('/personality/profile/' + characterId);
        if (data.success) {
            renderPersonality(data.data.personality);
            renderBigFive(data.data.big_five);
            renderEnneagram(data.data.enneagram);
        }
    } catch (e) {
        console.error('加载画像失败:', e);
    }
}

async function analyzePersonality() {
    const text = document.getElementById('p-text').value.trim();
    if (!text) return;

    try {
        const data = await apiCall('/personality/analyze', {
            method: 'POST',
            body: JSON.stringify({ text: text }),
        });
        if (data.success && data.data) {
            if (data.data.personality) renderPersonality(data.data.personality);
            if (data.data.big_five) renderBigFive(data.data.big_five);
        }
    } catch (e) {
        console.error('分析失败:', e);
    }
}

function renderPersonality(personality) {
    if (!personality) return;
    const container = document.getElementById('personality-traits');
    const traits = [
        { key: 'achievement_drive', label: '成就驱动' },
        { key: 'curiosity', label: '好奇心' },
        { key: 'risk_preference', label: '风险偏好' },
        { key: 'empathy', label: '共情能力' },
        { key: 'dominance', label: '支配性' },
    ];

    let html = '';
    traits.forEach(t => {
        const val = personality[t.key] || 0;
        const pct = Math.round(val * 100);
        html += '<div class="trait-item">' +
            '<div class="trait-label">' + t.label + '</div>' +
            '<div class="trait-bar"><div class="trait-fill" style="width:' + pct + '%"></div></div>' +
            '<div class="trait-value">' + val.toFixed(2) + '</div>' +
            '</div>';
    });
    container.innerHTML = html;
}

function renderBigFive(bigFive) {
    if (!bigFive) return;
    const container = document.getElementById('big-five-chart');
    const dims = [
        { key: 'openness', label: '开放性' },
        { key: 'conscientiousness', label: '尽责性' },
        { key: 'extraversion', label: '外向性' },
        { key: 'agreeableness', label: '宜人性' },
        { key: 'neuroticism', label: '神经质' },
    ];

    let html = '<div class="traits-grid">';
    dims.forEach(d => {
        const val = bigFive[d.key] || 0;
        const pct = Math.round(val * 100);
        html += '<div class="trait-item">' +
            '<div class="trait-label">' + d.label + '</div>' +
            '<div class="trait-bar"><div class="trait-fill" style="width:' + pct + '%"></div></div>' +
            '<div class="trait-value">' + val.toFixed(2) + '</div>' +
            '</div>';
    });
    html += '</div>';
    container.innerHTML = html;
}

function renderEnneagram(enneagram) {
    if (!enneagram) return;
    const container = document.getElementById('enneagram-chart');
    const types = [
        { key: 'type_1', label: '1-完美主义者' },
        { key: 'type_2', label: '2-助人者' },
        { key: 'type_3', label: '3-成就者' },
        { key: 'type_4', label: '4-个人主义者' },
        { key: 'type_5', label: '5-观察者' },
        { key: 'type_6', label: '6-忠诚者' },
        { key: 'type_7', label: '7-享乐主义者' },
        { key: 'type_8', label: '8-挑战者' },
        { key: 'type_9', label: '9-和平者' },
    ];

    let html = '<div class="traits-grid">';
    types.forEach(t => {
        const val = enneagram[t.key] || 0;
        const pct = Math.round(val * 100);
        html += '<div class="trait-item">' +
            '<div class="trait-label">' + t.label + '</div>' +
            '<div class="trait-bar"><div class="trait-fill" style="width:' + pct + '%"></div></div>' +
            '<div class="trait-value">' + val.toFixed(2) + '</div>' +
            '</div>';
    });
    html += '</div>';
    container.innerHTML = html;
}

// 页面加载时自动加载默认角色画像
document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
});
