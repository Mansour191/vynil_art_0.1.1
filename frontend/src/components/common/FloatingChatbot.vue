<template>
  <div class="chatbot-root">
    <!-- FAB Button (Mobile Only) -->
    <button 
      v-if="!isSidebar && !isFullscreen && !isOpen"
      class="chat-fab" 
      @click="toggleChatbot"
    >
      <i class="fa-solid fa-comments"></i>
      <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
    </button>

    <!-- Sidebar Mode (Desktop) -->
    <div 
      v-if="isSidebar && isOpen"
      class="chat-sidebar"
      :class="{ 'rtl-sidebar': isRTL, 'ltr-sidebar': !isRTL }"
    >
      <div class="chat-header">
        <div class="header-info">
          <div class="avatar-container">
            <img src="/logo.svg" alt="Paclos Logo" class="chat-avatar" />
          </div>
          <div class="title-container">
            <strong>Paclos Assistant</strong>
            <span class="status-indicator" :class="{ online: isOnline, offline: !isOnline }">
              <i class="fa-solid fa-circle"></i>
              {{ isOnline ? 'متصل' : 'غير متصل' }}
            </span>
          </div>
        </div>
        <button class="close-btn" @click="closeChatbot">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      
      <div class="chat-body" ref="chatBody">
        <div v-if="isLoading" class="loading-indicator">
          <i class="fa-solid fa-spinner fa-spin"></i>
          <span>جاري التحميل...</span>
        </div>
        
        <div v-else class="messages-container">
          <div 
            v-for="message in messages" 
            :key="message.timestamp"
            class="message"
            :class="message.role"
          >
            <div class="message-content">
              <p>{{ message.text }}</p>
              <span class="timestamp">{{ formatTime(message.timestamp) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <div class="input-container">
          <input 
            v-model="input" 
            @keyup.enter="sendMessage"
            :placeholder="isTyping ? 'يكتب المساعد...' : 'اكتب رسالتك...'"
            :disabled="loading"
            class="message-input"
          />
          <button 
            @click="sendMessage" 
            :disabled="loading || !input.trim()"
            class="send-btn"
          >
            <i class="fa-solid fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Full-Screen Mode (Mobile) -->
    <div 
      v-if="isFullscreen && isOpen"
      class="chat-fullscreen"
    >
      <div class="chat-header">
        <div class="header-info">
          <div class="avatar-container">
            <img src="/logo.svg" alt="Paclos Logo" class="chat-avatar" />
          </div>
          <div class="title-container">
            <strong>Paclos Assistant</strong>
            <span class="status-indicator" :class="{ online: isOnline, offline: !isOnline }">
              <i class="fa-solid fa-circle"></i>
              {{ isOnline ? 'متصل' : 'غير متصل' }}
            </span>
          </div>
        </div>
        <button class="close-btn" @click="closeChatbot">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      
      <div class="chat-body" ref="chatBody">
        <div v-if="isLoading" class="loading-indicator">
          <i class="fa-solid fa-spinner fa-spin"></i>
          <span>جاري التحميل...</span>
        </div>
        
        <div v-else class="messages-container">
          <div 
            v-for="message in messages" 
            :key="message.timestamp"
            class="message"
            :class="message.role"
          >
            <div class="message-content">
              <p>{{ message.text }}</p>
              <span class="timestamp">{{ formatTime(message.timestamp) }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="chat-input">
        <div class="input-container">
          <input 
            v-model="input" 
            @keyup.enter="sendMessage"
            :placeholder="isTyping ? 'يكتب المساعد...' : 'اكتب رسالتك...'"
            :disabled="loading"
            class="message-input"
          />
          <button 
            @click="sendMessage" 
            :disabled="loading || !input.trim()"
            class="send-btn"
          >
            <i class="fa-solid fa-paper-plane"></i>
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { nextTick, ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import ChatService from '@/integration/services/ChatService';
import { DateUtils } from '@/utils/DateUtils';
import { useChatbotStore } from '@/store/chatbot';

// Props
const props = defineProps({
  isSidebar: {
    type: Boolean,
    default: false
  },
  isFullscreen: {
    type: Boolean,
    default: false
  }
});

// Composables
const { locale } = useI18n();
const chatbotStore = useChatbotStore();

// Reactive State
const loading = ref(false);
const isLoading = ref(false); // For template loading indicator
const isVoiceInput = ref(false);
const unreadCount = ref(0);
const isOnline = ref(true);
const chatBody = ref(null);
const typingTimeout = ref(null);
const isTyping = ref(false);

// Computed Properties
const isOpen = computed(() => chatbotStore.isOpen);
const isRTL = computed(() => locale.value === 'ar');
const input = ref('');
const messages = ref([
  { 
    role: 'bot', 
    text: '🤖 مرحباً! أنا مساعد Paclos الذكي. يمكنني مساعدتك في:',
    timestamp: DateUtils.createTimestamp(),
    confidence: 1.0,
    sources: ['system']
  },
  { 
    role: 'bot', 
    text: '🎯 تحليل الأسعار والتوصيات\n📦 معلومات المنتجات\n📊 تتبع الطلبات\n🚚 معلومات الشحن',
    timestamp: DateUtils.createTimestamp(),
    confidence: 1.0,
    sources: ['system']
  },
  { 
    role: 'bot', 
    text: '💡 كيف يمكنني مساعدتك اليوم؟',
    timestamp: DateUtils.createTimestamp(),
    confidence: 1.0,
    sources: ['system']
  }
]);

// Methods
const toggleChatbot = () => {
  chatbotStore.toggle();
};

const closeChatbot = () => {
  chatbotStore.close();
};

const formatTime = (timestamp) => {
  return DateUtils.formatTime(timestamp);
};

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight;
    }
  });
};

