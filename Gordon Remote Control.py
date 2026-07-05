"""
Gordon Remote Control - النسخة المبسطة والموثوقة
Author: Gordon Team
Version: 7.0 (Standalone)
"""

import os
import socket
import threading
import base64
import io
import time
from datetime import datetime

from flask import Flask, render_template_string, request, jsonify
import pyautogui
import psutil
import mss
from PIL import Image

# ===================== الإعدادات =====================
PASSWORD = "gordon123"
PORT = 5000
QUALITY = 60
SCALE = 0.4

# ===================== السجلات =====================
logs = []

def add_log(msg):
    logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
    if len(logs) > 50:
        logs.pop(0)

add_log("🚀 Gordon v7 جاهز")

# ===================== المصادقة =====================
sessions = {}

def is_auth(ip):
    return sessions.get(ip, False)

# ===================== دوال التحكم =====================
def move_mouse(x, y):
    try:
        pyautogui.moveTo(x, y, duration=0)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def click_mouse(btn="left"):
    try:
        pyautogui.click(button=btn)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def drag_mouse(x1, y1, x2, y2):
    try:
        pyautogui.moveTo(x1, y1, duration=0.05)
        pyautogui.drag(x2 - x1, y2 - y1, duration=0.2)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def scroll_mouse(direction, amount=3, x=None, y=None):
    try:
        if x is not None and y is not None:
            pyautogui.moveTo(x, y, duration=0)
        pyautogui.scroll(amount if direction == "up" else -amount)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def type_text(text):
    try:
        pyautogui.typewrite(text, interval=0.03)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def press_key(key):
    try:
        pyautogui.press(key)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def hotkey(keys):
    try:
        pyautogui.hotkey(*keys)
        return {"success": True}
    except Exception as e:
        return {"error": str(e)}

def capture_screen():
    try:
        sct = mss.mss()
        monitor = sct.monitors[1]
        img = sct.grab(monitor)
        image = Image.frombytes("RGB", img.size, img.rgb)
        if SCALE != 1.0:
            new_size = (int(image.width * SCALE), int(image.height * SCALE))
            image = image.resize(new_size, Image.Resampling.LANCZOS)
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=QUALITY)
        b64 = base64.b64encode(buffer.getvalue()).decode()
        return {"success": True, "image": b64, "width": image.width, "height": image.height}
    except Exception as e:
        return {"error": str(e)}

def get_system_info():
    try:
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        return {"success": True, "cpu": cpu, "memory": mem.percent, "disk": disk.percent}
    except Exception as e:
        return {"error": str(e)}

# ===================== خادم Flask =====================
app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/auth", methods=["POST"])
def auth():
    data = request.json
    ip = request.remote_addr
    pwd = data.get("password", "")
    if pwd == PASSWORD:
        sessions[ip] = True
        add_log(f"✅ دخول من {ip}")
        return jsonify({"success": True})
    add_log(f"❌ فشل دخول من {ip}")
    return jsonify({"success": False, "message": "كلمة مرور خاطئة"})

@app.route("/api/mouse/move", methods=["POST"])
def api_move():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    data = request.json
    return jsonify(move_mouse(data["x"], data["y"]))

@app.route("/api/mouse/click", methods=["POST"])
def api_click():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    data = request.json
    return jsonify(click_mouse(data.get("button", "left")))

@app.route("/api/mouse/drag", methods=["POST"])
def api_drag():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    data = request.json
    return jsonify(drag_mouse(data["x1"], data["y1"], data["x2"], data["y2"]))

@app.route("/api/mouse/scroll", methods=["POST"])
def api_scroll():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    data = request.json
    return jsonify(scroll_mouse(data.get("direction", "up"), data.get("amount", 3), data.get("x"), data.get("y")))

@app.route("/api/keyboard/type", methods=["POST"])
def api_type():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    data = request.json
    return jsonify(type_text(data.get("text", "")))

@app.route("/api/keyboard/press", methods=["POST"])
def api_press():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    data = request.json
    return jsonify(press_key(data.get("key", "")))

@app.route("/api/keyboard/hotkey", methods=["POST"])
def api_hotkey():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    data = request.json
    return jsonify(hotkey(data.get("keys", [])))

@app.route("/api/screen/capture", methods=["GET"])
def api_screen():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    return jsonify(capture_screen())

@app.route("/api/system/info", methods=["GET"])
def api_info():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    return jsonify(get_system_info())

