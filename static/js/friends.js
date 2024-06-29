const socketFriends = new WebSocket(urlSocket+"/friends");

socketFriends.onopen = function() {
    socketFriends.send(JSON.stringify({"method" : "POST", "name": "loginWithToken", "data" : {"token" : token}}));
}

socketFriends.onmessage = function(message) {

    const data = JSON.parse(message.data);

    if(data.name == "updateUser"){

        const user = data.data;

        if(user["is_friend"]){

            const friend_div = document.querySelector("#"+user["username"]).parentNode;
            if("online_friends" && user["user_status"] == 0){
                document.getElementById("offline_friends").appendChild(friend_div);
            }else{
                document.getElementById("online_friends").appendChild(friend_div);
            }

            friend_div.querySelector("#"+user["username"]).style.background = "url('"+user["avatar"]+"')";
            
            const div_online_count = document.querySelector("span.count_online");
            const div_offline_count = document.querySelector("span.count_offline");

            div_online_count.textContent = document.querySelectorAll("#online_friends .div-element-friend-profile").length;
            div_offline_count.textContent = document.querySelectorAll("#offline_friends .div-element-friend-profile").length;

            if(user["user_status"] == 0){
                friend_div.querySelector("#"+user["username"]+"-status").style.background = "var(--no-hover)"     
                friend_div.querySelector(".div-text-info-profile-container p").textContent = "offline";
            }else if(user["user_status"] == 1){
                friend_div.querySelector("#"+user["username"]+"-status").style.background = "var(--fire-breeze-500)"
                friend_div.querySelector(".div-text-info-profile-container p").textContent = "Online";
            }else if(user["user_status"] == 2){
                friend_div.querySelector("#"+user["username"]+"-status").style.background = "var(--horty-red-600)"
                friend_div.querySelector(".div-text-info-profile-container p").textContent = "Do not distrub";
            }else if(user["user_status"] == 4){
                friend_div.querySelector("#"+user["username"]+"-status").style.background = "var(--fuwa-link-600)"
                friend_div.querySelector(".div-text-info-profile-container p").textContent = "Focus";
            }
                
        }

    }

}