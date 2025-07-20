import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MenubarModule } from 'primeng/menubar';
import { AuthService } from '../../app/auth/auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  imports: [CommonModule, MenubarModule]
})
export class HeaderComponent {
  @Input() houseName: string | null = null;
  @Input() houseId: number | null = null;

  constructor(
    private router: Router,
    private auth: AuthService
  ) {}

  goHome() {
    if (this.houseId != null) {
      this.router.navigate(['/house/dashboard'], {
        state: { houseId: this.houseId }
      });
    }
  }

  logout() {
    this.auth.logout();
    this.router.navigate(['/auth/loginHouse']);
  }
}