@app.route("/api/logs", methods=["GET"])
def api_logs():
    if not is_auth(request.remote_addr):
        return jsonify({"error": "غير مصرح"}), 401
    return jsonify({"logs": logs})

# ===================== قالب HTML =====================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Gordon • التحكم</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body {
            background: #0a0505;
            color: #00ff88;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            justify-content: center;
            padding: 12px;
        }
        .app { max-width: 700px; width:100%; }
        .card {
            background: rgba(20,8,8,0.9);
            border: 1px solid #ff2d55;
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 14px;
        }
        .header { text-align: center; border-bottom: 1px solid #ff2d55; padding-bottom: 12px; margin-bottom: 14px; }
        .logo { font-size: 32px; font-weight: 900; background: linear-gradient(135deg, #ff2d55, #00ff41); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .status { margin-top: 6px; font-size: 13px; color: #aaa; }
        input, button {
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #ff2d55;
            background: rgba(0,0,0,0.5);
            color: #00ff88;
            font-size: 16px;
            outline: none;
            margin-bottom: 8px;
        }
        button {
            background: #ff2d55;
            color: #fff;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: 0.2s;
        }
        button:hover { transform: scale(1.02); box-shadow: 0 0 20px #ff2d55; }
        .btn-sm { padding: 10px; font-size: 13px; background: rgba(255,45,85,0.15); color: #ff2d55; border: 1px solid #ff2d55; }
        .btn-sm:hover { background: rgba(255,45,85,0.3); }
        .grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 8px; }
        .grid-4 { display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; }
        .screen-wrap { background: #000; border-radius: 12px; overflow: hidden; border: 1px solid #ff2d55; position:relative; }
        .screen-wrap img { width: 100%; display: block; pointer-events: none; }
        .screen-overlay {
            position: absolute; top:0; left:0; width:100%; height:100%;
            cursor: crosshair; touch-action: none;
        }
        .touchpad {
            background: rgba(0,0,0,0.5);
            border: 2px solid #ff2d55;
            border-radius: 14px;
            padding: 24px;
            min-height: 120px;
            text-align: center;
            touch-action: none;
            cursor: pointer;
        }
        .touchpad .coords { color: #00ff41; font-weight: bold; margin-top: 6px; }
        .logs-box {
            background: rgba(0,0,0,0.4);
            border-radius: 10px;
            padding: 8px;
            max-height: 120px;
            overflow-y: auto;
            font-size: 12px;
            font-family: monospace;
        }
        .hidden { display: none; }
        .fps { position: absolute; bottom: 8px; right: 12px; background: rgba(0,0,0,0.7); padding: 2px 12px; border-radius: 20px; font-size: 11px; color: #00ff41; }
        @media (max-width:500px){ .grid-3{grid-template-columns:repeat(2,1fr)} .grid-4{grid-template-columns:repeat(2,1fr)} }
    </style>
</head>
<body>
<div class="app">
    <div class="card header">
        <div class="logo">✦ Gordon</div>
        <div class="status" id="statusText">⏳ غير متصل</div>
    </div>

    <!-- المصادقة -->
    <div class="card" id="authBox">
        <input type="password" id="password" placeholder="🔑 كلمة المرور" />
        <button onclick="authenticate()">🚀 دخول</button>
        <div id="authMsg" style="color:#ff6b6b;font-size:14px;text-align:center;"></div>
    </div>

    <!-- المحتوى -->
    <div id="mainContent" class="hidden">
        <!-- الشاشة -->
        <div class="card">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:#ff2d55;font-weight:bold;">📺 بث الشاشة</span>
                <span id="fpsLabel" style="color:#00ff41;font-size:12px;">-- FPS</span>
            </div>
            <div class="screen-wrap">
                <img id="screenImg" src="" alt="الشاشة" />
                <div class="screen-overlay" id="screenOverlay"></div>
                <span class="fps" id="fpsLabel2">--</span>
            </div>
            <div style="display:flex; gap:8px; margin-top:8px; align-items:center; flex-wrap:wrap;">
                <span style="font-size:12px;color:#aaa;">الجودة:</span>
                <input type="range" id="qualitySlider" min="20" max="90" value="60" style="flex:1; accent-color:#ff2d55;" />
                <span id="qualityLabel" style="font-size:13px;">60%</span>
                <button class="btn-sm" onclick="toggleStream()">⏸️ إيقاف</button>
            </div>
        </div>

        <!-- لوحة اللمس -->
        <div class="card">
            <div style="color:#ff2d55;font-weight:bold;margin-bottom:8px;">🖱️ لوحة اللمس</div>
            <div class="touchpad" id="touchpad">
                <div style="color:#aaa;">👆 اسحب لتحريك المؤشر</div>
                <div class="coords" id="coords">X: 0  Y: 0</div>
            </div>
            <div class="grid-3" style="margin-top:8px;">
                <button class="btn-sm" onclick="scrollMouse('up')">⬆️</button>
                <button class="btn-sm" onclick="clickMouse('left')">يسار</button>
                <button class="btn-sm" onclick="scrollMouse('down')">⬇️</button>
                <button class="btn-sm" onclick="clickMouse('right')">يمين</button>
                <button class="btn-sm" onclick="doubleClick()">نقرتين</button>
                <button class="btn-sm" onclick="clickMouse('middle')">وسط</button>
            </div>
        </div>

        <!-- لوحة المفاتيح -->
        <div class="card">
            <div style="color:#ff2d55;font-weight:bold;margin-bottom:8px;">⌨️ لوحة المفاتيح</div>
            <div style="display:flex; gap:6px;">
                <input type="text" id="textInput" placeholder="اكتب نصاً..." style="flex:1;" />
                <button class="btn-sm" onclick="typeText()" style="flex:0;">إرسال</button>
            </div>
            <div class="grid-4" style="margin-top:8px;">
                <button class="btn-sm" onclick="pressKey('enter')">↵</button>
                <button class="btn-sm" onclick="pressKey('backspace')">⌫</button>
                <button class="btn-sm" onclick="pressKey('space')">␣</button>
                <button class="btn-sm" onclick="pressKey('tab')">⇥</button>
                <button class="btn-sm" onclick="hotkey(['ctrl','c'])">Ctrl+C</button>
                <button class="btn-sm" onclick="hotkey(['ctrl','v'])">Ctrl+V</button>
                <button class="btn-sm" onclick="hotkey(['alt','tab'])">Alt+Tab</button>
                <button class="btn-sm" onclick="hotkey(['win','d'])">Win+D</button>
            </div>
        </div>

        <!-- معلومات النظام -->
        <div class="card">
            <div style="color:#ff2d55;font-weight:bold;margin-bottom:8px;">📊 النظام</div>
            <div id="sysInfo" style="font-size:14px;color:#aaa;">
                CPU: <span id="cpuVal">--</span>% &nbsp;|&nbsp; RAM: <span id="memVal">--</span>% &nbsp;|&nbsp; DISK: <span id="diskVal">--</span>%
            </div>
        </div>

        <!-- السجلات -->
        <div class="card">
            <div style="color:#ff2d55;font-weight:bold;margin-bottom:8px;">📝 السجلات</div>
            <div class="logs-box" id="logsList">⏳ جاري التحميل...</div>
        </div>
    </div>
</div>

<script>
    let auth = false;
    let streamInterval = null;
    let streamActive = true;
    const screenImg = document.getElementById('screenImg');
    const coordsDisplay = document.getElementById('coords');
    let screenWidth = 1920, screenHeight = 1080;
    let mouseDown = false;
    let dragStartX = 0, dragStartY = 0;

    function authenticate() {
        const pwd = document.getElementById('password').value;
        if (!pwd) { document.getElementById('authMsg').textContent = '⚠️ أدخل كلمة المرور'; return; }
        fetch('/api/auth', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({password: pwd})
        })
        .then(r => r.json())
        .then(d => {
            if (d.success) {
                auth = true;
                document.getElementById('authBox').classList.add('hidden');
                document.getElementById('mainContent').classList.remove('hidden');
                document.getElementById('statusText').textContent = '✅ متصل';
                startAll();
            } else {
                document.getElementById('authMsg').textContent = '❌ ' + d.message;
            }
        })
        .catch(() => { document.getElementById('authMsg').textContent = '❌ خطأ في الاتصال'; });
    }

    function startAll() {
        updateScreen();
        streamInterval = setInterval(updateScreen, 200);
        setInterval(updateSystemInfo, 2000);
        setInterval(updateLogs, 3000);
        document.getElementById('qualitySlider').oninput = function() {
            document.getElementById('qualityLabel').textContent = this.value + '%';
        };
        setupTouchpad();
        setupScreenInteraction();
    }

    // ===== الشاشة =====
    function updateScreen() {
        if (!auth || !streamActive) return;
        const q = document.getElementById('qualitySlider').value;
        const start = performance.now();
        fetch('/api/screen/capture?quality='+q)
        .then(r => r.json())
        .then(d => {
            if (d.success) {
                screenImg.src = 'data:image/jpeg;base64,' + d.image;
                screenWidth = d.width || 1920;
                screenHeight = d.height || 1080;
                const elapsed = performance.now() - start;
                document.getElementById('fpsLabel').textContent = Math.round(1000/elapsed) + ' FPS';
            }
        })
        .catch(() => {});
    }

    function toggleStream() {
        streamActive = !streamActive;
        this.textContent = streamActive ? '⏸️ إيقاف' : '▶️ تشغيل';
        if (streamActive) updateScreen();
    }

    // ===== التفاعل مع الشاشة =====
    function setupScreenInteraction() {
        const overlay = document.getElementById('screenOverlay');
        overlay.addEventListener('mousedown', function(e) {
            const rect = screenImg.getBoundingClientRect();
            const x = Math.round(((e.clientX - rect.left) / rect.width) * screenWidth);
            const y = Math.round(((e.clientY - rect.top) / rect.height) * screenHeight);
            mouseDown = true;
            dragStartX = x; dragStartY = y;
            sendMove(x, y);
        });
        overlay.addEventListener('mousemove', function(e) {
            if (!mouseDown) return;
            const rect = screenImg.getBoundingClientRect();
            const x = Math.round(((e.clientX - rect.left) / rect.width) * screenWidth);
            const y = Math.round(((e.clientY - rect.top) / rect.height) * screenHeight);
            sendMove(x, y);
        });
        overlay.addEventListener('mouseup', function(e) {
            if (mouseDown) {
                const rect = screenImg.getBoundingClientRect();
                const x = Math.round(((e.clientX - rect.left) / rect.width) * screenWidth);
                const y = Math.round(((e.clientY - rect.top) / rect.height) * screenHeight);
                const dx = x - dragStartX, dy = y - dragStartY;
                if (Math.hypot(dx, dy) < 10) clickMouse('left');
                else sendDrag(dragStartX, dragStartY, x, y);
                mouseDown = false;
            }
        });
        overlay.addEventListener('mouseleave', function() { mouseDown = false; });
        overlay.addEventListener('wheel', function(e) {
            e.preventDefault();
            const rect = screenImg.getBoundingClientRect();
            const x = Math.round(((e.clientX - rect.left) / rect.width) * screenWidth);
            const y = Math.round(((e.clientY - rect.top) / rect.height) * screenHeight);
            const dir = e.deltaY < 0 ? 'up' : 'down';
            fetch('/api/mouse/scroll', {
                method: 'POST',
                headers: {'Content-Type':'application/json'},
                body: JSON.stringify({direction: dir, amount: 4, x, y})
            }).catch(() => {});
        }, {passive: false});
        // دعم اللمس
        overlay.addEventListener('touchstart', function(e) {
            e.preventDefault();
            const touch = e.touches[0];
            const rect = screenImg.getBoundingClientRect();
            const x = Math.round(((touch.clientX - rect.left) / rect.width) * screenWidth);
            const y = Math.round(((touch.clientY - rect.top) / rect.height) * screenHeight);
            mouseDown = true;
            dragStartX = x; dragStartY = y;
            sendMove(x, y);
        }, {passive: false});
        overlay.addEventListener('touchmove', function(e) {
            e.preventDefault();
            if (!mouseDown) return;
            const touch = e.touches[0];
            const rect = screenImg.getBoundingClientRect();
            const x = Math.round(((touch.clientX - rect.left) / rect.width) * screenWidth);
            const y = Math.round(((touch.clientY - rect.top) / rect.height) * screenHeight);
            sendMove(x, y);
        }, {passive: false});
        overlay.addEventListener('touchend', function(e) {
            e.preventDefault();
            if (mouseDown) {
                const touch = e.changedTouches[0];
                const rect = screenImg.getBoundingClientRect();
                const x = Math.round(((touch.clientX - rect.left) / rect.width) * screenWidth);
                const y = Math.round(((touch.clientY - rect.top) / rect.height) * screenHeight);
                const dx = x - dragStartX, dy = y - dragStartY;
                if (Math.hypot(dx, dy) < 10) clickMouse('left');
                else sendDrag(dragStartX, dragStartY, x, y);
                mouseDown = false;
            }
        }, {passive: false});
    }

    function sendMove(x, y) {
        fetch('/api/mouse/move', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({x, y})
        }).catch(() => {});
    }
    function sendDrag(x1, y1, x2, y2) {
        fetch('/api/mouse/drag', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({x1, y1, x2, y2})
        }).catch(() => {});
    }

    // ===== لوحة اللمس =====
    function setupTouchpad() {
        const pad = document.getElementById('touchpad');
        let active = false, drag = false, sx, sy, lx, ly, st;
        function getPos(e) {
            const rect = pad.getBoundingClientRect();
            let cx, cy;
            if (e.touches) { cx = e.touches[0].clientX; cy = e.touches[0].clientY; }
            else { cx = e.clientX; cy = e.clientY; }
            return {
                x: Math.round(((cx - rect.left) / rect.width) * screenWidth),
                y: Math.round(((cy - rect.top) / rect.height) * screenHeight)
            };
        }
        function onStart(e) {
            e.preventDefault();
            const p = getPos(e);
            active = true; drag = false;
            sx = p.x; sy = p.y; lx = p.x; ly = p.y; st = Date.now();
            coordsDisplay.textContent = 'X: '+p.x+'  Y: '+p.y;
            sendMove(p.x, p.y);
        }
        function onMove(e) {
            e.preventDefault();
            if (!active) return;
            const p = getPos(e);
            if (Math.abs(p.x - lx) > 3 || Math.abs(p.y - ly) > 3) {
                sendMove(p.x, p.y);
                lx = p.x; ly = p.y;
                coordsDisplay.textContent = 'X: '+p.x+'  Y: '+p.y;
                if (!drag && Math.hypot(p.x - sx, p.y - sy) > 20) drag = true;
            }
        }
        function onEnd(e) {
            e.preventDefault();
            if (!active) return;
            active = false;
            if (!drag && (Date.now() - st) < 300) clickMouse('left');
            drag = false;
        }
        pad.addEventListener('touchstart', onStart, {passive:false});
        pad.addEventListener('touchmove', onMove, {passive:false});
        pad.addEventListener('touchend', onEnd, {passive:false});
        pad.addEventListener('mousedown', onStart);
        pad.addEventListener('mousemove', onMove);
        pad.addEventListener('mouseup', onEnd);
        pad.addEventListener('mouseleave', onEnd);
        pad.addEventListener('contextmenu', e => { e.preventDefault(); clickMouse('right'); });
    }

    // ===== دوال الماوس =====
    function clickMouse(btn) {
        fetch('/api/mouse/click', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({button: btn})
        }).catch(() => {});
    }
    function doubleClick() { clickMouse('left'); setTimeout(()=>clickMouse('left'), 100); }
    function scrollMouse(dir) {
        fetch('/api/mouse/scroll', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({direction: dir, amount: 4})
        }).catch(() => {});
    }

    // ===== لوحة المفاتيح =====
    function typeText() {
        const txt = document.getElementById('textInput').value;
        if (!txt) return;
        fetch('/api/keyboard/type', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({text: txt})
        }).catch(() => {});
        document.getElementById('textInput').value = '';
    }
    function pressKey(k) {
        fetch('/api/keyboard/press', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({key: k})
        }).catch(() => {});
    }
    function hotkey(keys) {
        fetch('/api/keyboard/hotkey', {
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body: JSON.stringify({keys})
        }).catch(() => {});
    }

    // ===== معلومات النظام =====
    function updateSystemInfo() {
        fetch('/api/system/info')
        .then(r => r.json())
        .then(d => {
            if (d.success) {
                document.getElementById('cpuVal').textContent = d.cpu;
                document.getElementById('memVal').textContent = d.memory;
                document.getElementById('diskVal').textContent = d.disk;
            }
        })
        .catch(() => {});
    }

    // ===== السجلات =====
    function updateLogs() {
        fetch('/api/logs')
        .then(r => r.json())
        .then(d => {
            document.getElementById('logsList').innerHTML = d.logs.map(log =>
                `<div style="border-left:2px solid #ff2d55;padding:2px 8px;margin-bottom:2px;">${log}</div>`
            ).join('');
        })
        .catch(() => {});
    }
</script>
</body>
</html>
"""

# ===================== تشغيل الخادم =====================
def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == "__main__":
    ip = get_ip()
    print("=" * 50)
    print("✦ Gordon Remote Control v7")
    print("=" * 50)
    print(f"🌐 IP Address: {ip}")
    print(f"🔌 Port: {PORT}")
    print(f"🔗 URL: http://{ip}:{PORT}")
    print(f"🔑 Password: {PASSWORD}")
    print("=" * 50)
    print("✅ الخادم يعمل...")
    print("📱 افتح الرابط من هاتفك")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=False)