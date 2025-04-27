// static/js/chat.js
class ChatApp {
    constructor() {
        this.socket = null;
        this.currentRoomId = null;
        this.currentUser = null;
        
        this.initialize();
    }
    
    initialize() {
        // Get current user from Django template
        this.currentUser = JSON.parse(document.getElementById('user-data').textContent);
        
        // Initialize event listeners
        this.setupEventListeners();
        
        // Load initial chat rooms
        this.loadChatRooms();
    }
    
    setupEventListeners() {
        // Chat room selection
        document.querySelectorAll('.chat-room-item').forEach(item => {
            item.addEventListener('click', (e) => {
                const roomId = e.currentTarget.dataset.roomId;
                this.connectToChatRoom(roomId);
            });
        });
        
        // Message send button
        document.getElementById('send-message-btn').addEventListener('click', () => {
            this.sendMessage();
        });
        
        // Message input field (for Enter key)
        document.getElementById('message-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    async loadChatRooms() {
        try {
            const response = await fetch('/api/messaging/chatrooms/');
            const chatRooms = await response.json();
            
            this.renderChatRooms(chatRooms);
            
            // Connect to the first room if available
            if (chatRooms.length > 0) {
                this.connectToChatRoom(chatRooms[0].room_id);
            }
        } catch (error) {
            console.error('Error loading chat rooms:', error);
        }
    }
    
    renderChatRooms(chatRooms) {
        const chatRoomsContainer = document.getElementById('chat-rooms-list');
        chatRoomsContainer.innerHTML = '';
        
        chatRooms.forEach(room => {
            const isVendor = this.currentUser.id === room.vendor.user.id;
            const otherUser = isVendor ? room.customer : room.vendor;
            
            const roomElement = document.createElement('div');
            roomElement.className = `chat-room-item ${this.currentRoomId === room.room_id ? 'active' : ''}`;
            roomElement.dataset.roomId = room.room_id;
            
            roomElement.innerHTML = `
                <div class="chat-room-avatar">
                    <img src="${otherUser.image || '/static/images/default-avatar.png'}" alt="${otherUser.username}">
                    ${room.unread_count > 0 ? `<span class="unread-badge">${room.unread_count}</span>` : ''}
                </div>
                <div class="chat-room-info">
                    <h5>${otherUser.username}</h5>
                    <p class="last-message">${room.last_message ? room.last_message.message.substring(0, 30) + (room.last_message.message.length > 30 ? '...' : '') : 'No messages yet'}</p>
                </div>
                <div class="chat-room-time">
                    ${room.last_message ? new Date(room.last_message.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ''}
                </div>
            `;
            
            chatRoomsContainer.appendChild(roomElement);
        });
        
        // Re-attach event listeners
        this.setupEventListeners();
    }
    
    connectToChatRoom(roomId) {
        // Disconnect from current room if connected
        if (this.socket) {
            this.socket.close();
        }
        
        this.currentRoomId = roomId;
        
        // Highlight selected room
        document.querySelectorAll('.chat-room-item').forEach(item => {
            item.classList.toggle('active', item.dataset.roomId === roomId);
        });
        
        // Connect to WebSocket
        const wsScheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsPath = `${wsScheme}${window.location.host}/ws/chat/${roomId}/`;
        
        this.socket = new WebSocket(wsPath);
        
        this.socket.onopen = (e) => {
            console.log('WebSocket connection established');
            this.loadMessages(roomId);
        };
        
        this.socket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            this.appendMessage(data, false);
        };
        
        this.socket.onclose = (e) => {
            console.log('WebSocket connection closed');
        };
        
        this.socket.onerror = (e) => {
            console.error('WebSocket error:', e);
        };
    }
    
    async loadMessages(roomId) {
        try {
            const response = await fetch(`/api/messaging/chatrooms/${roomId}/messages/`);
            const messages = await response.json();
            
            this.renderMessages(messages);
        } catch (error) {
            console.error('Error loading messages:', error);
        }
    }
    
    renderMessages(messages) {
        const messagesContainer = document.getElementById('messages-container');
        messagesContainer.innerHTML = '';
        
        messages.forEach(message => {
            this.appendMessage(message, true);
        });
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    appendMessage(message, isHistorical) {
        const messagesContainer = document.getElementById('messages-container');
        const isOwnMessage = message.sender_id === this.currentUser.id;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${isOwnMessage ? 'outgoing' : 'incoming'}`;
        messageElement.dataset.messageId = message.id;
        
        messageElement.innerHTML = `
            <div class="message-content">
                <div class="message-text">${message.message}</div>
                <div class="message-time">${new Date(message.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
            </div>
            ${!isOwnMessage ? `<div class="message-avatar">
                <img src="${message.sender_image || '/static/images/default-avatar.png'}" alt="${message.sender_username}">
            </div>` : ''}
        `;
        
        if (isHistorical) {
            messagesContainer.appendChild(messageElement);
        } else {
            // New message - add with animation
            messageElement.classList.add('new-message');
            messagesContainer.appendChild(messageElement);
            
            // Scroll to bottom if not scrolled up
            if (messagesContainer.scrollTop + messagesContainer.clientHeight >= messagesContainer.scrollHeight - 50) {
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }
        }
    }
    
    sendMessage() {
        const messageInput = document.getElementById('message-input');
        const message = messageInput.value.trim();
        
        if (message && this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify({
                'message': message,
                'sender_id': this.currentUser.id
            }));
            
            // Clear input
            messageInput.value = '';
        }
    }
    
    // Periodically check for unread messages
    startUnreadCheck() {
        setInterval(async () => {
            try {
                const response = await fetch('/api/messaging/unread-count/');
                const data = await response.json();
                
                // Update UI with unread count
                document.getElementById('unread-count').textContent = data.unread_count > 0 ? data.unread_count : '';
                document.getElementById('unread-count').style.display = data.unread_count > 0 ? 'block' : 'none';
                
                // Refresh chat rooms list to update unread badges
                this.loadChatRooms();
            } catch (error) {
                console.error('Error checking unread messages:', error);
            }
        }, 30000); // Check every 30 seconds
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const chatApp = new ChatApp();
    chatApp.startUnreadCheck();
});


