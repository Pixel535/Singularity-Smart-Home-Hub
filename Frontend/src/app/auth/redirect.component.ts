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
      next: () => {
        this.auth.isLoggedIn$.next(true);
        this.auth.startRefreshLoop();
        this.router.navigate(['/dashboard']);
      },
      error: () => {
        this.auth.isLoggedIn$.next(false);
        this.router.navigate(['/login']);
      }
    });
  }
}
