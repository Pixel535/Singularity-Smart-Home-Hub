import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';
import { catchError, switchMap, throwError } from 'rxjs';
import { HttpErrorResponse, HttpRequest } from '@angular/common/http';

let isRefreshing = false;

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const authService = inject(AuthService);
  const router = inject(Router);

  const isAuthRequest = req.url.includes('/auth/login') || req.url.includes('/auth/register');
  if (isAuthRequest) {
    return next(req);
  }

  const token = authService.getAccessToken();

  if (token) {
    req = req.clone({
      setHeaders: { Authorization: `Bearer ${token}` }
    });
  }

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && !isRefreshing) {
        isRefreshing = true;

        return authService.refresh().pipe(
          switchMap(() => {
            isRefreshing = false;

            const newToken = authService.getAccessToken();
            const clonedReq = req.clone({
              setHeaders: { Authorization: `Bearer ${newToken}` }
            });

            return next(clonedReq);
          }),
          catchError(refreshError => {
            isRefreshing = false;
            authService.logout();
            router.navigate(['/login']);
            return throwError(() => refreshError);
          })
        );
      }

      return throwError(() => error);
    })
  );
};
