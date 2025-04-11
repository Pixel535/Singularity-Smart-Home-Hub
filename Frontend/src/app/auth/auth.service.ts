import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, tap } from 'rxjs';
import { Router } from '@angular/router';
import { isTokenExpired } from './jwt.utils';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private baseUrl = 'http://localhost:5000/auth';
  private tokenKey = 'access_token';
  private refreshKey = 'refresh_token';

  isLoggedIn$ = new BehaviorSubject<boolean>(this.hasToken());

  private idleTimer: any;
  private idleLimitMs = 15 * 60 * 1000; // 15 min

  constructor(private http: HttpClient, private router: Router) {}

  private hasToken(): boolean {
    const token = localStorage.getItem(this.tokenKey);
    return !!token && !isTokenExpired(token);
  }

  login(data: { UserLogin: string; Password: string }) {
    return this.http.post<any>(`${this.baseUrl}/login`, data).pipe(
      tap(tokens => this.setTokens(tokens))
    );
  }

  register(data: any) {
    return this.http.post(`${this.baseUrl}/register`, data);
  }

  refresh() {
    const refreshToken = this.getRefreshToken();

    return this.http.post<any>(`${this.baseUrl}/refresh`, {}, {
      headers: {
        Authorization: `Bearer ${refreshToken}`
      }
    }).pipe(
      tap(tokens => this.setAccessToken(tokens.access_token))
    );
  }

  logout() {
    localStorage.clear();
    this.isLoggedIn$.next(false);
    clearTimeout(this.idleTimer);
    this.router.navigate(['/login']);
  }

  private setTokens(tokens: { access_token: string; refresh_token: string }) {
    localStorage.setItem(this.tokenKey, tokens.access_token);
    localStorage.setItem(this.refreshKey, tokens.refresh_token);
    this.isLoggedIn$.next(true);
  }

  private setAccessToken(token: string) {
    localStorage.setItem(this.tokenKey, token);
  }

  getAccessToken(): string | null {
    const token = localStorage.getItem(this.tokenKey);
    return token && !isTokenExpired(token) ? token : null;
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.refreshKey);
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
}
