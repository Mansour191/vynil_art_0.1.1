<template>
  <div class="chatbot-root">
    <button class="chat-fab" @click="open = !open">
      <i class="fa-solid fa-comments"></i>
      <span v-if="unreadCount > 0" class="unread-badge">{{ unreadCount }}</span>
    </button>

    <div v-if="open" class="chat-window">
      <div class="chat-header">
        <div class="header-info">
          <strong>Paclos Assistant</strong>
          <span class="status-indicator" :class="{ online: isOnline, offline: !isOnline }">
            <i class="fa-solid fa-circle"></i>
            {{ isOnline ? 'متصل' : 'غير متصل' }}
          </span>
        </div>
        <button class="close-btn" @click="open = false">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
      
      <div class="chat-body" ref="chatBody">
        <div v-if="isLoading" class="loading-indicator">
          <i class="fa-solid fa-spinner fa-spin"></i>
          <span>جاري التحميل...</span>
        </div>
        
        <div v-for="(msg, idx) in messages" :key="idx" :class="['msg', msg.role]">
          <div class="msg-content">
            <p>{{ msg.text }}</p>
            <div v-if="msg.confidence" class="msg-confidence">
              <span>مستوى الثقة: {{ Math.round(msg.confidence * 100) }}%</span>
              <div class="confidence-bar">
                <div class="confidence-fill" :style="{ width: (msg.confidence * 100) + '%' }"></div>
              </div>
            </div>
            <div v-if="msg.sources && msg.sources.length > 0" class="msg-sources">
              <small>المصادر: {{ msg.sources.join(', ') }}</small>
            </div>
          </div>
          <span class="msg-time">{{ formatTime(msg.timestamp) }}</span>
        </div>
      </div>
      
      <div class="typing-indicator" v-if="isTyping">
        <i class="fa-solid fa-ellipsis"></i>
        <span>Paclos Assistant يكتب...</span>
      </div>
      
      <form class="chat-input" @submit.prevent="sendMessage">
        <div class="input-container">
          <input 
            v-model="input" 
            type="text" 
            placeholder="اسأل عن الفينيل، الأسعار، أو أي شيء آخر..."
            :disabled="loading"
            @input="handleTyping"
          />
          <button type="button" class="voice-btn" @click="toggleVoiceInput" :class="{ active: isVoiceInput }">
            <i :class="isVoiceInput ? 'fa-solid fa-microphone' : 'fa-solid fa-microphone-slash'"></i>
          </button>
        </div>
        <button type="submit" :disabled="loading || !input.trim()">
          <i :class="loading ? 'fa-solid fa-spinner fa-spin' : 'fa-solid fa-paper-plane'"></i>
        </button>
      </form>
      
      <div class="chat-actions">
        <button class="action-btn" @click="clearChat">
          <i class="fa-solid fa-trash"></i>
          مسح المحادثة
        </button>
        <button class="action-btn" @click="exportChat">
          <i class="fa-solid fa-download"></i>
          تصدير
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import ChatService from '@/integration/services/ChatService';

const open = ref(false);
const loading = ref(false);
const input = ref('');
const messages = ref([
  { 
    role: 'bot', 
    text: '🤖 مرحباً! أنا مساعد Paclos الذكي. يمكنني مساعدتك في:',
    timestamp: new Date(),
    confidence: 1.0,
    sources: ['system']
  },
  { 
    role: 'bot', 
    text: '🎯 تحليل الأسعار والتوصيات\n📦 معلومات المنتجات\n📊 تتبع الطلبات\n🚚 معلومات الشحن',
    timestamp: new Date(),
    confidence: 1.0,
    sources: ['system']
  },
  { 
    role: 'bot', 
    text: '💡 كيف يمكنني مساعدتك اليوم؟',
    timestamp: new Date(),
    confidence: 1.0,
    sources: ['system']
  }
]);
const isTyping = ref(false);
const isVoiceInput = ref(false);
const unreadCount = ref(0);
const isOnline = ref(true);
const chatBody = ref(null);
const typingTimeout = ref(null);

const sendMessage = async () => {
  const text = input.value.trim();
  if (!text || loading.value) return;
  
  // Add user message
  messages.value.push({ 
    role: 'user', 
    text,
    timestamp: new Date(),
    confidence: 1.0
  });
  
  input.value = '';
  loading.value = true;
  isTyping.value = true;
  
  try {
    const data = await ChatService.ask(text);
    
    // Add bot response
    messages.value.push({ 
      role: 'bot', 
      text: data.answer || 'لم أتمكن من الإجابة الآن.',
      timestamp: new Date(),
      confidence: data.confidence || 0.8,
      sources: data.sources || []
    });
    
    isOnline.value = true;
  } catch (error) {
    console.error('Chat error:', error);
    
    // Show error message but keep service available
    messages.value.push({ 
      role: 'bot', 
      text: 'عذراً، حدث خطأ في الاتصال. لكن يمكنني مساعدتك بالمعرفة المتاحة.',
      timestamp: new Date(),
      confidence: 0.5,
      sources: ['fallback']
    });
    
    isOnline.value = false;
  } finally {
    loading.value = false;
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

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTop = chatBody.value.scrollHeight;
    }
  });
};

const formatTime = (timestamp) => {
  return new Intl.DateTimeFormat('ar-DZ', {
    hour: '2-digit',
    minute: '2-digit'
  }).format(timestamp);
};

const clearChat = () => {
  if (confirm('هل أنت متأكد من مسح المحادثة؟')) {
    messages.value = [{
      role: 'bot',
      text: 'تم مسح المحادثة. كيف يمكنني مساعدتك الآن؟',
      timestamp: new Date(),
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
watch(open, (newValue) => {
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
.chatbot-root { position: fixed; bottom: 20px; right: 20px; z-index: 1200; }
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
.close-btn { background: transparent; border: 0; color: #fff; cursor: pointer; }
.chat-body { flex: 1; overflow: auto; padding: 10px; display: flex; flex-direction: column; gap: 8px; }
.msg { padding: 8px 10px; border-radius: 10px; max-width: 85%; font-size: 13px; line-height: 1.5; }
.msg.user { align-self: flex-end; background: #d4af37; color: #111827; }
.msg.bot { align-self: flex-start; background: #1f2937; border: 1px solid #374151; }
.chat-input { display: flex; gap: 8px; padding: 10px; border-top: 1px solid #374151; }
.chat-input input {
  flex: 1; border: 1px solid #374151; border-radius: 10px; padding: 8px 10px;
  background: #0f172a; color: #f9fafb;
}
.chat-input button {
  border: 0; border-radius: 10px; padding: 8px 12px;
  background: #d4af37; color: #111827; font-weight: 700; cursor: pointer;
}
</style>
