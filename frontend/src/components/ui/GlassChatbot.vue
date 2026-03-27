<template>
  <div class="glass-chatbot-wrapper">
    <v-btn
      v-if="!isOpen"
      color="primary"
      icon="mdi-robot-happy-outline"
      size="x-large"
      elevation="8"
      class="chat-fab logo-glow"
      @click="isOpen = true"
    >
      <v-badge
        v-if="unreadCount > 0"
        :content="unreadCount"
        color="error"
        offset-x="3"
        offset-y="3"
      >
        <v-icon size="32">mdi-robot-happy-outline</v-icon>
      </v-badge>
      <v-icon v-else size="32">mdi-robot-happy-outline</v-icon>
    </v-btn>

    <v-expand-transition>
      <v-card
        v-if="isOpen"
        class="chat-window glass-card border-gold"
        width="380"
        height="550"
        rounded="xl"
      >
        <v-toolbar color="primary" class="px-2">
          <v-avatar size="40" class="bg-white-opacity-20 ml-3">
            <v-img src="/logo.svg" />
          </v-avatar>
          <div>
            <v-toolbar-title class="text-subtitle-1 font-weight-bold">مساعد Paclos الذكي</v-toolbar-title>
            <div class="text-caption d-flex align-center">
              <v-badge dot color="success" class="ml-2"></v-badge>
              متصل الآن
            </div>
          </div>
          <v-spacer></v-spacer>
          <v-btn icon="mdi-close" variant="text" @click="isOpen = false"></v-btn>
        </v-toolbar>

        <v-card-text class="chat-messages-container pa-4">
          <div v-for="(msg, i) in messages" :key="i" 
            :class="['d-flex mb-4', msg.role === 'user' ? 'justify-end' : 'justify-start']">
            
            <div :class="['message-bubble', msg.role === 'user' ? 'user-bubble' : 'bot-bubble']">
              {{ msg.text }}
              <div class="text-caption mt-1 opacity-60 text-left" style="font-size: 0.7rem;">
                {{ msg.time }}
              </div>
            </div>
          </div>
          
          <div v-if="isTyping" class="d-flex justify-start mb-4">
            <div class="bot-bubble typing-dots">
              <span>.</span><span>.</span><span>.</span>
            </div>
          </div>
        </v-card-text>

        <v-divider class="opacity-10"></v-divider>
        <v-card-actions class="pa-3 bg-glass-dark">
          <v-text-field
            v-model="userInput"
            placeholder="كيف يمكنني مساعدتك؟"
            variant="solo-filled"
            flat
            density="comfortable"
            rounded="pill"
            hide-details
            class="chat-input"
            @keyup.enter="sendMessage"
          >
            <template v-slot:append-inner>
              <v-btn
                icon="mdi-send-variant"
                variant="text"
                color="primary"
                :disabled="!userInput.trim()"
                @click="sendMessage"
              ></v-btn>
            </template>
          </v-text-field>
        </v-card-actions>
      </v-card>
    </v-expand-transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const isOpen = ref(false);
const userInput = ref('');
const isTyping = ref(false);
const unreadCount = ref(1);
const messages = ref([
  { role: 'bot', text: 'مرحباً بك في Paclos! كيف يمكنني مساعدتك في تجديد منزلك اليوم؟', time: '10:00 AM' }
]);

const sendMessage = async () => {
  if (!userInput.value.trim()) return;

  // إضافة رسالة المستخدم
  messages.value.push({
    role: 'user',
    text: userInput.value,
    time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  });

  const query = userInput.value;
  userInput.value = '';
  isTyping.value = true;

  // محاكاة استجابة الـ Backend (Django)
  setTimeout(() => {
    isTyping.value = false;
    messages.value.push({
      role: 'bot',
      text: 'شكراً لتواصلك. فريق Paclos سيقوم بالرد على استفسارك بخصوص "' + query + '" في أقرب وقت ممكن.',
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    });
  }, 1500);
};
</script>

<style scoped>
.glass-chatbot-wrapper {
  position: fixed;
  bottom: 30px;
  left: 30px; /* للغة العربية يفضل وضعه يساراً أو يميناً حسب التصميم */
  z-index: 9999;
}

.chat-fab {
  width: 65px !important;
  height: 65px !important;
  background: linear-gradient(135deg, #d4af37 0%, #aa891a 100%) !important;
}

.chat-window {
  position: absolute;
  bottom: 80px;
  left: 0;
  display: flex;
  flex-direction: column;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.4) !important;
  overflow: hidden;
}

.glass-card {
  background: rgba(15, 15, 26, 0.9) !important;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(212, 175, 55, 0.3) !important;
}

.chat-messages-container {
  flex-grow: 1;
  overflow-y: auto;
  background: rgba(255, 255, 255, 0.02);
}

.message-bubble {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 18px;
  font-size: 0.95rem;
  line-height: 1.4;
}

.user-bubble {
  background: #d4af37;
  color: #1a1a2e;
  border-bottom-left-radius: 4px;
}

.bot-bubble {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-bottom-right-radius: 4px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.bg-white-opacity-20 {
  background: rgba(255, 255, 255, 0.2);
}

.bg-glass-dark {
  background: rgba(0, 0, 0, 0.2);
}

.typing-dots span {
  animation: blink 1.4s infinite both;
  font-size: 1.5rem;
  margin: 0 2px;
}

.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
  0% { opacity: 0.2; }
  20% { opacity: 1; }
  100% { opacity: 0.2; }
}

.logo-glow {
  filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.5));
}
</style>
