const url = window.location.href.replace("https://"+window.location.host+"/", "");
const paths = url.split("/");

if(paths.includes("friend")){

    const friend_id = paths[3];
    
    const channelSocket = new WebSocket(urlSocket+"/friend/channel/"+friend_id);

    channelSocket.onopen = function() {
         channelSocket.send(JSON.stringify({"method" : "POST", "name": "loginWithToken", "data" : {"token" : token}}))
    }

    channelSocket.onmessage = function(req) {
        const data = JSON.parse(req.data);

        if(data.name == "sendMessage" && data.data?.content){
            console.log(data.data.content);
        }
    }

    function sendMessage(message){
        channelSocket.send(JSON.stringify({"method" : "POST", "name" : "sendMessage", "data" : {"content" : message}}));
    }

}else if(paths.includes("guild")){

}