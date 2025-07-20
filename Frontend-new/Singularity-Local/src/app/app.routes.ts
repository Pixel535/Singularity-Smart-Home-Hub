import { Routes } from '@angular/router';
import { canActivateGuest } from './auth/auth.guest.guard';
import { canActivateAuth } from './auth/auth.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./auth/redirect.component').then(m => m.RedirectComponent)
  },
  {
    path: 'initialization',
    loadComponent: () => import('./initialization/initialization.component').then(m => m.InitializationComponent),
    canActivate: [canActivateGuest]
  },
  {
    path: 'loginHouse',
    loadComponent: () => import('./auth/login-to-house/login-to-house.component').then(m => m.LoginToHouseComponent),
    canActivate: [canActivateGuest]
  },
  {
    path: 'house/dashboard',
    loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: 'house/room/dashboard',
    loadComponent: () => import('./room-dashboard/room-dashboard.component').then(m => m.RoomDashboardComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: '**',
    redirectTo: ''
  }
];
