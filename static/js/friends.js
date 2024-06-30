const socketFriends = new WebSocket(urlSocket+"/friends");

socketFriends.onopen = function() {
    socketFriends.send(JSON.stringify({"method" : "POST", "name": "loginWithToken", "data" : {"token" : token}}));
}

function htmlEntities(str) {
    return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

socketFriends.onmessage = function(message) {

    const data = JSON.parse(message.data);

    if(data.name == "errorFriendRequest"){
        document.getElementById("addfrienderrormessage").textContent = data.data;
    }
    if(data.name == "successFriendRequest"){

        const user = data.data;

        let status_name = "Offline";
        let status_styles = "background: var(--no-hover);"
        if(user["user_status"] == 1){
            status_name = "Online";
            status_styles = "background: var(--fire-breeze-500);";
        }else if(user["user_status"] == 2){
            status_name = "Do not distrub";
            status_styles = "background: var(--horty-red-600);";
        }else if(user["user_status"] == 4){
            status_name = "Focus";
            status_styles = "background: var(--fuwa-link-600);";
        }

        let div = `
        <div class="div-article-list" id="user_${user["user_id"]}">
        <div class="div-profile-picture-container" id="${htmlEntities(user["username"])}">
            <style>
            #${htmlEntities(user["username"])} {
                background: url('${user["avatar"]}');
                background-size: cover !important;
                background-position: center !important;
            }
            </style>
            <div class="div-profile-status-info" id="${htmlEntities(user["username"])}-status">
            <style>
                #${htmlEntities(user["username"])}-status {               
                    ${status_styles}
                }
            </style>
        </div>
        </div>
        <div class="div-text-info-profile-container">
            <h1>${htmlEntities(user["displayname"])}</h1>
            <p>
            ${status_name}
            </p>
        </div>
        <svg class="svg-deny-request-btn" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M18 6L6 18M6 6L18 18" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        </div>
        `;

        let div_result = document.getElementById("viewfriendrequestdivresult");
        if(div_result.innerHTML.includes("div-nothing-request")){
            div_result.innerHTML = div;
        }else{
            div_result.innerHTML = div + div_result.innerHTML;
        }
        

    }

    if(data.name == "updateUser"){

        const user = data.data;
        const friend_div = document.querySelector("#"+user["username"]).parentNode;
        if("online_friends" && user["user_status"] == 0 && user["is_friend"]){
            document.getElementById("offline_friends").appendChild(friend_div);
        }else if(user["is_friend"]){
            document.getElementById("online_friends").appendChild(friend_div);
        }

        friend_div.querySelector("#"+user["username"]).style.background = "url('"+user["avatar"]+"')";
        
        const div_online_count = document.querySelector("span.count_online");
        const div_offline_count = document.querySelector("span.count_offline");

        div_online_count.textContent = document.querySelectorAll("#online_friends .div-element-friend-profile").length;
        div_offline_count.textContent = document.querySelectorAll("#offline_friends .div-element-friend-profile").length;

        if(user["user_status"] == 0){
            friend_div.querySelector("#"+user["username"]+"-status").style.background = "var(--no-hover)"     
            friend_div.querySelector(".div-text-info-profile-container p").textContent = "Offline";
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

document.getElementById("add-element").onclick = () => {
    document.getElementById("viewfriendrequestdivresult").style.display = "none";
    document.getElementById("addfrienddivresult").style.display = "initial";
}
document.getElementById("pending-element").onclick = () => {
    document.getElementById("viewfriendrequestdivresult").style.display = "initial";
    document.getElementById("addfrienddivresult").style.display = "none";
}
document.getElementById("addfriendbutton").onclick = () => {
    socketFriends.send(JSON.stringify({"method" : "POST", "name" : "sendFriendRequest", "data" : {"username" : document.getElementById("addfriendinput").value}}))
}