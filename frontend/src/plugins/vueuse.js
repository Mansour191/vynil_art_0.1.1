import { MotionPlugin } from '@vueuse/motion';
import { autoAnimatePlugin } from '@formkit/auto-animate/vue'; // التأكد من المسار الصحيح للـ Vue plugin

export default {
    install: (app) => {
        app.use(MotionPlugin);
        app.use(autoAnimatePlugin);
    }
};