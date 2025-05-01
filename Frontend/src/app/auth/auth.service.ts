import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, tap } from 'rxjs';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseUrl = `${environment.apiBaseUrl}/auth`;
  isLoggedIn$ = new BehaviorSubject<boolean>(false);
  private sessionType: 'user' | 'house' | null = null;
  private idleTimer: any;
  private idleLimitMs = 15 * 60 * 1000; // 15 min
  private refreshInterval: any;
  private refreshRateMs = 14 * 60 * 1000; // 14 min

  constructor(private http: HttpClient, private router: Router) {}

  login(data: { UserLogin: string; Password: string }) {
    return this.http.post(`${this.baseUrl}/login`, data, { withCredentials: true }).pipe(
      tap(() => {
        this.sessionType = 'user';
        this.isLoggedIn$.next(true);
        this.startIdleWatch();
        this.startRefreshLoop();
      })
    );
  }

  loginToHouse(data: { HouseID: number, PIN: number }) {
    return this.http.post(`${this.baseUrl}/loginHouse`, data, {
      withCredentials: true
    }).pipe(
      tap(() => {
        this.sessionType = 'house';
        this.isLoggedIn$.next(true);
        this.startIdleWatch();
        this.startRefreshLoop();
      })
    );
  }
  

  register(data: any) {
    return this.http.post(`${this.baseUrl}/register`, data, { withCredentials: true });
  }

  refresh() {
    return this.http.post(`${this.baseUrl}/refresh`, {}, {
      withCredentials: true,
      headers: {
        'X-CSRF-TOKEN': this.getCsrfToken(true)
      }
    });
  }

  logout() {
    this.http.post(`${this.baseUrl}/logout`, {}, { withCredentials: true }).subscribe(() => {
      this.isLoggedIn$.next(false);
      clearTimeout(this.idleTimer);
      clearInterval(this.refreshInterval);
  
      const session = this.getSessionType();
      this.sessionType = null;
  
      const redirect = session === 'house' ? '/loginHouse' : '/login';
      this.router.navigate([redirect]);
    });
  }
  
  

  getUser() {
  return this.http.get<{ session: 'user' | 'house' | 'unknown'; houseId?: number; userLogin?: string }>(
    `${this.baseUrl}/me`,
    { withCredentials: true }
  ).pipe(
    tap((res) => {
      this.sessionType = res.session === 'user' ? 'user': res.session === 'house' ? 'house' : null;
      this.isLoggedIn$.next(true);
    })
  );
}



  private getCsrfToken(isRefresh = false): string {
    const cookieName = isRefresh ? 'csrf_refresh_token' : 'csrf_access_token';
    const match = document.cookie.match(new RegExp(`(^| )${cookieName}=([^;]+)`));
    return match ? match[2] : '';
  }

  startIdleWatch() {
    this.resetIdleTimer();
    ['mousemove', 'keydown', 'click'].forEach(event =>
      document.addEventListener(event, this.resetIdleTimer.bind(this))
    );
  }

  private resetIdleTimer() {
    clearTimeout(this.idleTimer);
    this.idleTimer = setTimeout(() => {
      this.logout();
      alert('You were logged out because of inactivity!');
    }, this.idleLimitMs);
  }

  startRefreshLoop() {
    clearInterval(this.refreshInterval);
    this.refreshInterval = setInterval(() => {
      this.refreshToken();
    }, this.refreshRateMs);
  }
  
  private refreshToken() {
    this.refresh().subscribe({
      next: () => {
        console.log('[JWT] Access token refreshed');
      },
      error: () => {
        console.warn('[JWT] Refresh failed — logging out');
        this.logout();
      }
    });
  }

  public getSessionType(): 'user' | 'house' | null {
    return this.sessionType;
  }
  
  public isUserSession(): boolean {
    return this.sessionType === 'user';
  }
  
  public isHouseSession(): boolean {
    return this.sessionType === 'house';
  }
}
