# دليل التطوير - فينيل آرت (Vinyl Art)

هذا المشروع هو واجهة أمامية متقدمة لمتجر فينيل آرت، مبني باستخدام Vue.js ومتكامل مع ERPNext.

## 🛠️ المتطلبات المسبقة
- Node.js (v14+)
- npm أو yarn

## 🚀 التثبيت
1. قم بتثبيت التبعيات:
   ```bash
   npm install
   ```
2. قم بإنشاء ملف `.env` بناءً على `.env.example`:
   ```bash
   cp .env.example .env
   ```
3. قم بتكوين مفاتيح API الخاصة بـ ERPNext و EmailJS في ملف `.env`.

## ⚙️ التكوين (Configuration)

### ERPNext
تأكد من تفعيل API في ERPNext وإنشاء مفتاح API وسر API للمستخدم المعني.
```env
VUE_APP_ERPNEXT_URL=https://your-erpnext-site.com
VUE_APP_ERPNEXT_API_KEY=your_api_key
VUE_APP_ERPNEXT_API_SECRET=your_api_secret
```

### EmailJS
مشروعنا يستخدم EmailJS لإرسال الإشعارات والبريد الإلكتروني من المتصفح مباشرة.
```env
VUE_APP_EMAILJS_SERVICE_ID=your_service_id
VUE_APP_EMAILJS_TEMPLATE_ID=your_template_id
VUE_APP_EMAILJS_USER_ID=your_user_id
```

## 🏗️ هيكل المشروع
- `src/views/`: المكونات الرئيسية للصفحات.
- `src/integration/services/`: خدمات الاتصال بالخلفية (ERPNext, Email, Alerts).
- `src/locales/`: ملفات الترجمة (العربية، الإنجليزية، الفرنسية).
- `src/router/`: نظام المسارات (يدعم التحميل المتأخر Lazy Loading).

## 🧪 الاختبارات
لتشغيل الفحص اللغوي (Linting):
```bash
npm run lint
```

## 📦 بناء المشروع للإنتاج
```bash
npm run build
```

## 🔒 الأمان والأداء
- **الأداء:** يتم استخدام Caching للبيانات في `ERPNextService` لتقليل طلبات الشبكة.
- **الأمان:** يتم الهروب من جميع المدخلات تلقائياً بواسطة Vue، وتم إضافة هيكلية لربط التوكنات الأمنية في المستقبل.
