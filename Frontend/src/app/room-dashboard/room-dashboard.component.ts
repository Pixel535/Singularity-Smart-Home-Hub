import { Component, OnInit, inject, ViewChildren, QueryList, ElementRef, ChangeDetectorRef, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../auth/auth.service';
import { MessageService } from 'primeng/api';
import { HeaderComponent } from '../shared/header/header.component';
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
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private http = inject(HttpClient);
  private auth = inject(AuthService);
  private cdr = inject(ChangeDetectorRef);
  private messageService = inject(MessageService);

  houseId!: number;
  houseName = '';
  roomId!: number;
  roomName = '';

  loading = true;

  get isLoaded(): boolean {
    return !this.loading;
  }

  private baseUrl = `${environment.apiBaseUrl}/house/room`;

  activeTab: 'devices' | 'functions' = 'devices';

  @ViewChildren('tabItem') tabItems!: QueryList<ElementRef>;
  tabIndicatorStyle = { left: '0px', width: '0px' };

  ngOnInit(): void {
    this.auth.startIdleWatch();

    const state = history.state;
    if (state && state.roomId && state.houseId) {
      this.roomId = state.roomId;
      this.houseId = state.houseId;
      this.loadRoomData();

      this.http.post<{ HouseName: string }>(
        `${environment.apiBaseUrl}/house/getHouse`,
        { HouseID: this.houseId },
        { withCredentials: true }
      ).subscribe({
        next: res => this.houseName = res.HouseName,
        error: () => this.houseName = ''
      });
    } else {
      this.messageService.add({
        severity: 'error',
        summary: 'Missing Data',
        detail: 'No room or house ID provided. Redirecting to dashboard...'
      });
      this.router.navigate(['/dashboard']);
    }
  }

  ngAfterViewInit(): void {
    this.tabItems.changes.subscribe(() => this.safeUpdateIndicator());
    setTimeout(() => this.safeUpdateIndicator());
  }

  setTab(tab: 'devices' | 'functions') {
    this.activeTab = tab;
    this.updateIndicator();
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

  private safeUpdateIndicator() {
    setTimeout(() => {
      this.updateIndicator();
      this.cdr.detectChanges();
    });
  }

  private loadRoomData() {
    this.http.post<{ RoomName: string }>(
      `${this.baseUrl}/getRoom`,
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

  goBackToHouseDashboard() {
    this.router.navigate(['/house/dashboard'], {
      state: { houseId: this.houseId }
    });
  }
}
