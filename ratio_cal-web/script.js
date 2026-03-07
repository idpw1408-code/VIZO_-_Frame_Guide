// 1. 초기 설정 변수
let lockStatus = true;
let savedRatio = 16 / 9;

// 2. 계산 함수 (체인 상태 확인 로직 포함)
function calculate(target) {
    // 자물쇠가 풀려있으면(False) 계산을 중단합니다. (데스크탑 v1.0 로직 반영)
    if (!lockStatus) return;

    const entW = document.getElementById('ent_w');
    const entH = document.getElementById('ent_h');
    const combo = document.getElementById('ratioSelect');
    
    try {
        let ratio;
        if (combo.value === "Custom") {
            ratio = savedRatio;
        } else {
            ratio = parseFloat(combo.value);
        }

        if (target === 'h' && entW.value) {
            entH.value = Math.round(entW.value / ratio);
        } else if (target === 'w' && entH.value) {
            entW.value = Math.round(entH.value * ratio);
        }
    } catch (e) {
        console.error("계산 오류 발생");
    }
}

// 3. 자물쇠 토글 함수
function toggle() {
    lockStatus = !lockStatus;
    const btn = document.getElementById('lockBtn');
    const combo = document.getElementById('ratioSelect');
    const entW = document.getElementById('ent_w');
    const entH = document.getElementById('ent_h');

    if (lockStatus) {
        btn.innerText = "🔗";
        btn.style.color = "white";
        // 다시 잠길 때 현재 입력된 값으로 비율 저장
        if (entW.value && entH.value) {
            savedRatio = entW.value / entH.value;
        }
    } else {
        btn.innerText = "🔓";
        btn.style.color = "#ff4757";
        combo.value = "Custom"; // 체인 풀면 자동으로 Custom 선택
    }
}

// 4. 콤보박스 선택 시 호출되는 함수
function onComboSelect() {
    const combo = document.getElementById('ratioSelect');
    if (combo.value !== "Custom") {
        if (!lockStatus) {
            toggle(); // 고정 비율 선택 시 다시 잠금
        }
        calculate('h'); // 선택 즉시 계산 실행
    }
}