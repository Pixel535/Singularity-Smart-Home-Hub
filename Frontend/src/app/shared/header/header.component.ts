import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from 'primeng/avatar';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { ButtonModule } from 'primeng/button';
import { ChipModule } from 'primeng/chip';

@Component({
  selector: 'app-header',
  standalone: true,
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  imports: [
    MenubarModule,
    AvatarModule,
    TieredMenuModule,
    ButtonModule,
    ChipModule,
  ]
})
export class HeaderComponent {
  private router = inject(Router);
  private auth = inject(AuthService);

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

  constructor() {
    this.loadUserLoginFromToken();
  }

  logout() {
    this.auth.logout();
  }

  goHome() {
    this.router.navigate(['/dashboard']);
  }

  private loadUserLoginFromToken(): void {
    const token = this.auth.getAccessToken();
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        this.userLogin = payload.sub || payload.identity || null;
      } catch (e) {
        console.error('Invalid JWT token format:', e);
        this.userLogin = null;
      }
    }
  }
}