const sendMessage = async () => {
  const text = input.value.trim();
  if (!text || loading.value) return;
  
  // Add user message
  messages.value.push({ 
    role: 'user', 
    text,
    timestamp: DateUtils.createTimestamp()
  });
  input.value = '';
  loading.value = true;
  isLoading.value = true; // Set loading indicator to true
  isTyping.value = true;
  
  try {
    // Call ChatService.ask and get response
    const response = await ChatService.ask(text, {
      temperature: 0.7,
      top_p: 0.9,
      max_tokens: 500
    });
    
    // Add bot response
    messages.value.push({ 
      role: 'bot', 
      text: response.answer || response.response || 'عذراً، لم أتمكن من معالجة طلبك.',
      timestamp: DateUtils.createTimestamp(),
      confidence: response.confidence || 0.5,
      sources: response.sources || ['chatbot']
    });
    
  } catch (error) {
    console.error('Chat error:', error);
    
    // Enhanced error handling
    messages.value.push({ 
      role: 'bot', 
      text: 'عذراً، واجهت بعض الصعافات. يمكنني مساعدتك بالمعرفة المتاحة أو يمكنك التواصل مع فريق Paclos مباشرة.',
      timestamp: DateUtils.createTimestamp(),
      confidence: 0.3,
      sources: ['error_handling'],
      isError: true
    });
    
    isOnline.value = false;
  } finally {
    // Always reset loading states
    loading.value = false;
    isLoading.value = false; // Critical: Always reset loading indicator
    isTyping.value = false;
    scrollToBottom();
  }
};

const handleTyping = () => {
  isTyping.value = true;
  
  // Clear existing timeout
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value);
  }
  
  // Stop typing indicator after 1 second of inactivity
  typingTimeout.value = setTimeout(() => {
    isTyping.value = false;
  }, 1000);
};

const clearChat = () => {
  if (confirm('هل أنت متأكد من مسح المحادثة؟')) {
    messages.value = [{
      role: 'bot',
      text: 'تم مسح المحادثة. كيف يمكنني مساعدتك الآن؟',
      timestamp: DateUtils.createTimestamp(),
      confidence: 1.0,
      sources: ['system']
    }];
    unreadCount.value = 0;
  }
};

