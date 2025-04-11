import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';

export const canActivateAuth: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  const token = auth.getAccessToken();
  if (!token) {
    router.navigate(['/login']);
    return false;
  }

  return true;
};
