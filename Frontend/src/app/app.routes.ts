import { Routes } from '@angular/router';
import { canActivateAuth } from './auth/auth.guard';
import { canActivateGuest } from './auth/auth.guest.guard';
import { RedirectComponent } from './auth/redirect.component';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./auth/redirect.component').then(m => m.RedirectComponent)
  },
  {
    path: 'login',
    loadComponent: () => import('./auth/login/login.component').then(m => m.LoginComponent),
    canActivate: [canActivateGuest]
  },
  {
    path: 'register',
    loadComponent: () => import('./auth/register/register.component').then(m => m.RegisterComponent),
    canActivate: [canActivateGuest]
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: '**',
    redirectTo: ''
  }
];
