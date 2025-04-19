import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { TabViewModule } from 'primeng/tabview';
import { ButtonModule } from 'primeng/button';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { HeaderComponent } from '../shared/header/header.component';

@Component({
  selector: 'app-house-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    TabViewModule,
    ButtonModule,
    ToastModule,
    HeaderComponent
  ],
  templateUrl: './house-dashboard.component.html',
  styleUrls: ['./house-dashboard.component.scss'],
  providers: [MessageService]
})
export class HouseDashboardComponent implements OnInit {
  private route = inject(ActivatedRoute);
  private http = inject(HttpClient);
  private messageService = inject(MessageService);

  houseId!: number;
  houseName: string = '';
  loading = true;
  isLoaded = false;

  rooms: any[] = [];
  devices: any[] = [];

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      const id = params.get('houseId');
      if (id) {
        this.houseId = +id;
        this.loadHouseData();
      }
    });
  }

  loadHouseData() {
    this.http.get<any>(`http://localhost:5000/house/${this.houseId}`, { withCredentials: true })
      .subscribe({
        next: (res) => {
          this.houseName = res.HouseName;
          this.loading = false;
          this.isLoaded = true;
        },
        error: () => {
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to load house data'
          });
          this.loading = false;
        }
      });
  }
}
