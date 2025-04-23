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
    path: 'loginHouse',
    loadComponent: () => import('./auth/login-to-house/login-to-house.component').then(m => m.LoginToHouseComponent),
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
    path: 'profile',
    loadComponent: () => import('./profile/profile.component').then(m => m.ProfileComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: 'profile/changePassword',
    loadComponent: () => import('./profile/change-password/change-password.component').then(m => m.ChangePasswordComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: 'house/dashboard',
    loadComponent: () => import('./house-dashboard/house-dashboard.component').then(m => m.HouseDashboardComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: 'house/room/dashboard',
    loadComponent: () => import('./room-dashboard/room-dashboard.component').then(m => m.RoomDashboardComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: 'house/info',
    loadComponent: () => import('./house-info/house-info.component').then((m) => m.HouseInfoComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: 'house/changePin',
    loadComponent: () => import('./house-info/change-pin/change-pin.component').then(m => m.ChangeHousePinComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: 'house/manageUsers',
    loadComponent: () =>
      import('./manage-users/manage-users.component').then(m => m.ManageUsersComponent),
    canActivate: [canActivateAuth]
  },
  {
    path: '**',
    redirectTo: ''
  }
];
