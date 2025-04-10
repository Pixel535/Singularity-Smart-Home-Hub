import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { MessageService } from 'primeng/api';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { CardModule } from 'primeng/card';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    InputTextModule,
    ButtonModule,
    ToastModule,
    CardModule,
    RouterModule
  ],
  providers: [MessageService]
})
export class RegisterComponent {
  loading = false;
  showPassword = false;
  showConfirmPassword = false;
  
  form: any;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private messageService: MessageService
  ) {
    this.form = this.fb.group({
      UserLogin: ['', Validators.required],
      Password: ['', [Validators.required, Validators.minLength(6)]],
      ConfirmPassword: ['', Validators.required],
      Mail: ['', [Validators.required, Validators.email]],
      TelephoneNumber: ['', Validators.required],
      Name: [''],
      Surname: ['']
    },
    {
      validators: this.passwordsMatchValidator
    }
  );
  }

  private passwordsMatchValidator(formGroup: any) {
    const password = formGroup.get('Password')?.value;
    const confirm = formGroup.get('ConfirmPassword')?.value;
    return password === confirm ? null : { passwordMismatch: true };
  }

  onSubmit() {
    if (this.form.invalid) return;

    const formData = { ...this.form.value };
    delete formData.ConfirmPassword;

    this.loading = true;

    this.auth.register(formData).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Registered',
          detail: 'Registered successfully'
        });
        this.router.navigate(['/login']);
      },
      error: err => {
        const detail = err?.error?.msg || 'Error with Registering';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
        this.loading = false;
      }
    });
  }
}