const exportChat = () => {
  const chatData = {
    messages: messages.value,
    sessionId: ChatService.sessionId,
    exportDate: new Date().toISOString()
  };
  
  const blob = new Blob([JSON.stringify(chatData, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `paclos-chat-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  URL.revokeObjectURL(url);
};

const toggleVoiceInput = () => {
  isVoiceInput.value = !isVoiceInput.value;
  
  if (isVoiceInput.value) {
    // Initialize voice recognition if available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      startVoiceRecognition();
    } else {
      alert('ميزة التعرف على الصوت غير مدعومة في متصفحك');
      isVoiceInput.value = false;
    }
  } else {
    stopVoiceRecognition();
  }
};

const startVoiceRecognition = () => {
  // Voice recognition implementation would go here
  console.log('Voice recognition started');
};

const stopVoiceRecognition = () => {
  // Stop voice recognition
  console.log('Voice recognition stopped');
};

// Watch for new messages when chat is closed
watch(isOpen, (newValue) => {
  if (newValue) {
    unreadCount.value = 0;
    scrollToBottom();
  }
});

// Check service availability
const checkServiceStatus = () => {
  const isAvailable = ChatService.checkAvailability();
  isOnline.value = isAvailable;
  
  if (!isAvailable) {
    messages.value.push({
      role: 'bot',
      text: '⚠️ خدمة الذكاء الاصطناعي غير متاحة حالياً. يعمل النظام في الوضع الاحتياطي.',
      timestamp: new Date(),
      confidence: 0.3,
      sources: ['system']
    });
  }
};

onMounted(() => {
  checkServiceStatus();
  
  // Check service status every 30 seconds
  setInterval(checkServiceStatus, 30000);
});
</script>

<style scoped>
/* Chatbot Root Container */
.chatbot-root {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1200;
}

[dir="rtl"] .chatbot-root {
  right: auto;
  left: 20px;
}

/* FAB Button (Mobile Only) */
.chat-fab {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  border: none;
  color: #0A0A0A;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 8px 32px rgba(212, 175, 55, 0.4);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1201;
}

[dir="rtl"] .chat-fab {
  right: auto;
  left: 20px;
}

.chat-fab:hover {
  transform: scale(1.1);
  box-shadow: 0 12px 48px rgba(212, 175, 55, 0.6);
}

.unread-badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background: #FF4444;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Sidebar Mode (Desktop) */
.chat-sidebar {
  width: 100%;
  height: 100%;
  background: linear-gradient(180deg, #0A0A0A 0%, #1A1A1A 100%);
  border-left: 1px solid #D4AF37;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.chat-sidebar.rtl-sidebar {
  border-left: none;
  border-right: 1px solid #D4AF37;
}

.chat-sidebar.ltr-sidebar {
  border-right: none;
  border-left: 1px solid #D4AF37;
}

/* Full-Screen Mode (Mobile) */
.chat-fullscreen {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(180deg, #0A0A0A 0%, #1A1A1A 100%);
  display: flex;
  flex-direction: column;
  z-index: 9999;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Chat Header */
.chat-header {
  background: linear-gradient(135deg, #1A1A1A 0%, #2A2A2A 100%);
  padding: 16px 20px;
  border-bottom: 1px solid #D4AF37;
  display: flex;
  justify-content: space-between;
  align-items: center;
  min-height: 70px;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.chat-avatar {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

.title-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.title-container strong {
  color: #F5F5F5;
  font-size: 16px;
  font-weight: 600;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #F5F5F5;
  opacity: 0.8;
}

.status-indicator.online {
  color: #4CAF50;
}

.status-indicator.offline {
  color: #FF4444;
}

.close-btn {
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: #F5F5F5;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.close-btn:hover {
  background: rgba(255, 68, 68, 0.2);
  color: #FF4444;
}

/* Chat Body */
.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #0A0A0A;
}

.messages-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.message {
  display: flex;
  animation: messageSlide 0.3s ease-out;
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 16px;
  position: relative;
}

.message.user .message-content {
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  color: #0A0A0A;
  border-bottom-right-radius: 4px;
}

.message.bot .message-content {
  background: linear-gradient(135deg, #1A1A1A 0%, #2A2A2A 100%);
  color: #F5F5F5;
  border: 1px solid #333;
  border-bottom-left-radius: 4px;
}

.message-content p {
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
}

.timestamp {
  font-size: 11px;
  opacity: 0.7;
  margin-top: 4px;
  display: block;
}

/* Chat Input */
.chat-input {
  padding: 16px 20px;
  background: linear-gradient(135deg, #1A1A1A 0%, #2A2A2A 100%);
  border-top: 1px solid #333;
}

.input-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.message-input {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #333;
  border-radius: 24px;
  padding: 12px 16px;
  color: #F5F5F5;
  font-size: 14px;
  outline: none;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.message-input:focus {
  border-color: #D4AF37;
  background: rgba(255, 255, 255, 0.08);
}

.message-input::placeholder {
  color: rgba(245, 245, 245, 0.5);
}

.send-btn {
  background: linear-gradient(135deg, #D4AF37 0%, #B8860B 100%);
  border: none;
  color: #0A0A0A;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(212, 175, 55, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Loading Indicator */
.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px;
  color: #F5F5F5;
  opacity: 0.8;
}

.loading-indicator i {
  animation: spin 1s linear infinite;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes slideInRight {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideInLeft {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes messageSlide {
  from {
    transform: translateY(10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Responsive Design */
@media (max-width: 1023px) {
  .chat-sidebar {
    display: none !important;
  }
}

@media (max-width: 640px) {
  .chat-fab {
    bottom: 16px;
    right: 16px;
    width: 56px;
    height: 56px;
    font-size: 20px;
  }
  
  [dir="rtl"] .chat-fab {
    right: auto;
    left: 16px;
  }
}

/* RTL Support */
[dir="rtl"] .message.user .message-content {
  border-bottom-right-radius: 16px;
  border-bottom-left-radius: 4px;
}

[dir="rtl"] .message.bot .message-content {
  border-bottom-left-radius: 16px;
  border-bottom-right-radius: 4px;
}

.chat-fab {
  width: 56px; height: 56px; border-radius: 999px; border: 0; cursor: pointer;
  background: linear-gradient(135deg, #d4af37, #f7df90); color: #111827;
  box-shadow: 0 10px 24px rgba(212, 175, 55, 0.35);
}
.chat-window {
  width: 340px; height: 470px; margin-bottom: 10px; border-radius: 16px; overflow: hidden;
  border: 1px solid rgba(212, 175, 55, 0.35); background: #111827; color: #f9fafb;
  display: flex; flex-direction: column;
}
.chat-header {
  padding: 10px 12px; background: linear-gradient(135deg, rgba(212,175,55,.2), rgba(120,120,120,.15));
  display: flex; align-items: center; justify-content: space-between;
}

.header-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-container {
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  filter: drop-shadow(0 0 5px #D4AF37);
  transition: filter 0.3s ease;
}

.chat-avatar:hover {
  filter: drop-shadow(0 0 8px #D4AF37) drop-shadow(0 0 12px rgba(212, 175, 55, 0.4));
}

.title-container {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
</style>
