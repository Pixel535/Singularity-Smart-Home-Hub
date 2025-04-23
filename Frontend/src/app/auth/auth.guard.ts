import { inject } from '@angular/core';
import { CanActivateFn, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from './auth.service';
import { map, catchError, of } from 'rxjs';

export const canActivateAuth: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  return auth.getUser().pipe(
    map((res) => {
      const type = auth.getSessionType();
      const targetUrl = state.url;

      const isUserOnlyRoute = [
        '/dashboard',
        '/profile',
        '/profile/changePassword',
      ].some(route => targetUrl.startsWith(route));

      if (type === 'house' && isUserOnlyRoute) {
        router.navigateByUrl('/house/dashboard', {
          state: { houseId: res.houseId }
        });
        return false;
      }

      return true;
    }),
    catchError(() => {
      auth.logout();
      return of(false);
    })
  );
};
