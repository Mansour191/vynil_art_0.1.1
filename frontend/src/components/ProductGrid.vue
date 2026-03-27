<template>
  <div class="product-grid-wrapper">
    <!-- Products Grid -->
    <v-row>
      <v-col
        v-for="product in products"
        :key="product.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
        class="mb-4"
      >
        <v-card class="product-card h-100" elevation="4" hover>
          <v-img
            :src="product.image"
            :alt="product.name"
            height="200"
            cover
            class="product-image"
          >
            <template v-slot:placeholder>
              <v-row class="fill-height" align="center" justify="center">
                <v-progress-circular indeterminate color="primary"></v-progress-circular>
              </v-row>
            </template>
          </v-img>
          
          <v-card-text class="pa-4">
            <v-card-title class="text-h6 mb-2">{{ product.name }}</v-card-title>
            
            <v-card-subtitle class="text-h5 font-weight-bold text-primary mb-3">
              {{ product.price }} ر.س
            </v-card-subtitle>
            
            <v-card-actions class="d-flex justify-space-between">
              <v-btn
                variant="outlined"
                color="primary"
                prepend-icon="mdi-eye"
                size="small"
              >
                معاينة
              </v-btn>
              
              <v-btn
                color="primary"
                prepend-icon="mdi-cart-plus"
                size="small"
              >
                إضافة للسلة
              </v-btn>
            </v-card-actions>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Empty State -->
    <v-row v-if="!products || products.length === 0" justify="center" class="py-8">
      <v-col cols="12" class="text-center">
        <v-icon size="64" color="primary" class="mb-4">mdi-package-variant-closed</v-icon>
        <h3 class="text-h5 font-weight-medium mb-2">لا توجد منتجات</h3>
        <p class="text-body-2 text-medium-emphasis">لم يتم العثور على منتجات متاحة حالياً</p>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
defineProps({
  products: {
    type: Array,
    default: () => []
  }
});
</script>
              

  
