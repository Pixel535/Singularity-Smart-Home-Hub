import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { HeaderComponent } from '../shared/header/header.component';
import { ConfirmDialogComponent } from '../shared/confirm-dialog/confirm-dialog.component';
import { MessageService } from 'primeng/api';
import { AuthService } from '../auth/auth.service';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { ToastModule } from 'primeng/toast';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    HeaderComponent,
    ConfirmDialogComponent,
    CardModule,
    ButtonModule,
    InputTextModule,
    ToastModule,
    ReactiveFormsModule
  ],
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss'],
  providers: [MessageService]
})
export class ProfileComponent implements OnInit {
  private http = inject(HttpClient);
  private auth = inject(AuthService);
  private messageService = inject(MessageService);
  private fb = inject(FormBuilder);
  private router = inject(Router);
  private route = inject(ActivatedRoute);

  private baseUrl = `${environment.apiBaseUrl}/profile`;

  userLogin: string | null = null;
  userData: any = null;
  loading = true;
  isEditing = false;
  showConfirm = false;

  profileForm!: FormGroup;

  ngOnInit(): void {
    this.auth.getUser().subscribe({
      next: (res) => {
        this.userLogin = res.session === 'user' ? res.userLogin ?? null : null;
      },
      error: () => {
        this.userLogin = null;
      }
    });
    this.http.get<{ user: any }>(`${this.baseUrl}/getProfile`, { withCredentials: true }).subscribe({
      next: (res) => {
        this.userData = res.user;
        this.userLogin = this.userData.UserLogin
        this.initForm(this.userData);
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        this.userLogin = null;
      }
    });
  }

  initForm(data: any) {
    this.profileForm = this.fb.group({
      Name: [data.Name, Validators.required],
      Surname: [data.Surname, Validators.required],
      Mail: [data.Mail, [Validators.required, Validators.email]],
      TelephoneNumber: [data.TelephoneNumber, Validators.required]
    });
  }

  onEditProfile() {
    this.isEditing = true;
  }

  cancelEdit() {
    this.isEditing = false;
    this.profileForm.reset(this.userData);
  }

  saveProfile() {
    if (this.profileForm.invalid) return;

    this.http.put(`${this.baseUrl}/editProfile`, this.profileForm.value, { withCredentials: true }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Profile Updated',
          detail: 'Your profile has been updated.'
        });
        this.isEditing = false;
        Object.assign(this.userData, this.profileForm.value);
      },
      error: err => {
        const detail = err?.error?.msg || 'Failed to update profile';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      }
    });
  }
  
  onDeleteAccount() {
    this.showConfirm = true;
  }

  confirmDelete() {
    this.http.delete(`${this.baseUrl}/deleteProfile`, { withCredentials: true }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Account deleted',
          detail: 'Your account has been successfully deleted.'
        });
        this.auth.logout();
      },
      error: err => {
        const detail = err?.error?.msg || 'Failed to delete account';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      }
    });
  }

  cancelDelete() {
    this.showConfirm = false;
  }

  onChangePassword() {
    this.router.navigate(['/profile/changePassword']);
  }

  isInvalid(fieldName: string): boolean {
    const control = this.profileForm.get(fieldName);
    return !!control && control.invalid && control.touched;
  }
  
}
