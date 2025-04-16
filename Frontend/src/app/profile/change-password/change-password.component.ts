import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ToastModule } from 'primeng/toast';

@Component({
  selector: 'app-change-password',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ButtonModule,
    InputTextModule,
    ToastModule
  ],
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss'],
  providers: [MessageService]
})
export class ChangePasswordComponent {
  private fb = inject(FormBuilder);
  private http = inject(HttpClient);
  private router = inject(Router);
  private messageService = inject(MessageService);

  form: FormGroup = this.fb.group({
    CurrentPassword: ['', Validators.required],
    NewPassword: ['', [Validators.required, Validators.minLength(6)]],
    ConfirmPassword: ['', Validators.required]
  }, { validators: [this.passwordsMatchValidator] });

  isSubmitting = false;
  showCurrent = false;
  showNew = false;
  showConfirm = false;


  private baseUrl = 'http://localhost:5000/profile';

  passwordsMatchValidator(group: FormGroup) {
    const newPass = group.get('NewPassword')?.value;
    const confirmPass = group.get('ConfirmPassword')?.value;
    return newPass === confirmPass ? null : { passwordMismatch: true };
  }

  submit() {
    if (this.form.invalid) return;

    this.isSubmitting = true;

    this.http.put(`${this.baseUrl}/changePassword`, this.form.value, {
      withCredentials: true
    }).subscribe({
      next: (res: any) => {
        this.messageService.add({
          severity: 'success',
          summary: 'Password changed',
          detail: res?.msg || 'Your password has been updated.'
        });
        setTimeout(() => {
          this.router.navigate(['/profile']);
        }, 1500);
      },
      error: (err) => {
        const detail = err?.error?.msg || 'Password change failed.';
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
    this.router.navigate(['/profile']);
  }
}
