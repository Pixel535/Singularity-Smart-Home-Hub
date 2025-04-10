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
    const token = this.auth.getAccessToken();
    this.router.navigate([token ? '/dashboard' : '/login']);
  }
}
