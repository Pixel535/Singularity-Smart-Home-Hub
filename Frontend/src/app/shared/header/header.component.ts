import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
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
    ChipModule
  ]
})
export class HeaderComponent implements OnChanges {
  @Input() houseName: string | null = null;
  @Input() isInsideHouse = false;
  @Input() houseId: number | null = null;
  @Input() userLogin: string | null = null;

  constructor(private auth: AuthService, private router: Router) {}

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

  houseMenuItems: any[] = [];

  ngOnChanges(changes: SimpleChanges): void {
    this.houseMenuItems =
      this.isInsideHouse && this.houseId != null
        ? [
            {
              label: 'House Info',
              icon: 'pi pi-info-circle',
              command: () =>
                this.router.navigate(['/house/info'], {
                  state: { houseId: this.houseId }
                })
            }
          ]
        : [];
  }

  logout() {
    this.auth.logout();
  }

  goHome() {
    this.router.navigate(['/dashboard']);
  }
}
