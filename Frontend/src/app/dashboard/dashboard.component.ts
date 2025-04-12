import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth/auth.service';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from 'primeng/avatar';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { ButtonModule } from 'primeng/button';
import { ChipModule } from 'primeng/chip';
import { HeaderComponent } from '../shared/header/header.component';

@Component({
  standalone: true,
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  imports: [
    CommonModule,
    RouterModule,
    MenubarModule,
    AvatarModule,
    TieredMenuModule,
    ButtonModule,
    ChipModule,
    HeaderComponent
  ]
})
export class DashboardComponent implements OnInit {
  private baseUrl = 'http://127.0.0.1:5000/dashboard';
  private auth = inject(AuthService);
  private router = inject(Router);
  private http = inject(HttpClient);

  userLogin: string | null = null;

  menuItems = [
    {
      label: 'Profile',
      icon: 'pi pi-user',
      command: () => this.router.navigate(['/profile'])
    },
    {
      label: 'Log out',
      icon: 'pi pi-sign-out',
      command: () => this.logout()
    }
  ];

  ngOnInit(): void {
    this.auth.startIdleWatch();
    this.fetchUserInfo();
  }

  fetchUserInfo() {
    this.http.get<{ user: string }>(`${this.baseUrl}/dashboardInfo`).subscribe({
      next: res => {
        this.userLogin = res.user;
      },
      error: () => {
        this.auth.logout();
      }
    });
  }

  logout() {
    this.auth.logout();
  }

  goHome() {
    this.router.navigate(['/dashboard']);
  }
}