import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseAuthUrl = `${environment.apiBaseUrl}/auth`;
  private baseInitUrl = `${environment.apiBaseUrl}/initialization`;
  isLoggedIn$ = new BehaviorSubject<boolean>(false);
  private idleTimer: any;
  private idleLimitMs = 15 * 60 * 1000; // 15 min
  private refreshInterval: any;
  private refreshRateMs = 14 * 60 * 1000; // 14 min

  constructor(private http: HttpClient, private router: Router) {}

  loginToHouse(data: { PIN: string }) {
    return this.http.post(`${this.baseAuthUrl}/loginToHouse`, data, {
      withCredentials: true
    }).pipe(
      tap(() => {
        this.isLoggedIn$.next(true);
        this.startIdleWatch();
        this.startRefreshLoop();
      })
    );
  }

  loginUser(data: { UserLogin: string; Password: string }) {
    return this.http.post(`${this.baseAuthUrl}/loginUser`, data, {
      withCredentials: true
    }).pipe(
      tap(() => {
        this.isLoggedIn$.next(true);
      })
    );
  }


  logout() {
    this.http.post(`${this.baseAuthUrl}/logout`, {}, { withCredentials: true }).subscribe(() => {
      this.isLoggedIn$.next(false);
      clearTimeout(this.idleTimer);
      clearInterval(this.refreshInterval);
      this.router.navigateByUrl('/loginHouse');
    });
  }

  logoutUser() {
    return this.http.post(`${this.baseAuthUrl}/logout`, {}, {
      withCredentials: true
    }).subscribe(() => {
      this.isLoggedIn$.next(false);
    });
  }

  getHouseStatus(): Observable<{ houseId: number }> {
    return this.http.get<{ houseId: number }>(`${this.baseAuthUrl}/me`, {
      withCredentials: true
    }).pipe(
      tap((res) => {
        console.log(res);
        if (res?.houseId) {
          this.isLoggedIn$.next(true);
        } else {
          this.isLoggedIn$.next(false);
        }
      })
    );
  }

  getInitializeStatus(): Observable<{ config_exists: boolean; online: boolean }> {
    return this.http.get<{ config_exists: boolean; online: boolean }>(`${this.baseInitUrl}/status`, {
      withCredentials: true
    });
  }

  startIdleWatch() {
    this.resetIdleTimer();
    ['click', 'touchstart', 'keydown'].forEach(event =>
      document.addEventListener(event, this.resetIdleTimer.bind(this))
    );
  }

  private resetIdleTimer() {
    clearTimeout(this.idleTimer);
    this.idleTimer = setTimeout(() => {
      this.logout();
      alert('Session expired due to inactivity.');
    }, this.idleLimitMs);
  }

  startRefreshLoop() {
    clearInterval(this.refreshInterval);
    this.refreshInterval = setInterval(() => {
      this.refreshToken();
    }, this.refreshRateMs);
  }

  private refreshToken() {
    const token = this.getCsrfToken(true);

    this.http.post(`${this.baseAuthUrl}/refresh`, {}, {
      withCredentials: true,
      headers: {
        'X-CSRF-TOKEN': token
      }
    }).subscribe({
      next: () => {
        console.log('[JWT] Refreshed access token');
      },
      error: () => {
        console.warn('[JWT] Refresh failed — logging out');
        this.logout();
      }
    });
  }

  private getCsrfToken(isRefresh = false): string {
    const cookieName = isRefresh ? 'csrf_refresh_token' : 'csrf_access_token';
    const match = document.cookie.match(new RegExp(`(^| )${cookieName}=([^;]+)`));
    return match ? match[2] : '';
  }
}
