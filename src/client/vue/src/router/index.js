import Vue from 'vue';
import Router from 'vue-router';
import Ping from '@/components/Ping';
import Schueler from '@/components/Schueler';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Schueler',
      component: Schueler,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
  ],
  mode: 'hash',
});
