import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router, ActivatedRoute } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ToastModule } from 'primeng/toast';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-change-pin',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ButtonModule,
    InputTextModule,
    ToastModule,
  ],
  templateUrl: './change-pin.component.html',
  styleUrls: ['./change-pin.component.scss'],
  providers: [MessageService]
})
export class ChangeHousePinComponent implements OnInit {
  private fb = inject(FormBuilder);
  private http = inject(HttpClient);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  private messageService = inject(MessageService);

  private baseUrl = `${environment.apiBaseUrl}/house`;

  houseId!: number;
  from: 'dashboard' | 'info' = 'dashboard';

  form: FormGroup = this.fb.group({
    CurrentPIN: ['', [Validators.required, Validators.pattern(/^\d{6}$/)]],
    NewPIN: ['', [Validators.required, Validators.pattern(/^\d{6}$/)]],
    ConfirmPIN: ['', [Validators.required]]
  }, { validators: [this.pinsMatchValidator] });

  isSubmitting = false;
  showCurrent = false;
  showNew = false;
  showConfirm = false;

  ngOnInit(): void {
    const state = history.state;
    this.houseId = state.houseId;
    this.from = state.from || 'dashboard';
  }

  pinsMatchValidator(group: FormGroup) {
    const newPin = group.get('NewPIN')?.value;
    const confirmPin = group.get('ConfirmPIN')?.value;
    return newPin === confirmPin ? null : { pinMismatch: true };
  }

  submit() {
    if (this.form.invalid) return;

    const payload = {
      HouseID: this.houseId,
      ...this.form.value
    };

    this.isSubmitting = true;

    this.http.put(`${this.baseUrl}/changePin`, payload, {
      withCredentials: true
    }).subscribe({
      next: (res: any) => {
        this.messageService.add({
          severity: 'success',
          summary: 'PIN changed',
          detail: res?.msg || 'House PIN has been updated.'
        });
        setTimeout(() => {
          this.navigateBack();
        }, 1500);
      },
      error: (err) => {
        const detail = err?.error?.msg || 'PIN change failed.';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
        this.isSubmitting = false;
      }
    });
  }

  cancel() {
    this.navigateBack();
  }

  private navigateBack() {
    const route = this.from === 'info' ? '/house/info' : '/dashboard';
    this.router.navigate([route], {
      state: { houseId: this.houseId }
    });
  }
}
