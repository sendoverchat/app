const url = window.location.href.replace("https://"+window.location.host+"/", "");
const paths = url.split("/");

const urlSocket = "wss://sendover.fr:19062"

if(paths.includes("friend")){

    const friend_id = paths[3];
    
    const channelSocket = new WebSocket(urlSocket+"/friend/channel/"+friend_id);

}else if(paths.includes("guild")){

}