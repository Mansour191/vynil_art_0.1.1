<template>
  <v-card class="royal-table-card elevation-4 rounded-xl overflow-hidden">
    <v-toolbar flat class="bg-gradient-royal px-4" height="80">
      <v-toolbar-title class="text-h6 font-weight-bold royal-text-dark">
        {{ title }}
      </v-toolbar-title>
      
      <v-spacer></v-spacer>

      <v-text-field
        v-model="search"
        prepend-inner-icon="mdi-magnify"
        label="بحث سريع..."
        variant="solo"
        hide-details
        rounded="lg"
        class="search-field hidden-sm-and-down"
        density="compact"
      ></v-text-field>

      <v-btn icon="mdi-filter-variant" variant="text" class="ms-2"></v-btn>
      <v-btn icon="mdi-export-variant" variant="text"></v-btn>
    </v-toolbar>

    <v-data-table
      :headers="headers"
      :items="data"
      :search="search"
      :loading="loading"
      :items-per-page="rows"
      class="royal-table"
      hover
    >
      <template v-slot:loading>
        <v-skeleton-loader type="table-row-divider@5"></v-skeleton-loader>
      </template>

      <template v-slot:item="{ item }">
        <tr class="royal-row">
          <td v-for="header in headers" :key="header.key" class="py-4">
            <slot :name="'item-' + header.key" :item="item">
              <span class="text-body-2 font-weight-medium text-marble-700">
                {{ item[header.key] }}
              </span>
            </slot>
          </td>
        </tr>
      </template>

      <template v-slot:bottom>
        <div class="d-flex align-center justify-space-between pa-4 bg-gradient-royal-light border-t">
          <span class="text-caption text-grey-darken-1">
            إجمالي السجلات: {{ data.length }}
          </span>
          <v-pagination
            v-model="page"
            :length="Math.ceil(data.length / rows)"
            active-color="primary"
            density="comfortable"
            variant="flat"
            rounded="lg"
          ></v-pagination>
        </div>
      </template>
    </v-data-table>
  </v-card>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  title: { type: String, default: 'جدول البيانات الملكي' },
  data: { type: Array, required: true },
  headers: { type: Array, required: true },
  loading: { type: Boolean, default: false },
  rows: { type: Number, default: 10 }
});

const search = ref('');
const page = ref(1);
</script>

<style scoped>
/* التدرج الملكي الخاص بـ Paclos */
.bg-gradient-royal {
  background: linear-gradient(90deg, #f8f9fa 0%, #eef2f3 100%) !important;
  border-bottom: 1px solid rgba(212, 175, 55, 0.2);
}

.bg-gradient-royal-light {
  background: linear-gradient(90deg, #ffffff 0%, #f8f9fa 100%);
}

.royal-table-card {
  border: 1px solid rgba(212, 175, 55, 0.15);
}

.royal-text-dark {
  color: #1a1a2e;
  letter-spacing: 0.5px;
}

.search-field {
  max-width: 300px;
}

/* تحسين شكل الجدول */
:deep(.v-data-table-header) {
  background-color: #f1f4f8 !important;
}

:deep(.v-data-table-header th) {
  font-weight: 700 !important;
  text-transform: uppercase;
  font-size: 0.75rem !important;
  color: #5c5c70 !important;
  letter-spacing: 1px;
}

.royal-row:hover {
  background-color: rgba(212, 175, 55, 0.03) !important;
  transition: background-color 0.2s ease;
}

.text-marble-700 {
  color: #4a4a68;
}

.border-t {
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}
</style>
