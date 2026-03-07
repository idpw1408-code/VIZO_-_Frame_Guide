let lockStatus = true;
let savedRatio = 16 / 9;

window.onload = function() {
    document.getElementById('ent_w').value = 1920;
    document.getElementById('ent_h').value = 1080;
};

function calculate(target) {
    if (!lockStatus) return;
    const entW = document.getElementById('ent_w');
    const entH = document.getElementById('ent_h');
    const combo = document.getElementById('ratioSelect');
    
    let ratio = (combo.value === "Custom") ? savedRatio : parseFloat(combo.value);

    if (target === 'h' && entW.value) {
        entH.value = Math.round(entW.value / ratio);
    } else if (target === 'w' && entH.value) {
        entW.value = Math.round(entH.value * ratio);
    }
}

function toggle() {
    lockStatus = !lockStatus;
    const btn = document.getElementById('lockBtn');
    const combo = document.getElementById('ratioSelect');
    const entW = document.getElementById('ent_w');
    const entH = document.getElementById('ent_h');

    if (lockStatus) {
        btn.innerText = "🔗";
        btn.style.color = "white";
        if (entW.value && entH.value) savedRatio = entW.value / entH.value;
    } else {
        btn.innerText = "🔓";
        btn.style.color = "#ff4757";
        combo.value = "Custom";
    }
}

function onComboSelect() {
    const combo = document.getElementById('ratioSelect');
    if (combo.value !== "Custom") {
        if (!lockStatus) toggle();
        calculate('h');
    }
}

function copyValue(id) {
    const val = document.getElementById(id).value;
    if (!val) return;
    navigator.clipboard.writeText(val).then(() => {
        alert("값이 복사되었습니다: " + val + "px");
    });
}

let lockStatus = true;

function switchTab(mode) {
    document.getElementById('pixel-tab').style.display = (mode === 'pixel') ? 'block' : 'none';
    document.getElementById('physics-tab').style.display = (mode === 'physics') ? 'block' : 'none';
}

function calculatePhysics() {
    const W = parseFloat(document.getElementById('phy_w').value);
    const H = parseFloat(document.getElementById('phy_h').value);
    const ratio = parseFloat(document.getElementById('phy_ratioSelect').value);

    if (W && H && ratio) {
        const targetH = W / ratio;
        const eachMargin = (H - targetH) / 2;
        
        document.getElementById('result_margin').innerText = eachMargin.toFixed(1);
        document.getElementById('result_area').innerText = `${W.toFixed(1)} x ${targetH.toFixed(1)}`;
    }
}

// ... 기존 calculate, toggle, onComboSelect 함수 유지 ...