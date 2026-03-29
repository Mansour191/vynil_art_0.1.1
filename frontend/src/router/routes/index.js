// src/router/routes/index.js

import PublicRoutes from './public';
import DashboardRoutes from './dashboard';
import AuthRoutes from './auth';
import CategoryRoutes from './categories';
import InvestorRoutes from './investor';
import CustomerRoutes from './customer';

// دمج جميع المسارات
const routes = [
  ...PublicRoutes,
  ...AuthRoutes,
  ...DashboardRoutes,
  ...CategoryRoutes,
  ...InvestorRoutes,
  ...CustomerRoutes
];

console.log('📊 المسارات المحملة:', routes);

export default routes;
