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
export class DashboardComponent {
  private baseUrl = 'http://127.0.0.1:5000/dashboard';
  private auth = inject(AuthService);
  private router = inject(Router);
  private http = inject(HttpClient);
}