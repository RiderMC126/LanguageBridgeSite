document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chatBox');
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const userList = document.getElementById('userList');
    const searchInput = document.getElementById('userSearch');
    const chatWith = document.getElementById('chatWith');
    const currentUser = document.getElementById('currentUser');

    const username = localStorage.getItem("username") || "User";
    currentUser.textContent = username;

    let selectedUser = null;
    let ws = null;

    const connectWS = () => {
        if(ws) ws.close();

        ws = new WebSocket(`ws://${window.location.host}/ws/chat/${username}`);

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if(selectedUser && (data.sender === selectedUser || data.sender === username)){
                addMessageToChat(data.sender, data.content);
            }
        };

        ws.onclose = () => {
            console.log("WebSocket disconnected, reconnecting in 1s...");
            setTimeout(connectWS, 1000);
        };
    };

    const addMessageToChat = (sender, content) => {
        const div = document.createElement('div');
        div.className = sender === username ? "message user" : "message bot";
        div.textContent = content;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    const fetchHistoryUsers = async () => {
        const res = await fetch(`/api/users/history?current=${username}`);
        const data = await res.json();
        userList.innerHTML = "";
        data.users.forEach(user => addUserToList(user));
    };

    const fetchMessages = async (withUser) => {
        const res = await fetch(`/api/messages/history?user1=${username}&user2=${withUser}`);
        const data = await res.json();
        chatBox.innerHTML = "";
        data.messages.forEach(msg => addMessageToChat(msg.sender, msg.content));
    };

    const addUserToList = (user) => {
        const li = document.createElement('li');
        li.textContent = user;
        li.addEventListener('click', () => {
            selectedUser = user;
            chatWith.textContent = "Chat with: " + user;
            fetchMessages(user);
        });
        userList.appendChild(li);
    };

    searchInput.addEventListener('input', async () => {
        const q = searchInput.value.trim();
        if(!q){
            fetchHistoryUsers();
            return;
        }
        const res = await fetch(`/api/users/search?q=${q}&current=${username}`);
        const data = await res.json();
        userList.innerHTML = "";
        data.users.forEach(user => addUserToList(user));
    });

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if(!selectedUser) return alert("Select a user first!");
        const msg = chatInput.value.trim();
        if(!msg) return;

        ws.send(JSON.stringify({
            sender: username,
            receiver: selectedUser,
            content: msg
        }));

        chatInput.value = "";
    });

    fetchHistoryUsers();
    connectWS();
});
