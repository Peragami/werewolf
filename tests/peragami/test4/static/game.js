let score = 0;

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const apiStatus = document.getElementById("apiStatus");
const connectedUsers = document.getElementById("connectedUsers");
const HEARTBEAT_INTERVAL_MS = 15000;
const RECONNECT_DELAY_MS = 1000;
const MAX_WS_RETRY = 5;
const POLL_INTERVAL_MS = 3000;
let playersSocket = null;
let heartbeatTimerId = null;
let pollTimerId = null;
let shouldReconnect = true;
let wsRetryCount = 0;

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
        refreshConnectedUsers();
    } catch (error) {
        apiStatus.textContent = "API status: error";
        console.error("Communication error:", error);
    }
}

async function syncMyScoreFromServer() {
    try {
        const response = await fetch("/api/me", {
            method: "GET",
            cache: "no-store",
        });
        if (!response.ok) {
            return;
        }

        const result = await response.json();
        const serverScore = Number(result.score);
        score = Number.isFinite(serverScore) ? serverScore : 0;
        drawScore();
    } catch (error) {
        console.error("Failed to sync my score:", error);
    }
}

function renderConnectedUsers(players) {
    if (!connectedUsers) {
        return;
    }

    connectedUsers.innerHTML = "";
    const values = Array.isArray(players) && players.length > 0 ? players : [];

    if (values.length === 0) {
        const emptyItem = document.createElement("li");
        emptyItem.textContent = "No players";
        connectedUsers.appendChild(emptyItem);
        return;
    }

    values.forEach((player) => {
        const name = typeof player?.name === "string" ? player.name : "Guest";
        const scoreValue = Number(player?.score);
        const scoreText = Number.isFinite(scoreValue) ? scoreValue : 0;
        const listItem = document.createElement("li");
        listItem.textContent = `${name} : ${scoreText}`;
        connectedUsers.appendChild(listItem);
    });
}

async function refreshConnectedUsers() {
    try {
        const response = await fetch("/api/connected-users", {
            method: "GET",
            cache: "no-store",
        });
        if (!response.ok) {
            return;
        }
        const result = await response.json();
        renderConnectedUsers(result.players);
    } catch (error) {
        console.error("Failed to refresh connected users:", error);
    }
}

function stopHeartbeat() {
    if (heartbeatTimerId !== null) {
        clearInterval(heartbeatTimerId);
        heartbeatTimerId = null;
    }
}

function startPollingFallback() {
    if (pollTimerId !== null) {
        return;
    }
    refreshConnectedUsers();
    pollTimerId = window.setInterval(refreshConnectedUsers, POLL_INTERVAL_MS);
}

function stopPollingFallback() {
    if (pollTimerId !== null) {
        clearInterval(pollTimerId);
        pollTimerId = null;
    }
}

function startHeartbeat() {
    stopHeartbeat();
    heartbeatTimerId = window.setInterval(() => {
        if (playersSocket && playersSocket.readyState === WebSocket.OPEN) {
            playersSocket.send("ping");
        }
    }, HEARTBEAT_INTERVAL_MS);
}

function connectPlayersSocket() {
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    playersSocket = new WebSocket(`${protocol}://${window.location.host}/ws/players`);

    playersSocket.addEventListener("open", () => {
        wsRetryCount = 0;
        stopPollingFallback();
        startHeartbeat();
    });

    playersSocket.addEventListener("message", (event) => {
        try {
            const payload = JSON.parse(event.data);
            if (payload.type === "players") {
                renderConnectedUsers(payload.players);
            }
        } catch (error) {
            console.error("Invalid websocket message:", error);
        }
    });

    playersSocket.addEventListener("close", () => {
        stopHeartbeat();
        if (shouldReconnect && wsRetryCount < MAX_WS_RETRY) {
            wsRetryCount += 1;
            window.setTimeout(connectPlayersSocket, RECONNECT_DELAY_MS);
            return;
        }
        startPollingFallback();
    });

    playersSocket.addEventListener("error", (error) => {
        console.error("WebSocket error:", error);
    });
}

function notifyDisconnect() {
    if (navigator.sendBeacon) {
        navigator.sendBeacon("/api/disconnect");
        return;
    }

    fetch("/api/disconnect", {
        method: "POST",
        keepalive: true,
    }).catch(() => {
        // Ignore network race on tab close.
    });
}

canvas.addEventListener("click", () => {
    score += 1;
    drawScore();
    sendScoreToAPI(score);
});

drawScore();
syncMyScoreFromServer();
refreshConnectedUsers();
connectPlayersSocket();

window.addEventListener("beforeunload", () => {
    shouldReconnect = false;
    stopHeartbeat();
    stopPollingFallback();
    if (playersSocket && playersSocket.readyState === WebSocket.OPEN) {
        playersSocket.close();
    }
    notifyDisconnect();
});

document.addEventListener("visibilitychange", () => {
    if (!document.hidden && playersSocket && playersSocket.readyState === WebSocket.OPEN) {
        playersSocket.send("ping");
    }
});
