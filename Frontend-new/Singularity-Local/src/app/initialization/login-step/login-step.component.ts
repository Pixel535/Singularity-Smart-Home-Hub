import { Component, EventEmitter, Output, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService } from '../../auth/auth.service';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-login-step',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    ButtonModule,
    InputTextModule,
    ToastModule
  ],
  providers: [MessageService],
  templateUrl: './login-step.component.html',
  styleUrls: ['./login-step.component.scss']
})
export class LoginStepComponent {
  @Output() loggedIn = new EventEmitter<void>();

  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private toast = inject(MessageService);

  form: FormGroup = this.fb.group({
    UserLogin: ['', [Validators.required]],
    Password: ['', Validators.required]
  });

  submitted = false;
  loading = false;
  errorMessage: string | null = null;
  showPassword = false;

  onSubmit() {
    this.submitted = true;
    this.errorMessage = null;

    if (this.form.invalid) return;

    this.loading = true;

    this.auth.loginUser(this.form.value).subscribe({
      next: () => {
        this.loading = false;
        this.loggedIn.emit();
        this.toast.add({
          severity: 'success',
          summary: 'Login successful',
          detail: 'You are now signed in',
          life: 3000
        });
      },
      error: (err) => {
        this.loading = false;
        const msg = err?.error?.msg || 'Invalid UserLogin or Password.';
        this.errorMessage = msg;

        this.toast.add({
          severity: 'error',
          summary: 'Login failed',
          detail: msg,
          life: 4000
        });
      }
    });
  }
}
