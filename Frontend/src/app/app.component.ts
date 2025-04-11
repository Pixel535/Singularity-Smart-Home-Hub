import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { ToastModule } from 'primeng/toast';
import { OnInit } from '@angular/core';
import { AuthService } from './auth/auth.service';

@Component({
  standalone: true,
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  imports: [
    RouterOutlet,
    ToastModule
  ]
})
export class AppComponent implements OnInit {
  constructor(private auth: AuthService) {}

  ngOnInit(): void {
    const accessToken = this.auth.getAccessToken();

    if (!accessToken && this.auth.getRefreshToken()) {
      this.auth.refresh().subscribe({
        next: () => console.log('Access token refreshed'),
        error: () => this.auth.logout()
      });
    }

    this.auth.startIdleWatch();
  }
}
