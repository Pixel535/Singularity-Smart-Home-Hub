import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from './auth.service';
import { map, catchError, of } from 'rxjs';

export const canActivateGuest: CanActivateFn = () => {
  const auth = inject(AuthService);
  const router = inject(Router);

  return auth.getHouseStatus().pipe(
    map((house) => {
      if (house?.houseId) {
        router.navigateByUrl('/house/dashboard');
        return false;
      }

      return true;
    }),
    catchError(() => {
      return of(true);
    })
  );
};
