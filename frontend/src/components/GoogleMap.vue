<template>
  <section class="google-map-section py-12">
    <v-container>
      <v-row class="mb-8">
        <v-col cols="12" class="text-center">
          <h2 class="text-h4 font-weight-bold mb-4">
            <v-icon color="primary" class="mr-3">mdi-map-marker</v-icon>
            موقعنا
          </h2>
          <p class="text-body-1 text-medium-emphasis mb-6">
            نحن موجودون في قلب مدينة الجزائر لتقديم أفضل الخدمات لعملائنا
          </p>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12" lg="8" class="mb-6 mb-lg-0">
          <v-card class="map-container" elevation="4">
            <!-- Google Map Iframe -->
            <div class="map-wrapper">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2634.123456789!2d3.123456789!3d36.123456789!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMznCsDA3JzI0LjAiTiAzwrA3JzI0LjAiRQ!5e0!3m2!1sar!2sdz!4v1234567890"
                width="100%"
                height="400"
                style="border:0;"
                allowfullscreen=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
                class="map-iframe"
              ></iframe>
            </div>
          </v-card>
        </v-col>
        
        <v-col cols="12" lg="4">
          <v-card class="contact-info-card h-100" elevation="4">
            <v-card-title class="text-h5 font-weight-bold mb-4">
              <v-icon color="primary" class="mr-2">mdi-information</v-icon>
              معلومات التواصل
            </v-card-title>
            
            <v-card-text>
              <!-- Address -->
              <div class="contact-item mb-4">
                <div class="d-flex align-start">
                  <v-icon color="primary" class="me-3 mt-1">mdi-map-marker-radius</v-icon>
                  <div>
                    <h3 class="text-h6 font-weight-medium mb-1">العنوان</h3>
                    <p class="text-body-2 text-medium-emphasis">
                      شارع الأمير عبد القادر، الجزائر العاصمة<br>
                      بجوار مسجد العاشور
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- Phone -->
              <div class="contact-item mb-4">
                <div class="d-flex align-start">
                  <v-icon color="primary" class="me-3 mt-1">mdi-phone</v-icon>
                  <div>
                    <h3 class="text-h6 font-weight-medium mb-1">الهاتف</h3>
                    <p class="text-body-2 text-medium-emphasis mb-1">
                      +213 21 23 45 67
                    </p>
                    <p class="text-body-2 text-medium-emphasis">
                      +213 66 314 0341
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- Email -->
              <div class="contact-item mb-4">
                <div class="d-flex align-start">
                  <v-icon color="primary" class="me-3 mt-1">mdi-email</v-icon>
                  <div>
                    <h3 class="text-h6 font-weight-medium mb-1">البريد الإلكتروني</h3>
                    <p class="text-body-2 text-medium-emphasis">
                      info@paclos-dz.com<br>
                      support@paclos-dz.com
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- Working Hours -->
              <div class="contact-item">
                <div class="d-flex align-start">
                  <v-icon color="primary" class="me-3 mt-1">mdi-clock</v-icon>
                  <div>
                    <h3 class="text-h6 font-weight-medium mb-1">ساعات العمل</h3>
                    <p class="text-body-2 text-medium-emphasis">
                      من الأحد إلى الخميس: 9:00 - 18:00<br>
                      الجمعة والسبت: 9:00 - 14:00
                    </p>
                  </div>
                </div>
              </div>
            </v-card-text>
            
            <v-card-actions class="pa-4">
              <v-btn
                color="primary"
                variant="elevated"
                prepend-icon="mdi-directions"
                block
                @click="openDirections"
              >
                احصل على الاتجاهات
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
      
      <!-- Quick Contact Form -->
      <v-row class="mt-8">
        <v-col cols="12">
          <v-card class="quick-contact-card" elevation="4">
            <v-card-title class="text-h5 font-weight-bold mb-4">
              <v-icon color="primary" class="mr-2">mdi-message-text</v-icon>
              تواصل معنا بسرعة
            </v-card-title>
            
            <v-card-text>
              <v-row>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="quickForm.name"
                    label="الاسم الكامل"
                    variant="outlined"
                    prepend-inner-icon="mdi-account"
                    required
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <v-text-field
                    v-model="quickForm.phone"
                    label="رقم الهاتف"
                    variant="outlined"
                    prepend-inner-icon="mdi-phone"
                    type="tel"
                    required
                  />
                </v-col>
                <v-col cols="12" md="4">
                  <v-btn
                    color="primary"
                    variant="elevated"
                    size="large"
                    prepend-icon="mdi-send"
                    block
                    @click="sendQuickMessage"
                    :loading="sending"
                  >
                    إرسال رسالة
                  </v-btn>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue';

// Quick form state
const quickForm = reactive({
  name: '',
  phone: ''
});

const sending = ref(false);

// Methods
const openDirections = () => {
  const address = 'شارع الأمير عبد القادر، الجزائر العاصمة';
  const encodedAddress = encodeURIComponent(address);
  window.open(`https://www.google.com/maps/dir/?api=1&destination=${encodedAddress}`, '_blank');
};

const sendQuickMessage = async () => {
  if (!quickForm.name || !quickForm.phone) {
    return;
  }
  
  sending.value = true;
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Reset form
    quickForm.name = '';
    quickForm.phone = '';
    
    // Show success message (you can use a snackbar here)
    console.log('Message sent successfully');
  } catch (error) {
    console.error('Error sending message:', error);
  } finally {
    sending.value = false;
  }
};
</script>

<style scoped>
.google-map-section {
  background: linear-gradient(135deg, rgba(10, 10, 18, 0.95), rgba(212, 175, 55, 0.05));
}

.map-container {
  overflow: hidden;
}

.map-wrapper {
  position: relative;
  width: 100%;
  height: 400px;
}

.map-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.contact-info-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

.contact-item {
  transition: transform 0.3s ease;
}

.contact-item:hover {
  transform: translateX(5px);
}

.quick-contact-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(5px);
}

@media (max-width: 960px) {
  .map-wrapper {
    height: 300px;
  }
}
</style>
