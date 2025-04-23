import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { map, catchError, of } from 'rxjs';

export const canActivateGuest: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  return auth.getUser().pipe(
    map(() => {
      const type = auth.getSessionType();
      router.navigate([type === 'house' ? '/house/dashboard' : '/dashboard']);
      return false;
    }),
    catchError(() => of(true))
  );
};
