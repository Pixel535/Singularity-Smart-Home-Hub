import { Component, OnInit, Output, EventEmitter, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { FormsModule } from '@angular/forms';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-select-house-step',
  standalone: true,
  imports: [
    CommonModule,
    CardModule,
    ButtonModule,
    FormsModule,
    ToastModule
  ],
  providers: [MessageService],
  templateUrl: './select-house-step.component.html',
  styleUrls: ['./select-house-step.component.scss']
})
export class SelectHouseStepComponent implements OnInit {
  houses: any[] = [];
  selectedHouseId: string | null = null;
  loading = false;
  error: string | null = null;

  private http = inject(HttpClient);
  private toast = inject(MessageService);
  private router = inject(Router);
  private baseInitUrl = `${environment.apiBaseUrl}/initialization`;

  @Output() completed = new EventEmitter<void>();

  ngOnInit(): void {
    this.http.get<{ houses: any[] }>(`${this.baseInitUrl}/get-houses`).subscribe({
      next: (res) => {
        this.houses = res.houses;
      },
      error: (err) => {
        const msg = err?.error?.msg || 'Failed to load houses.';
        this.error = msg;
        this.toast.add({
          severity: 'error',
          summary: 'Load Error',
          detail: msg,
          life: 4000
        });
      }
    });
  }

  selectHouse(houseId: string) {
    this.selectedHouseId = houseId;
  }

  continue() {
    if (!this.selectedHouseId) return;
    this.loading = true;

    this.http.post(`${this.baseInitUrl}/link-house`, { HouseID: this.selectedHouseId }).subscribe({
      next: () => {
        this.toast.add({
          severity: 'success',
          summary: 'House linked',
          detail: 'You can now log in with your house PIN',
          life: 3000
        });
        this.loading = false;
        this.completed.emit();
      },
      error: (err) => {
        const msg = err?.error?.msg || 'Failed to link selected house.';
        this.error = msg;
        this.loading = false;

        this.toast.add({
          severity: 'error',
          summary: 'Link Error',
          detail: msg,
          life: 4000
        });
      }
    });
  }
}
