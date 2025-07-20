import { Component, inject, OnInit, EventEmitter, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { DropdownModule } from 'primeng/dropdown';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { environment } from '../../../environments/environment';
import { Router } from '@angular/router';

@Component({
  selector: 'app-wifi-step',
  standalone: true,
  imports: [
    CommonModule, 
    ReactiveFormsModule, 
    DropdownModule, 
    InputTextModule, 
    ButtonModule,
    ToastModule
  ],
  providers: [MessageService],
  templateUrl: './wifi-step.component.html',
  styleUrls: ['./wifi-step.component.scss']
})
export class WifiStepComponent implements OnInit {
  
  @Output() checkedOffline = new EventEmitter<{ configExists: boolean }>();

  private http = inject(HttpClient);
  private fb = inject(FormBuilder);
  private toast = inject(MessageService);
  private router = inject(Router);

  private connectivityUrl = `${environment.apiBaseUrl}/connectivity`;
  private initializationUrl = `${environment.apiBaseUrl}/initialization`;

  form!: FormGroup;
  networks: string[] = [];
  loading = false;
  submitted = false;
  errorMessage: string | null = null;
  showPassword = false;

  ngOnInit() {
    this.form = this.fb.group({
      ssid: [null, Validators.required],
      password: ['']
    });

    this.http.get<{ ssid: string }[]>(`${this.connectivityUrl}/wifi/scan`).subscribe({
      next: (res) => this.networks = res.map(n => n.ssid),
      error: (err) => {
        this.networks = [];
        const msg = err?.error?.msg || 'Failed to scan WiFi networks';
        this.toast.add({
          severity: 'error',
          summary: 'WiFi Scan Error',
          detail: msg,
          life: 4000
        });
      }
    });
  }

  onSubmit() {
    this.submitted = true;
    this.errorMessage = null;

    if (this.form.invalid) return;

    this.loading = true;

    this.http.post(`${this.connectivityUrl}/wifi/connect`, this.form.value).subscribe({
      next: () => {
        this.loading = false;
        this.toast.add({
          severity: 'success',
          summary: 'Connected',
          detail: 'You are now connected to WiFi',
          life: 3000
        });
        this.router.navigate(['/']); // wracamy do redirect logiki
      },
      error: (err) => {
        this.errorMessage = 'Connection failed. Please check your password.';
        this.loading = false;

        const msg = err?.error?.msg || 'Failed to connect to WiFi';
        this.toast.add({
          severity: 'error',
          summary: 'Connection Error',
          detail: msg,
          life: 4000
        });
      }
    });
  }

  continueOffline() {
    this.loading = true;
    
    this.http.get<{ config_exists: boolean }>(`${this.initializationUrl}/status`).subscribe({
      next: (res) => {
        this.loading = false;
        this.checkedOffline.emit({ configExists: res.config_exists });
      },
      error: () => {
        this.loading = false;
        this.checkedOffline.emit({ configExists: false });
      }
    });
  }
}
