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
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
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
export class LoginComponent {
  loading = false;
  showPassword = false;

  form: any;

  constructor(
    private fb: FormBuilder,
    private auth: AuthService,
    private router: Router,
    private messageService: MessageService
  ) {
    this.form = this.fb.group({
    UserLogin: ['', Validators.required],
    Password: ['', Validators.required]
  });
}

  onSubmit() {
    if (this.form.invalid) return;
  
    const { UserLogin, Password } = this.form.value;
  
    if (!UserLogin || !Password) return;
  
    this.loading = true;
  
    this.auth.login({ UserLogin, Password }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Logged in',
          detail: 'Logged in successfully'
        });
        this.router.navigate(['/dashboard']);
      },
      error: err => {
        const detail = err?.error?.msg || 'Error with login';
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
