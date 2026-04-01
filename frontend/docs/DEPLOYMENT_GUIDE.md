# 🚀 دليل النقل والنشر اليدوي

## 📋 نظرة عامة

هذا الدليل يشرح كيفية نقل المشروع يدوياً وتجنب المشاكل الشائعة أثناء النشر.

---

## 📁 هيكل المجلدات المطلوب

```
frontend/
├── docs/                    # 📚 ملفات التوثيق الجديدة
│   ├── API_INTEGRATION_REPORT.md
│   └── DEPLOYMENT_GUIDE.md
├── src/                      # 📦 شفرة المصدر
│   ├── views/                 # 📄 ملفات الواجهات
│   ├── components/             # 🧩 المكونات
│   ├── assets/                # 🖼️ الموارد الثابتة
│   └── ...
├── public/                   # 🌐 الملفات العامة
├── package.json              # 📦 إعدادات المشروع
├── vite.config.js           # ⚙️ إعدادات Vite
└── .env.example             # 🔐 متغيرات البيئة
```

---

## 🔄 خطوات النقل اليدوي

### 1️⃣ التحقق من الملفات المهمة

**الملفات التي يجب التأكد من وجودها:**

```bash
# الملفات الأساسية
✓ package.json
✓ vite.config.js
✓ index.html
✓ .env.example

# مجلدات المصدر
✓ src/
✓ src/main.js
✓ src/App.vue
✓ src/views/

# مجلد الموارد
✓ public/
✓ src/assets/

# ملفات التوثيق الجديدة
✓ docs/API_INTEGRATION_REPORT.md
✓ docs/DEPLOYMENT_GUIDE.md
```

### 2️⃣ نسخ الملفات

**الطريقة الآمنة للنسخ:**

```bash
# 1. إنشاء نسخة احتياطية
cp -r /path/to/current/frontend /path/to/backup/frontend-$(date +%Y%m%d)

# 2. نسخ الملفات الجديدة
cp -r /path/to/new/frontend/* /path/to/current/frontend/

# 3. التحقق من الصلاحيات
chmod -R 755 /path/to/current/frontend/
chown -R www-data:www-data /path/to/current/frontend/
```

### 3️⃣ إعدادات البيئة

**إنشاء ملف .env:**

```bash
# نسخ الملف النموذجي
cp .env.example .env

# تعديل المتغيرات
nano .env
```

**المتغيرات المطلوبة:**
```env
VITE_API_BASE_URL=https://your-api-domain.com/api
VITE_APP_NAME=VynilArt
VITE_APP_VERSION=1.0.0
VITE_ENABLE_ANALYTICS=true
```

---

## 🛠️ التثبيت والإعداد

### 1️⃣ تثبيت الاعتماديات

```bash
# تثبيت الحزم
npm install

# أو باستخدام yarn
yarn install

# أو باستخدام pnpm
pnpm install
```

### 2️⃣ التحقق من الإصدارات

**الإصدارات الموصى بها:**
```json
{
  "vue": "^3.4.0",
  "vuetify": "^3.4.0",
  "vite": "^5.0.0",
  "@apollo/client": "^3.8.0"
}
```

### 3️⃣ بناء المشروع

```bash
# بناء للإنتاج
npm run build

# أو
yarn build

# أو
pnpm build
```

---

## 🔧 حل المشاكل الشائعة

### ❌ مشكلة: "Module not found"

**الحل:**
```bash
# حذف node_modules وإعادة التثبيت
rm -rf node_modules package-lock.json
npm install
```

### ❌ مشكلة: "Failed to load resource"

**الحل:**
```bash
# التحقق من مسارات الموارد
ls -la public/
ls -la dist/

# التأكد من وجود index.html
ls -la dist/index.html
```

### ❌ مشكلة: "CORS error"

**الحل:**
```javascript
// في vite.config.js
export default {
  server: {
    cors: true
  },
  build: {
    outDir: 'dist'
  }
}
```

### ❌ مشكلة: "API connection failed"

**الحل:**
```bash
# التحقق من متغيرات البيئة
cat .env

# اختبار الاتصال بالـ API
curl -X GET "$VITE_API_BASE_URL/health"
```

---

## 🚀 النشر

### 1️⃣ النشر المحلي

```bash
# تشغيل خادم التطوير
npm run dev

# تشغيل على منفذ مختلف
npm run dev -- --port 3001
```

### 2️⃣ النشر على الخادم

**باستخدام Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /path/to/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**باستخدام Apache:**
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /path/to/frontend/dist
    
    <Directory /path/to/frontend/dist>
        AllowOverride All
        Require all granted
    </Directory>
    
    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule . /index.html [L]
</VirtualHost>
```

---

## ✅ قائمة التحقق قبل النشر

### 🔍 التحقق من الملفات
- [ ] جميع ملفات Vue موجودة وصالحة
- [ ] ملفات الإعدادات موجودة
- [ ] مجلد docs منسوخ
- [ ] متغيرات البيئة معدة

### 🧪 الاختبار
- [ ] التطبيق يعمل محلياً
- [ ] اتصال الـ API يعمل
- [ ] جميع الصفحات تفتح بدون أخطاء
- [ ] الروابط الداخلية تعمل

### 📊 الأداء
- [ ] وقت التحميل مقبول
- [ ] حجم الملفات محسن
- [ ] الصور والـ assets محسّنة
- [ ] الـ cache يعمل

---

## 🔄 الصيانة

### تحديث المشروع

```bash
# 1. أخذ نسخة احتياطية
cp -r /path/to/current/frontend /backup/frontend-$(date +%Y%m%d)

# 2. سحب التحديثات
git pull origin main

# 3. تحديث الاعتماديات
npm install

# 4. إعادة البناء
npm run build

# 5. إعادة تشغيل الخدمات
systemctl restart nginx
```

### المراقبة

```bash
# مراقبة سجلات الأخطاء
tail -f /var/log/nginx/error.log

# مراقبة أداء الخادم
htop
df -h
free -m
```

---

## 📞 الدعم الفني

### 🆘 المشاكل الشائعة والحلول

| المشكلة | الحل | الرابط |
|---------|------|-------|
| 404 Not Found | التحقق من مسارات Vue Router | [Vue Router](https://router.vuejs.org/) |
| CORS Error | إعدادات الخادم | [CORS Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) |
| Slow Loading | تحسين الأداء | [Vue Performance](https://vuejs.org/guide/best-practices/performance.html) |
| API Errors | التحقق من endpoints | [API Documentation](./API_INTEGRATION_REPORT.md) |

### 📚 موارد إضافية

- [Vue.js Documentation](https://vuejs.org/)
- [Vuetify Documentation](https://vuetifyjs.com/)
- [Vite Documentation](https://vitejs.dev/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

## 📝️ ملاحظات هامة

### ⚠️ تحذيرات
1. **دائماً أخذ نسخة احتياطية** قبل أي تحديث
2. **اختبار التغييرات** على بيئة التطوير أولاً
3. **مراجعة السجلات** بعد كل عملية نشر
4. **تحديث الصلاحيات** بعد نسخ الملفات

### 💡 نصائح
1. استخدام **Git** لإدارة الإصدارات
2. تفعيل **HTTPS** في الإنتاج
3. إعداد **CDN** للملفات الثابتة
4. مراقبة **الأداء** بانتظام

---

**تاريخ التحديث**: 1 أبريل 2026  
**الإصدار**: v1.0.0  
**الحالة**: جاهز للاستخدام
