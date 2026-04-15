let score = 0;

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const apiStatus = document.getElementById("apiStatus");

function drawScore() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = "24px sans-serif";
    ctx.fillText(`Score: ${score}`, 40, 50);
}

async function sendScoreToAPI(currentScore) {
    try {
        const response = await fetch("/api/score", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ score: currentScore }),
        });

        const result = await response.json();
        apiStatus.textContent = `API status: ${result.message} (${result.score})`;
    } catch (error) {
        apiStatus.textContent = "API status: error";
        console.error("Communication error:", error);
    }
}

canvas.addEventListener("click", () => {
    score += 1;
    drawScore();
    sendScoreToAPI(score);
});

drawScore();