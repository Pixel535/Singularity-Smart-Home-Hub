import { Component, OnInit, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-redirect',
  standalone: true,
  template: '',
})
export class RedirectComponent implements OnInit {
  private http = inject(HttpClient);
  private router = inject(Router);

  private baseConnectivity = `${environment.apiBaseUrl}/connectivity`;
  private baseInitialize = `${environment.apiBaseUrl}/initialization`;

  ngOnInit(): void {
    this.http.get<{ online: boolean }>(`${this.baseConnectivity}/check`).subscribe({
      next: (res) => {
        if (res.online) {
          this.http.get<{ config_exists: boolean }>(`${this.baseInitialize}/status`).subscribe({
            next: (status) => {
              if (status.config_exists) {
                this.router.navigate(['/loginHouse']);
              } else {
                this.router.navigate(['/initialization']);
              }
            },
            error: () => {
              this.router.navigate(['/initialization']);
            }
          });
        } else {
          this.http.get<{ config_exists: boolean }>(`${this.baseInitialize}/status`).subscribe({
            next: (status) => {
              if (status.config_exists) {
                this.router.navigate(['/loginHouse']);
              } else {
                this.router.navigate(['/initialization']);
              }
            },
            error: () => {
              this.router.navigate(['/initialization']);
            }
          });
        }
      },
      error: () => {
        this.router.navigate(['/initialization']);
      }
    });
  }
}
