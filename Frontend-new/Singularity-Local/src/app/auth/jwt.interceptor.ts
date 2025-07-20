import { HttpInterceptorFn } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';
import { HttpErrorResponse, HttpRequest } from '@angular/common/http';

export const jwtInterceptor: HttpInterceptorFn = (req, next) => {
  const isRefresh = req.url.endsWith('/auth/refresh');

  const csrfToken = getCsrfToken();

  const shouldAddCsrf =
    !isRefresh &&
    ['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method.toUpperCase()) &&
    csrfToken;

  const modifiedReq = req.clone({
    ...(shouldAddCsrf && {
      setHeaders: { 'X-CSRF-TOKEN': csrfToken }
    }),
    withCredentials: true
  });

  return next(modifiedReq).pipe(
    catchError((error: HttpErrorResponse) => {
      return throwError(() => error);
    })
  );
};


function getCsrfToken(): string {
  const match = document.cookie.match(new RegExp('(^| )csrf_access_token=([^;]+)'));
  return match ? match[2] : '';
}
