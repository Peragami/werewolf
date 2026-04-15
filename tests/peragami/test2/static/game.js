// スコア変数
let score = 0;

// キャンバスとコンテキストの取得
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// クリックでスコアを増やす
canvas.addEventListener('click', () => {
    score += 1;
    drawScore();
    // FastAPIにスコアを送信
    sendScoreToAPI(score);
});

// スコアを描画
function drawScore() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = '24px sans-serif';
    ctx.fillText(`スコア: ${score}`, 50, 50);
}

// FastAPIにスコアを送信する関数
async function sendScoreToAPI(currentScore) {
    try {
        const response = await fetch('/api/score', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ score: currentScore }),
        });
        const result = await response.json();
        console.log('APIからの応答:', result);
    } catch (error) {
        console.error('通信エラー:', error);
    }
}

// 初期描画
drawScore();