var EMOTION_COLORS = {
    'Angry':'#E040A0','Disgust':'#00CC44','Fear':'#8B5CF6',
    'Happy':'#7B3FF2','Sad':'#06B6D4','Surprise':'#F59E0B',
    'Neutral':'#9B7EC8'
};
var STRESS_EMOTIONS   = ['Angry','Fear','Disgust','Sad'];
var POSITIVE_EMOTIONS = ['Happy','Surprise'];

var photoFile     = null;
var videoStream   = null;
var videoInterval = null;
var videoHistory  = [];

function showPage(name, btn) {
    document.querySelectorAll('.page')
        .forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.sb-btn')
        .forEach(b => b.classList.remove('active'));
    document.getElementById('page-' + name).classList.add('active');
    btn.classList.add('active');
    document.getElementById('tb-sub').textContent =
        '→ ' + btn.textContent.trim();
    if (name === 'history') loadHistory();
}

function handleDrop(e, ctx) {
    e.preventDefault();
    var file = e.dataTransfer.files[0];
    if (!file) return;
    if (ctx === 'dash') {
        var inp = document.getElementById('dash-file');
        var dt  = new DataTransfer();
        dt.items.add(file);
        inp.files = dt.files;
        analyzeFile(inp, 'dash');
    } else {
        var inp = document.getElementById('photo-file');
        var dt  = new DataTransfer();
        dt.items.add(file);
        inp.files = dt.files;
        analyzeFile(inp, 'photo');
    }
}

function analyzeFile(input, ctx) {
    var file = input.files[0];
    if (!file) return;

    if (ctx === 'dash') {
        var fd = new FormData();
        fd.append('photo', file);
        fetch('/analyze', {method:'POST', body:fd})
        .then(r => r.json())
        .then(data => {
            if (data.error) { alert(data.error); return; }
            updateDashboard(data);
        });
    } else {
        photoFile = file;
        var reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('photo-preview-img').src = e.target.result;
            document.getElementById('photo-preview').style.display = 'block';
            document.getElementById('photo-btn').style.display = 'flex';
        };
        reader.readAsDataURL(file);
    }
}

function submitPhoto() {
    if (!photoFile) return;
    var fd = new FormData();
    fd.append('photo', photoFile);
    document.getElementById('photo-btn').textContent = 'Analyzing...';
    fetch('/analyze', {method:'POST', body:fd})
    .then(r => r.json())
    .then(data => {
        document.getElementById('photo-btn').innerHTML =
            '<i class="ti ti-brain"></i> Analyze Emotion';
        if (data.error) { alert(data.error); return; }
        updatePhotoResult(data);
    });
}

function updateDashboard(data) {
    document.getElementById('m-wellness').textContent  = data.wellness + '%';
    document.getElementById('m-stress').textContent    = data.stress + '%';
    document.getElementById('m-positive').textContent  = data.positive + '%';
    document.getElementById('m-dominant').textContent  = data.dominant_emoji;

    document.getElementById('dash-emotion-card').innerHTML =
        '<div class="emotion-icon">' + data.emoji + '</div>' +
        '<div class="emotion-name" style="color:' + data.color + '">' +
            data.emotion.toUpperCase() + '</div>' +
        '<div class="emotion-conf">Confidence: ' + data.conf + '%</div>';

    document.getElementById('dash-result-img').style.display = 'block';
    document.getElementById('dash-img').src =
        'data:image/jpeg;base64,' + data.result_img;

    document.getElementById('dash-bars').style.display = 'block';
    renderBars('dash-bar-rows', data.probs, data.colors);
    renderTips('dash-tips', data.tips);
}

function updatePhotoResult(data) {
    document.getElementById('photo-emotion-card').innerHTML =
        '<div class="emotion-icon">' + data.emoji + '</div>' +
        '<div class="emotion-name" style="color:' + data.color + '">' +
            data.emotion.toUpperCase() + '</div>' +
        '<div class="emotion-conf">Confidence: ' + data.conf + '%</div>';

    document.getElementById('photo-result-img').style.display = 'block';
    document.getElementById('photo-overlay').src =
        'data:image/jpeg;base64,' + data.result_img;

    renderBars('photo-bar-rows', data.probs, data.colors);
    renderTips('photo-tips', data.tips);
}

function renderBars(containerId, probs, colors) {
    var sorted = Object.entries(probs)
        .sort((a,b) => b[1] - a[1]);
    var html = '';
    sorted.forEach(function(entry) {
        var e   = entry[0];
        var pct = entry[1];
        var c   = colors[e] || '#7B3FF2';
        html += '<div class="bar-row">' +
            '<span class="bar-label">' + e + '</span>' +
            '<div class="bar-track">' +
                '<div class="bar-fill" style="width:' + pct + '%;' +
                    'background:' + c + '"></div>' +
            '</div>' +
            '<span class="bar-pct">' + pct + '%</span>' +
            '</div>';
    });
    document.getElementById(containerId).innerHTML = html;
}

