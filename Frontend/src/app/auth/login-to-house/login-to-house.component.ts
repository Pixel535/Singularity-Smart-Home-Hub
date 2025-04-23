import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { MessageService } from 'primeng/api';
import { ToastModule } from 'primeng/toast';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login-to-house',
  standalone: true,
  templateUrl: './login-to-house.component.html',
  styleUrls: ['./login-to-house.component.scss'],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    ToastModule,
    CardModule,
    ButtonModule,
    InputTextModule
  ],
  providers: [MessageService]
})
export class LoginToHouseComponent {
  form: FormGroup;
  pinValue: string = '';
  isLoading = false;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private messageService: MessageService,
    private auth: AuthService
  ) {
    this.form = this.fb.group({
      HouseID: [null, Validators.required],
      PIN: [null, [Validators.required, Validators.pattern(/^\d{6}$/)]]
    });
  }

  handleDigitClick(digit: string) {
    if (this.pinValue.length < 6) {
      this.pinValue += digit;
      this.form.get('PIN')?.setValue(Number(this.pinValue));
    }
  }

  handleBackspace() {
    this.pinValue = this.pinValue.slice(0, -1);
    this.form.get('PIN')?.setValue(Number(this.pinValue || 0));
  }

  submit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.isLoading = true;

    const payload = {
      HouseID: Number(this.form.get('HouseID')?.value),
      PIN: Number(this.form.get('PIN')?.value)
    };

    this.auth.loginToHouse(payload).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Logged into house'
        });

        setTimeout(() => {
          this.router.navigate(['/house/dashboard'], {
            state: { houseId: payload.HouseID }
          });
        });
      },
      error: (err) => {
        const detail = err?.error?.msg || 'Login failed';
        this.messageService.add({ severity: 'error', summary: 'Error', detail });
        this.isLoading = false;
      }
    });
  }

  isInvalid(controlName: string): boolean {
    const control = this.form.get(controlName);
    return !!control && control.invalid && control.touched;
  }
}
