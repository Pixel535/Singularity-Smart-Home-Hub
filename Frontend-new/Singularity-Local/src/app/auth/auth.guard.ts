import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from './auth.service';
import { catchError, map, switchMap, of } from 'rxjs';

export const canActivateAuth: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  return auth.getHouseStatus().pipe(
    switchMap((house) => {
      const targetUrl = state.url;

      if (house?.houseId && targetUrl.startsWith('/house')) {
        return of(true);
      }

      return auth.getInitializeStatus().pipe(
        map((status) => {
          console.log(status);
          if (status?.config_exists) {
            router.navigateByUrl('/loginHouse');
          } else {
            router.navigateByUrl('/initialization');
          }
          return false;
        }),
        catchError(() => {
          auth.logout();
          return of(false);
        })
      );
    }),
    catchError(() => {
      auth.logout();
      return of(false);
    })
  );
};
