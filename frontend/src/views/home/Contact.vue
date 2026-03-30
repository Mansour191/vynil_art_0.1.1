<template>
  <v-container class="py-8">
    <!-- Page Title -->
    <div class="text-center mb-8">
      <h1 class="text-h2 font-weight-bold text-warning d-flex align-center justify-center gap-4">
        <v-icon size="48" color="warning">mdi-headset</v-icon>
        {{ $t('contactPageTitle') }}
      </h1>
    </div>

    <!-- Welcome Message -->
    <v-card elevation="4" class="intro-box mb-8" color="surface">
      <v-card-text class="pa-6 text-center">
        <p class="text-h6 text-medium-emphasis">{{ $t('contactIntroText') }}</p>
      </v-card-text>
    </v-card>

    <!-- Contact Cards -->
    <v-row class="mb-8">
      <!-- Email -->
      <v-col cols="12" sm="6" md="4">
        <v-card elevation="4" class="contact-card text-center h-100" hover>
          <v-card-text class="pa-6">
            <div class="contact-icon-wrapper mb-4">
              <v-icon size="48" color="warning">mdi-email</v-icon>
            </div>
            <h3 class="text-h5 font-weight-bold text-warning mb-2">{{ $t('contactEmailTitle') }}</h3>
            <div class="text-body-2 text-medium-emphasis mb-2">{{ $t('contactEmailLabel') }}</div>
            <div class="contact-value">
              <v-btn
                href="mailto:remadnamansour7@gmail.com"
                variant="text"
                color="warning"
                prepend-icon="mdi-email"
                class="text-none"
              >
                remadnamansour7@gmail.com
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- Phone -->
      <v-col cols="12" sm="6" md="4">
        <v-card elevation="4" class="contact-card text-center h-100" hover>
          <v-card-text class="pa-6">
            <div class="contact-icon-wrapper mb-4">
              <v-icon size="48" color="warning">mdi-phone</v-icon>
            </div>
            <h3 class="text-h5 font-weight-bold text-warning mb-2">{{ $t('contactPhoneTitle') }}</h3>
            <div class="text-body-2 text-medium-emphasis mb-2">{{ $t('contactPhoneLabel') }}</div>
            <div class="contact-value">
              <v-btn
                href="tel:0663140341"
                variant="text"
                color="warning"
                prepend-icon="mdi-phone"
                class="text-none"
              >
                0663140341
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <!-- WhatsApp -->
      <v-col cols="12" sm="6" md="4">
        <v-card elevation="4" class="contact-card text-center h-100" hover>
          <v-card-text class="pa-6">
            <div class="contact-icon-wrapper mb-4">
              <v-icon size="48" color="warning">mdi-whatsapp</v-icon>
            </div>
            <h3 class="text-h5 font-weight-bold text-warning mb-2">{{ $t('contactWhatsappTitle') }}</h3>
            <div class="text-body-2 text-medium-emphasis mb-2">{{ $t('contactWhatsappLabel') }}</div>
            <div class="contact-value">
              <v-btn
                href="https://wa.me/213663140341"
                target="_blank"
                variant="text"
                color="success"
                prepend-icon="mdi-whatsapp"
                class="text-none"
              >
                0663140341
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Facebook Card -->
    <v-card elevation="6" class="facebook-card mb-8" color="blue-darken-4">
      <v-card-text class="pa-8">
        <div class="d-flex align-center justify-space-between flex-wrap gap-4">
          <div class="facebook-content">
            <div class="d-flex align-center gap-4 mb-4">
              <div class="facebook-icon-wrapper">
                <v-icon size="48" color="white">mdi-facebook</v-icon>
              </div>
              <div>
                <h3 class="text-h5 font-weight-bold text-white mb-2">{{ $t('contactFacebookTitle') }}</h3>
                <p class="text-body-2 text-white opacity-90">{{ $t('contactFacebookText') }}</p>
              </div>
            </div>
          </div>
          <v-btn
            href="https://www.facebook.com/profile.php?id=61588391030740"
            target="_blank"
            variant="elevated"
            color="white"
            prepend-icon="mdi-facebook"
            class="text-none"
          >
            {{ $t('contactFacebookButton') }}
          </v-btn>
        </div>
      </v-card-text>
    </v-card>

    <!-- Footer Message -->
    <v-card elevation="4" class="footer-box" color="surface">
      <v-card-text class="pa-6 text-center">
        <p class="text-h6 text-medium-emphasis d-flex align-center justify-center gap-2">
          <v-icon color="error">mdi-heart</v-icon>
          {{ $t('contactFooterText') }}
          <v-icon color="error">mdi-heart</v-icon>
        </p>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'ContactView',
};
</script>

<style scoped>
/* Vuetify handles most styling, only custom animations needed */
.contact-icon-wrapper:hover {
  transform: scale(1.1) rotate(360deg);
  transition: transform 0.6s ease;
}

.contact-icon-wrapper,
.facebook-icon-wrapper {
  transition: transform 0.6s ease;
  will-change: transform;
}

.v-card--hover {
  transition: all 0.3s ease;
  will-change: transform, box-shadow;
}
</style>
