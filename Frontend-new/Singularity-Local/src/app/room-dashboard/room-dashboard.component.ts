import { Component, OnInit, AfterViewInit, ViewChildren, ElementRef, QueryList, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { HeaderComponent } from '../../shared/header/header.component';
import { AuthService } from '../auth/auth.service';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { ButtonModule } from 'primeng/button';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-room-dashboard',
  standalone: true,
  templateUrl: './room-dashboard.component.html',
  styleUrls: ['./room-dashboard.component.scss'],
  imports: [
    CommonModule,
    RouterModule,
    ToastModule,
    HeaderComponent,
    ButtonModule
  ],
  providers: [MessageService]
})
export class RoomDashboardComponent implements OnInit, AfterViewInit {
  private router = inject(Router);
  private http = inject(HttpClient);
  private auth = inject(AuthService);
  private cdr = inject(ChangeDetectorRef);
  private messageService = inject(MessageService);

  houseId!: number;
  roomId!: number;
  roomName = '';
  houseName = '';
  loading = true;

  activeTab: 'devices' | 'functions' = 'devices';

  @ViewChildren('tabItem') tabItems!: QueryList<ElementRef>;
  tabIndicatorStyle = { left: '0px', width: '0px' };

  baseDashboardUrl = `${environment.apiBaseUrl}/dashboard`;
  baseRoomDashboardUrl = `${environment.apiBaseUrl}/roomDashboard`;

  ngOnInit(): void {
    this.auth.startIdleWatch();

    const state = history.state;
    if (!state?.roomId || !state?.houseId) {
      this.messageService.add({
        severity: 'error',
        summary: 'Missing Data',
        detail: 'No room or house ID provided. Redirecting...'
      });
      this.router.navigate(['/house/dashboard']);
      return;
    }

    this.houseId = state.houseId;
    this.roomId = state.roomId;

    this.loadRoomData();
    this.loadHouseName();
  }

  ngAfterViewInit(): void {
    this.tabItems.changes.subscribe(() => this.safeUpdateIndicator());
    setTimeout(() => this.safeUpdateIndicator());
  }

  private safeUpdateIndicator(): void {
    setTimeout(() => {
      this.updateIndicator();
      this.cdr.detectChanges();
    });
  }

  updateIndicator() {
    if (!this.tabItems?.length) return;

    const index = this.activeTab === 'devices' ? 0 : 1;
    const tabEl = this.tabItems.get(index)?.nativeElement;
    if (tabEl) {
      this.tabIndicatorStyle = {
        left: `${tabEl.offsetLeft}px`,
        width: `${tabEl.getBoundingClientRect().width}px`
      };
    }
  }

  setTab(tab: 'devices' | 'functions') {
    this.activeTab = tab;
    this.updateIndicator();
  }

  loadRoomData() {
    this.http.post<{ RoomName: string }>(
      `${this.baseRoomDashboardUrl}/getRoom`,
      { RoomID: this.roomId, HouseID: this.houseId },
      { withCredentials: true }
    ).subscribe({
      next: res => {
        this.roomName = res.RoomName;
        this.loading = false;
      },
      error: err => {
        const detail = err?.error?.msg || 'Failed to load room data';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
        this.loading = false;
      }
    });
  }

  loadHouseName() {
    this.http.post<{ HouseName: string }>(
      `${this.baseDashboardUrl}/getHouse`,
      { HouseID: this.houseId },
      { withCredentials: true }
    ).subscribe({
      next: res => this.houseName = res.HouseName,
      error: () => this.houseName = ''
    });
  }

  goBackToHouseDashboard() {
    this.router.navigate(['/house/dashboard'], {
      state: { houseId: this.houseId }
    });
  }
}
