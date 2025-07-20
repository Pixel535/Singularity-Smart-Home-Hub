import { Component, OnInit, inject } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { AuthService } from '../../auth/auth.service';

@Component({
  standalone: true,
  selector: 'app-login-to-house',
  templateUrl: './login-to-house.component.html',
  styleUrls: ['./login-to-house.component.scss'],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ToastModule,
    CardModule,
    ButtonModule
  ],
  providers: [MessageService]
})
export class LoginToHouseComponent implements OnInit {
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private auth = inject(AuthService);
  private toast = inject(MessageService);

  form: FormGroup = this.fb.group({
    PIN: ['', [Validators.required, Validators.pattern(/^\d{6}$/)]]
  });

  pinValue = '';
  isLoading = false;
  submitted = false;
  loading = true;

  ngOnInit(): void {
    this.auth.getInitializeStatus().subscribe({
      next: (res) => {
        if (!res.config_exists) {
          this.toast.add({
            severity: 'error',
            summary: 'Missing Configuration',
            detail: 'No house is configured. Please restart the setup.'
          });
        }
        this.loading = false;
      },
      error: () => {
        this.toast.add({
          severity: 'error',
          summary: 'Connection Error',
          detail: 'Could not verify configuration.'
        });
        this.loading = false;
      }
    });
  }

  handleDigitClick(d: string) {
    if (this.pinValue.length < 6) {
      this.pinValue += d;
      this.form.patchValue({ PIN: this.pinValue });
    }
  }

  handleBackspace() {
    this.pinValue = this.pinValue.slice(0, -1);
    this.form.patchValue({ PIN: this.pinValue });
  }

  isInvalid(field: string): boolean {
    const control = this.form.get(field);
    return !!(control && control.invalid && this.submitted);
  }

  submit() {
    this.submitted = true;

    if (this.form.invalid) return;

    this.isLoading = true;

    this.auth.loginToHouse({ PIN: this.pinValue }).subscribe({
      next: () => {
        console.log("git")
        this.router.navigate(['/house/dashboard']);
      },
      error: () => {
        this.isLoading = false;
        this.pinValue = '';
        this.form.patchValue({ PIN: '' });
        this.submitted = false;

        this.toast.add({
          severity: 'error',
          summary: 'Invalid PIN',
          detail: 'Please try again.'
        });
      }
    });
  }
}
