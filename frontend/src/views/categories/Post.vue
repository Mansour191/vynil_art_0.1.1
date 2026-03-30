<template>
  <v-main class="post-page">
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card class="post-card" elevation="4">
            <v-card-text class="pa-8">
              <h1 class="text-h3 font-weight-bold text-center mb-6 text-primary" v-ai-t>{{ post.title }}</h1>
              <div class="post-body" v-html="post.content" v-ai-t></div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const post = ref({
  id: 1,
  title: 'كيف تختار الفينيل المناسب لمشروعك؟',
  content: `
    <!-- Content omitted for brevity in search/replace, keep original content -->
    <div style="position:absolute; top:-9999px; left:-9999px; width:0; height:0; overflow:hidden;">
        <img src="https://i.postimg.cc/0QKmBBJ9/kitchen2.png" alt="صورة مصغرة للمقال"/>
    </div>

    <h2 class="text-h2 text-center text-primary mb-8">📘 دليل المبتدئين: كيف تختار الفينيل المناسب لمشروعك؟</h2>

    <div class="mb-8">
        <v-card class="pa-6" color="surface" elevation="4">
            <p class="text-body-1 text-center">
                ✨ إذا كنت جديداً في عالم الفينيل اللاصق، قد تشعر بالحيرة عند اختيار النوع المناسب لمشروعك. لا تقلق! هذا الدليل الشامل سيساعدك على فهم كل ما تحتاج معرفته.
            </p>
        </v-card>
    </div>

    <v-card class="pa-6 mb-8" elevation="2">
        <h3 class="text-h5 mb-4 text-primary">📌 في هذا الدليل:</h3>
        <v-row>
            <v-col cols="12" md="6">
                <v-list density="compact">
                    <v-list-item>
                        <template v-slot:prepend>
                            <v-icon color="primary">mdi-circle-small</v-icon>
                        </template>
                        <v-list-item-title>
                            <a href="#types" class="text-primary text-decoration-none">أنواع الفينيل المختلفة</a>
                        </v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                        <template v-slot:prepend>
                            <v-icon color="primary">mdi-circle-small</v-icon>
                        </template>
                        <v-list-item-title>
                            <a href="#finish" class="text-primary text-decoration-none">الفرق بين اللامع والمطفي</a>
                        </v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                        <template v-slot:prepend>
                            <v-icon color="primary">mdi-circle-small</v-icon>
                        </template>
                        <v-list-item-title>
                            <a href="#tips" class="text-primary text-decoration-none">نصائح الشراء</a>
                        </v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-col>
            <v-col cols="12" md="6">
                <v-list density="compact">
                    <v-list-item>
                        <template v-slot:prepend>
                            <v-icon color="primary">mdi-circle-small</v-icon>
                        </template>
                        <v-list-item-title>
                            <a href="#mistakes" class="text-primary text-decoration-none">أخطاء شائعة تجنبها</a>
                        </v-list-item-title>
                    </v-list-item>
                    <v-list-item>
                        <template v-slot:prepend>
                            <v-icon color="primary">mdi-circle-small</v-icon>
                        </template>
                        <v-list-item-title>
                            <a href="#faq" class="text-primary text-decoration-none">أسئلة وأجوبة</a>
                        </v-list-item-title>
                    </v-list-item>
                </v-list>
            </v-col>
        </v-row>
    </v-card>

    <div id="types" class="my-12">
        <h3 class="text-h4 mb-6 text-primary border-b pb-2">🔰 أنواع الفينيل حسب الاستخدام</h3>
        
        <v-row>
            <v-col cols="12" md="6">
                <v-card class="pa-6 h-100" elevation="2" hover>
                    <div class="text-h6 text-center mb-4">🪑</div>
                    <h4 class="text-h5 text-center mb-3 text-primary">فينيل الأثاث</h4>
                    <p class="text-body-1 mb-4">مصمم خصيصاً للأسطح الخشبية والمدهونة. يتميز بقوة التصاق عالية ومقاومة للخدوش. مثالي لتجديد الخزائن، الطاولات، والأدراج.</p>
                    <v-chip color="primary" variant="tonal" class="mb-2">
                        <v-icon start>mdi-check</v-icon>
                        مناسب لـ: الخشب، الـ MDF، الأسطح المدهونة
                    </v-chip>
                </v-card>
            </v-col>
            
            <v-col cols="12" md="6">
                <v-card class="pa-6 h-100" elevation="2" hover>
                    <div class="text-h6 text-center mb-4">🧱</div>
                    <h4 class="text-h5 text-center mb-3 text-primary">فينيل الجدران</h4>
                    <p class="text-body-1 mb-4">أخف وزناً وأسهل في الإزالة. مصمم للأسطح الملساء مثل الجدران المدهونة والزجاج. يأتي بتصاميم وألوان لا حصر لها.</p>
                    <v-chip color="primary" variant="tonal" class="mb-2">
                        <v-icon start>mdi-check</v-icon>
                        مناسب لـ: الجدران الملساء، الزجاج، المرايا
                    </v-chip>
                </v-card>
            </v-col>
            
            <v-col cols="12" md="6">
                <v-card class="pa-6 h-100" elevation="2" hover>
                    <div class="text-h6 text-center mb-4">🚗</div>
                    <h4 class="text-h5 text-center mb-3 text-primary">فينيل السيارات</h4>
                    <p class="text-body-1 mb-4">مقاوم للعوامل الجوية والحرارة. يتميز بمرونة عالية تسمح بتطبيقه على الأسطح المنحنية للسيارات والدراجات النارية.</p>
                    <v-chip color="primary" variant="tonal" class="mb-2">
                        <v-icon start>mdi-check</v-icon>
                        مناسب لـ: السيارات، الدراجات، الأسطح الخارجية
                    </v-chip>
                </v-card>
            </v-col>
            
            <v-col cols="12" md="6">
                <v-card class="pa-6 h-100" elevation="2" hover>
                    <div class="text-h6 text-center mb-4">🪟</div>
                    <h4 class="text-h5 text-center mb-3 text-primary">فينيل النوافذ</h4>
                    <p class="text-body-1 mb-4">شبه شفاف أو مزخرف، يستخدم للخصوصية مع السماح بدخول الضوء. مثالي للمكاتب والحمامات وأبواب الزجاج.</p>
                    <v-chip color="primary" variant="tonal" class="mb-2">
                        <v-icon start>mdi-check</v-icon>
                        مناسب لـ: النوافذ، الأبواب الزجاجية، الفواصل
                    </v-chip>
                </v-card>
            </v-col>
        </v-row>
    </div>
  `,
});

onMounted(() => {
  const postId = route.params.id;
  console.log('Loading post:', postId);
});
</script>

