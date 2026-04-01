# 🔧 دليل حل المشاكل

## 📋 مقدمة

هذا الدليل يحتوي على حلول للمشاكل الشائعة التي قد تواجهها أثناء نقل المشروع أو تشغيله.

---

## 🚨 المشاكل الشائعة والحلول

### 1️⃣ مشاكل التثبيت

#### ❌ "npm install fails"
**الأعراض:**
```
npm ERR! code ENOENT
npm ERR! errno -2
npm ERR! syscall open
```

**الحلول:**
```bash
# 1. تنظيف التثبيت الحالي
npm cache clean --force

# 2. حذف node_modules
rm -rf node_modules package-lock.json

# 3. إعادة التثبيت
npm install

# أو استخدام yarn
yarn install
```

#### ❌ "Permission denied"
**الأعراض:**
```
npm ERR! code EACCES
npm ERR! syscall mkdir
```

**الحلول:**
```bash
# 1. تغيير الصلاحيات
sudo chown -R $(whoami) node_modules

# 2. استخدام nvm
nvm use node
npm install
```

---

### 2️⃣ مشاكل البناء

#### ❌ "Build failed"
**الأعراض:**
```
[vite] Build failed with errors
Error: RollupError: Unexpected token
```

**الحلول:**
```bash
# 1. التحقق من صياغة Vue
npm run lint

# 2. تنظيف البناء
rm -rf dist

# 3. إعادة البناء
npm run build

# 4. التحقق من إصدارات Node
node --version  # يجب أن يكون >= 18
npm --version   # يجب أن يكون >= 9
```

#### ❌ "Memory limit exceeded"
**الأعراض:**
```
FATAL ERROR: Ineffective mark-compacts near heap limit Allocation failed
```

**الحلول:**
```bash
# 1. زيادة الذاكرة
export NODE_OPTIONS="--max-old-space-size=4096"

# 2. بناء تدريجي
npm run build --mode=development
```

---

### 3️⃣ مشاكل التشغيل

#### ❌ "Port already in use"
**الأعراض:**
```
Error: listen EADDRINUSE :::3000
```

**الحلول:**
```bash
# 1. البحث عن العملية
lsof -i :3000

# 2. قتل العملية
kill -9 $(lsof -t -i:3000)

# 3. استخدام منفذ آخر
npm run dev -- --port 3001
```

#### ❌ "Cannot find module"
**الأعراض:**
```
Module not found: Error: Can't resolve 'vue'
```

**الحلول:**
```bash
# 1. إعادة تثبيت الاعتماديات
npm install

# 2. التحقق من package.json
cat package.json | grep vue

# 3. تنظيف Webpack Cache
rm -rf .vite
```

---

### 4️⃣ مشاكل الـ API

#### ❌ "Network Error"
**الأعراض:**
```
Network Error: fetch failed
CORS policy: No 'Access-Control-Allow-Origin'
```

**الحلول:**
```bash
# 1. التحقق من اتصال الشبكة
ping your-api-domain.com

# 2. التحقق من الـ API
curl -X GET "http://localhost:8000/api/health"

# 3. التحقق من CORS
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     http://localhost:8000/api/health
```

#### ❌ "404 Not Found"
**الأعراض:**
```
GET /api/users 404 (Not Found)
```

**الحلول:**
```bash
# 1. التحقق من مسارات الـ API
cat src/api/services/*.js | grep "fetch"

# 2. التحقق من الخادم الخلفي
ps aux | grep python

# 3. التحقق من إعدادات Proxy
cat vite.config.js | grep -A 5 proxy
```

---

### 5️⃣ مشاكل الواجهة

#### ❌ "Blank page"
**الأعراض:**
- صفحة بيضاء تماماً
- لا تظهر رسائل خطأ

**الحلول:**
```bash
# 1. فتح أدوات المطور
F12 -> Console

# 2. التحقق من أخطاء JavaScript
# 3. التحقق من سجلات الشبكة
# 4. التحقق من مصادر الصفحة

# 5. التحقق من Vue DevTools
# تثبيت Vue DevTools extension
```

#### ❌ "Styles not loading"
**الأعراض:**
- التصميم CSS لا يظهر
- الألوان خاطئة

**الحلول:**
```bash
# 1. التحقق من ملفات CSS
ls -la src/assets/css/

# 2. التحقق من Vuetify
npm list vuetify

# 3. تنظيف Cache
rm -rf node_modules/.cache
```

---

## 🔧 أدوات التشخيص

### 1️⃣ أدوات سطر الأوامر

```bash
# التحقق من إصدارات Node
node --version && npm --version

# التحقق من مساحة القرص
df -h

# التحقق من استخدام الذاكرة
free -h

# التحقق من العمليات
ps aux | grep node

# التحقق من المنافذ
netstat -tulpn | grep :3000
```