function renderTips(containerId, tips) {
    var html = '';
    tips.forEach(function(tip) {
        html += '<div class="tip">' + tip + '</div>';
    });
    document.getElementById(containerId).innerHTML = html ||
        '<div class="tip">No tips available.</div>';
}

function loadHistory() {
    fetch('/history')
    .then(r => r.json())
    .then(function(hist) {
        if (hist.length === 0) {
            document.getElementById('history-summary').style.display = 'none';
            document.getElementById('history-list').innerHTML =
                '<div class="empty-state">' +
                '<i class="ti ti-clipboard-list" style="font-size:2.5rem;' +
                'display:block;margin-bottom:8px;color:#C4AAFE"></i>' +
                'No history yet — analyze some photos first</div>';
            return;
        }
        document.getElementById('history-summary').style.display = 'grid';
        var total   = hist.length;
        var happy   = hist.filter(h => POSITIVE_EMOTIONS.includes(h.emotion)).length;
        var stress  = hist.filter(h => STRESS_EMOTIONS.includes(h.emotion)).length;
        var counts  = {};
        hist.forEach(h => counts[h.emotion] = (counts[h.emotion]||0)+1);
        var dominant = Object.keys(counts)
            .reduce((a,b) => counts[a]>counts[b]?a:b);

        document.getElementById('h-total').textContent    = total;
        document.getElementById('h-happy').textContent    = happy;
        document.getElementById('h-stress').textContent   = stress;
        document.getElementById('h-dominant').textContent = dominant;

        var html = '';
        hist.slice().reverse().forEach(function(h, i) {
            html += '<div class="hist-row">' +
                '<div class="hist-num">#' + (total-i) + '</div>' +
                '<div class="hist-time">' + h.time + '</div>' +
                '<div class="hist-emoji">' + h.emoji + '</div>' +
                '<div class="hist-emotion" style="color:' + h.color + '">' +
                    h.emotion + '</div>' +
                '<div class="hist-conf">' + h.conf + '%</div>' +
                '</div>';
        });
        document.getElementById('history-list').innerHTML = html;
    });
}

function clearHistory() {
    fetch('/clear_history', {method:'POST'})
    .then(() => loadHistory());
}

function startVideo() {
    if (videoStream) return;
    navigator.mediaDevices.getUserMedia({video:true})
    .then(function(stream) {
        videoStream = stream;
        document.getElementById('video-area').style.display = 'none';
        var canvas = document.getElementById('video-canvas');
        canvas.style.display = 'block';

        var video = document.createElement('video');
        video.srcObject  = stream;
        video.autoplay   = true;
        video.playsinline = true;

        video.onloadedmetadata = function() {
            canvas.width  = video.videoWidth;
            canvas.height = video.videoHeight;
            var ctx = canvas.getContext('2d');

            videoInterval = setInterval(function() {
                ctx.drawImage(video, 0, 0);
                canvas.toBlob(function(blob) {
                    var fd = new FormData();
                    fd.append('photo', blob, 'frame.jpg');
                    fetch('/analyze', {method:'POST', body:fd})
                    .then(r => r.json())
                    .then(function(data) {
                        if (data.error) return;
                        videoHistory.push(data.emotion);

                        document.getElementById('video-emoji').textContent =
                            data.emoji;
                        document.getElementById('video-emotion-name').textContent =
                            data.emotion.toUpperCase();
                        document.getElementById('video-emotion-name').style.color =
                            data.color;
                        document.getElementById('video-conf').textContent =
                            'Confidence: ' + data.conf + '%';

                        document.getElementById('v-detections').textContent =
                            videoHistory.length;
                        document.getElementById('v-wellness').textContent =
                            data.wellness + '%';
                        document.getElementById('v-stress').textContent =
                            data.stress + '%';

                        renderTips('video-tips', data.tips);

                        ctx.drawImage(video, 0, 0);
                        ctx.strokeStyle = '#7B3FF2';
                        ctx.lineWidth   = 2;
                        ctx.fillStyle   = '#7B3FF2';
                        ctx.font        = 'bold 14px Inter';
                        ctx.fillText(
                            data.emotion + ' ' + data.conf.toFixed(0) + '%',
                            12, 30);
                    });
                }, 'image/jpeg', 0.8);
            }, 1500);
        };
    })
    .catch(function() {
        alert('Cannot access camera. Please allow camera permissions.');
    });
}

function stopVideo() {
    if (videoInterval) { clearInterval(videoInterval); videoInterval = null; }
    if (videoStream)   {
        videoStream.getTracks().forEach(t => t.stop());
        videoStream = null;
    }
    document.getElementById('video-canvas').style.display = 'none';
    document.getElementById('video-area').style.display   = 'block';
    document.getElementById('video-emoji').textContent    = '🎥';
    document.getElementById('video-emotion-name').textContent = 'STOPPED';
    document.getElementById('video-emotion-name').style.color = '#6B4F8E';
    document.getElementById('video-conf').textContent =
        'Press Start to begin again';
    videoHistory = [];
}