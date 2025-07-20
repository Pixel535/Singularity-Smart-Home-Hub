import { Component, EventEmitter, Output, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-mode-step',
  standalone: true,
  imports: [CommonModule, ButtonModule],
  templateUrl: './mode-step.component.html',
  styleUrls: ['./mode-step.component.scss']
})
export class ModeStepComponent implements OnInit {
  private baseInitUrl = `${environment.apiBaseUrl}/connectivity`;

  @Output() modeSelected = new EventEmitter<'local' | 'new' | 'join'>();

  isOnline = false;
  loading = true;

  private http = inject(HttpClient);

  ngOnInit(): void {
    this.http.get<{ connected: boolean; online: boolean }>(`${this.baseInitUrl}/check`)
      .subscribe({
        next: (res) => {
          this.isOnline = !!res.online;
          this.loading = false;
        },
        error: () => {
          this.isOnline = false;
          this.loading = false;
        }
      });
  }

  select(mode: 'local' | 'new' | 'join') {
    if (!this.loading) {
      this.modeSelected.emit(mode);
    }
  }
}
