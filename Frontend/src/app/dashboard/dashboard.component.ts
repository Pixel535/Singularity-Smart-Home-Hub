import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth/auth.service';
import { Router } from '@angular/router';
import { ButtonModule } from 'primeng/button';

@Component({
  standalone: true,
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  imports: [
    CommonModule,
    ButtonModule
  ]
})
export class DashboardComponent implements OnInit {
  private auth = inject(AuthService);
  private router = inject(Router);

  userLogin: string | null = null;

  ngOnInit(): void {
    const token = this.auth.getAccessToken();
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      this.userLogin = payload.sub || payload.identity || null;
    }
  
    this.auth.startIdleWatch();
  }
  

  logout() {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