### 2️⃣ أدوات المتصفح

```javascript
// في Console
console.log('Vue version:', Vue.version);
console.log('Vuetify version:', Vuetify.version);
console.log('Environment:', import.meta.env.MODE);

// التحقق من الـ API
fetch('/api/health')
  .then(r => r.json())
  .then(d => console.log('API Status:', d));
```

### 3️⃣ أدوات Vue

```javascript
// في Vue DevTools
// التحقق من Component
this.$options.name

// التحقق من Store
this.$store.state

// التحقق من Router
this.$route
```

---

## 📊 المراقبة والتشخيص

### 1️⃣ مراقبة الأداء

```bash
# مراقبة استخدام الذاكرة
watch -n 1 'free -h | grep Mem'

# مراقبة استخدام المعالج
top -p $(pgrep node)

# مراقبة الشبكة
iftop -i
```

### 2️⃣ مراقبة الأخطاء

```bash
# مراقبة سجلات Nginx
tail -f /var/log/nginx/error.log

# مراقبة سجلات Node
tail -f /var/log/nodejs/app.log

# مراقبة سجلات النظام
journalctl -u nodejs -f
```

---

## 🚀 الإصلاحات السريعة

### 1️⃣ إعادة تعيين البيئة

```bash
# إعادة تعيين Node
source ~/.bashrc

# إعادة تعيين npm
npm config delete prefix
npm config set prefix ~/.npm-global
```

### 2️⃣ تنظيف المشروع

```bash
# تنظيف كامل
rm -rf node_modules dist .vite package-lock.json
npm install
npm run build
```

### 3️⃣ إعادة تشغيل الخدمات

```bash
# إعادة تشغيل Nginx
sudo systemctl restart nginx

# إعادة تشغيل Node
sudo systemctl restart nodejs

# التحقق من الحالة
sudo systemctl status nginx nodejs
```

---

## 📞 الحصول على المساعدة

### 🆘 متى تطلب المساعدة

1. **عند استمرار الخطأ** بعد محاولة كل الحلول
2. **عند عدم فهم الخطأ** أو رسالة الخطأ غير واضحة
3. **عند تأثير الأداء** على عمل المستخدمين
4. **عند حدوث المشكلة** في بيئة الإنتاج

### 📧 كيف تطلب المساعدة

1. **جمع المعلومات**:
   - نسخة الخطأ بالكامل
   - خطوات إعادة المشكلة
   - بيئة التشغيل (OS, Node, npm versions)
   - لقطات شاشة إذا أمكن

2. **التوثيق**:
   ```bash
   # جمع معلومات النظام
   uname -a > system-info.txt
   node --version >> system-info.txt
   npm --version >> system-info.txt
   
   # جمع معلومات المشروع
   cat package.json >> system-info.txt
   git log --oneline -5 >> system-info.txt
   ```

3. **إنشاء تقرير المشكلة**:
   ```markdown
   ## وصف المشكلة
   [وصف دقيق للمشكلة]
   
   ## الخطوات لإعادة المشكلة
   1. [الخطوة الأولى]
   2. [الخطوة الثانية]
   3. [الخطوة الثالثة]
   
   ## النتائج المتوقعة
   [ما كنت تتوقع أن يحدث]
   
   ## النتائج الفعلية
   [ما حدث فعلياً]
   
   ## معلومات النظام
   - OS: [نظام التشغيل]
   - Node: [إصدار Node]
   - npm: [إصدار npm]
   - Browser: [المتصفح وإصداره]
   ```

---

## 📚 موارد إضافية

### 🔗 روابط مفيدة

- [Vue.js Troubleshooting](https://vuejs.org/guide/scaling-up/troubleshooting.html)
- [Vite Troubleshooting](https://vitejs.dev/guide/troubleshooting.html)
- [Nginx Troubleshooting](https://nginx.org/en/docs/troubleshooting.html)
- [Node.js Debugging](https://nodejs.org/en/docs/guides/debugging-getting-started/)

### 🛠️ أدوات مفيدة

- **Vue DevTools**: لتصحيح أخطاء Vue
- **Postman**: لاختبار الـ API
- **Chrome DevTools**: لتصحيح أخطاء الويب
- **Wireshark**: لتحليل الشبكة

---

## 📝️ خلاصة

مع هذا الدليل، يجب أن تكون قادراً على:

- ✅ تشخيص المشاكل الشائعة بسرعة
- ✅ تطبيق الحلول المناسبة
- ✅ مراقبة أداء النظام
- ✅ طلب المساعدة بفعالية عند الحاجة

**تذكر**: معظم المشاكل لها حلول بسيطة، والصبر والممارسة هما مفتاح النجاح! 🚀

---

**تاريخ التحديث**: 1 أبريل 2026  
**الإصدار**: v1.0.0  
**الحالة**: جاهز للاستخدام
