import Home from '@/home'
import Login from '@/components/login/login'
import Index from '@/components/index/index'
import IndexMajor from '@/components/index/indexMajor'
import indexStudents from '@/components/index/indexStudents'
import person from '@/components/index/personal'
import officeDataExpore from '@/components/office/officeDataExpore'
import officeSuggestions from '@/components/office/officeSuggestions'
import dataFilter from '@/components/office/dataFilter'
import systemUserTeam from '@/components/system/systemUserTeam'
import systemRoleTeam from '@/components/system/systemRoleTeam'
import systemUsers from '@/components/system/systemUsers'
import dataUpdateBasic from '@/components/data/dataUpdateBasic'
import dataUpdateScore from '@/components/data/dataUpdateScore'
import dataUpdateFocus from '@/components/data/dataUpdateFocus'


import store from '@/vuex/store'

let routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/login',
    name: '',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {requiresAuth: true},
    children: [
            { path: '/home', component: Index, name: store['index'], meta: { requiresAuth: true } },
            { path: '/indexMajor', component: IndexMajor, name: store['indexMajor'], meta: { requiresAuth: true } },
            { path: '/indexStudents', component: indexStudents, name: store['indexStudents'], meta: { requiresAuth: true } },
            { path: '/person', component: person, name: store['person'], meta: { requiresAuth: true } },
            { path: '/officeDataExpore', component: officeDataExpore, name: store['officeDataExpore'], meta: { requiresAuth: true } },
            { path: '/systemUserTeam', component: systemUserTeam, name: store['systemUserTeam'], meta: { requiresAuth: true } },
            { path: '/systemRoleTeam', component: systemRoleTeam, name: store['systemRoleTeam'], meta: { requiresAuth: true } },
            { path: '/systemUsers', component: systemUsers, name: store['systemUsers'], meta: { requiresAuth: true } },
            { path: '/officeSuggestions', component: officeSuggestions, name: store['officeSuggestions'], meta: { requiresAuth: true } },
            { path: '/dataUpdateBasic', component: dataUpdateBasic, name: store['dataUpdateBasic'], meta: { requiresAuth: true } },
            { path: '/dataUpdateScore', component: dataUpdateScore, name: store['dataUpdateScore'], meta: { requiresAuth: true } },
            { path: '/dataFilter', component: dataFilter, name: store['dataFilter'], meta: { requiresAuth: true } },
            { path: '/dataUpdateFocus', component: dataUpdateFocus, name: store['dataUpdateFocus'], meta: { requiresAuth: true } }
        ]
  }
]

export default routes;
