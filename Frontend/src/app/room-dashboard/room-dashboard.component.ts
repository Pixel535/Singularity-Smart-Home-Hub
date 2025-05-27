import { Component, OnInit, inject, ViewChildren, QueryList, ElementRef, ChangeDetectorRef, AfterViewInit, OnDestroy } from '@angular/core';
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
export class RoomDashboardComponent implements OnInit, AfterViewInit, OnDestroy {
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

  weather: any = null;
  news: any[] = [];
  city = '';
  country = '';
  countryCode = '';
  private externalDataInterval: any;

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

      this.http.post<any>(
        `${environment.apiBaseUrl}/house/getHouse`,
        { HouseID: this.houseId },
        { withCredentials: true }
      ).subscribe({
        next: res => {
          this.houseName = res.HouseName;
          this.city = res.City;
          this.country = res.Country;
          this.countryCode = res.CountryCode;
          this.scheduleExternalDataFetch();
        },
        error: () => {
          this.houseName = '';
        }
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

  ngOnDestroy(): void {
    clearInterval(this.externalDataInterval);
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

  private scheduleExternalDataFetch() {
    this.fetchExternalData();
    this.externalDataInterval = setInterval(() => {
      this.fetchExternalData();
    }, 15 * 60 * 1000); // 15 min
  }

  private fetchExternalData() {
    const payload = {
      City: this.city,
      Country: this.country,
      CountryCode: this.countryCode
    };

    this.http.post<any>(`${environment.apiBaseUrl}/house/externalData`, payload, {
      withCredentials: true
    }).subscribe({
      next: (res) => {
        this.weather = res.weather;
        this.news = res.news?.articles || [];
      },
      error: (err) => {
        console.error('Failed to fetch weather/news', err);
      }
    });
  }
}
