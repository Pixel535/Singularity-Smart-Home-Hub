import { Component, inject, OnInit } from '@angular/core';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-redirect',
  template: ''
})
export class RedirectComponent implements OnInit {
  private auth = inject(AuthService);
  private router = inject(Router);

  ngOnInit(): void {
    this.auth.getUser().subscribe({
      next: (res) => {
        this.auth.isLoggedIn$.next(true);
        this.auth.startRefreshLoop();
  
        const type = this.auth.getSessionType();
        const route = type === 'house' ? '/house/dashboard' : '/dashboard';
  
        const navExtras = type === 'house' && res.houseId
          ? { state: { houseId: res.houseId } }
          : undefined;
  
        this.router.navigate([route], navExtras);
      },
      error: () => {
        this.auth.isLoggedIn$.next(false);
        const type = this.auth.getSessionType();
        this.router.navigate([type === 'house' ? '/loginHouse' : '/login']);
      }
    });
  }
  
  
}
