import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';
import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from 'primeng/avatar';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { ButtonModule } from 'primeng/button';
import { ChipModule } from 'primeng/chip';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  standalone: true,
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  imports: [
    CommonModule,
    MenubarModule,
    AvatarModule,
    TieredMenuModule,
    ButtonModule,
    ChipModule,
  ]
})
export class HeaderComponent {
  @Input() houseName: string | null = null;
  @Input() isInsideHouse = false;
  @Input() userLogin: string | null = null;

  constructor(
    private auth: AuthService,
    private router: Router
  ) { }

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

  houseMenuItems = [
    {
      label: 'House Info',
      icon: 'pi pi-info-circle',
      command: () => console.log('House Info clicked') // placeholer
    }
  ];

  logout() {
    this.auth.logout();
  }

  goHome() {
    this.router.navigate(['/dashboard']);
  }

}
