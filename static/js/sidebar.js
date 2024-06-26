document.addEventListener("DOMContentLoaded", () => {
    const sidebarSocket = new WebSocket(urlSocket+"/sidebar");

    sidebarSocket.onopen = function () {
        sidebarSocket.send(JSON.stringify({"method" : "POST", "name": "loginWithToken", "data" : {"token" : token}}))
    }
})