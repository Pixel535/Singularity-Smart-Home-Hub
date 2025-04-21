import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../auth/auth.service';
import { MessageService } from 'primeng/api';
import { HeaderComponent } from '../shared/header/header.component';
import { ConfirmDialogComponent } from '../shared/confirm-dialog/confirm-dialog.component';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { DividerModule } from 'primeng/divider';
import { ToastModule } from 'primeng/toast';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { COUNTRIES } from '../shared/countries';

@Component({
  selector: 'app-house-info',
  standalone: true,
  templateUrl: './house-info.component.html',
  styleUrls: ['./house-info.component.scss'],
  imports: [
    CommonModule,
    RouterModule,
    HeaderComponent,
    ConfirmDialogComponent,
    ReactiveFormsModule,
    ButtonModule,
    CardModule,
    InputTextModule,
    DividerModule,
    ToastModule,
    DropdownModule
  ],
  providers: [MessageService]
})
export class HouseInfoComponent implements OnInit {
  private router = inject(Router);
  private http = inject(HttpClient);
  private auth = inject(AuthService);
  private fb = inject(FormBuilder);
  private messageService = inject(MessageService);

  private houseBase = 'http://localhost:5000/house';
  private dashBase = 'http://localhost:5000/dashboard';

  houseId!: number;
  houseData: any = null;
  users: any[] = [];
  userRole: string = '';
  loading = true;
  isEditing = false;
  showDeleteConfirm = false;

  houseForm!: FormGroup;
  countries = COUNTRIES;

  ngOnInit(): void {
    this.auth.startIdleWatch();

    const state = history.state;
    if (!state?.houseId) {
      this.messageService.add({
        severity: 'error',
        summary: 'Missing data',
        detail: 'No house ID provided. Redirecting to dashboard...'
      });
      this.router.navigate(['/dashboard']);
      return;
    }
    this.houseId = state.houseId;

    Promise.all([this.loadHouse(), this.loadUsers()]).then(() => {
      this.loading = false;
    });
  }

  isOwner(): boolean {
    return this.userRole === 'Owner';
  }

  private loadHouse(): Promise<void> {
    return new Promise((resolve) => {
      this.http
        .post<any>(`${this.houseBase}/getHouse`, { HouseID: this.houseId }, { withCredentials: true })
        .subscribe({
          next: (res) => {
            this.houseData = res;
            this.userRole = res.Role;
            this.initForm();
            resolve();
          },
          error: (err) => {
            const detail = err?.error?.msg || 'Failed to fetch house data';
            this.messageService.add({ severity: 'error', summary: 'Error', detail });
            this.router.navigate(['/dashboard']);
            resolve();
          }
        });
    });
  }
  
  private loadUsers(): Promise<void> {
    return new Promise((resolve) => {
      this.http
        .post<{ users: any[] }>(`${this.houseBase}/getHouseUsers`, { HouseID: this.houseId }, { withCredentials: true })
        .subscribe({
          next: (res) => {
            this.users = res.users;
            resolve();
          },
          error: () => {
            this.users = [];
            resolve();
          }
        });
    });
  }

  initForm() {
    const h = this.houseData;
    const selectedCountry = this.countries.find(c => c.code === h.CountryCode);

    this.houseForm = this.fb.group({
      HouseName: [h.HouseName, Validators.required],
      Country: [selectedCountry || null, Validators.required],
      City: [h.City, Validators.required],
      StreetAddress: [h.StreetAddress, Validators.required],
      PostalCode: [h.PostalCode, Validators.required],
      PIN: [h.PIN, [Validators.required, Validators.pattern(/^\d{6}$/)]]
    });
  }

  startEdit() {
    this.isEditing = true;
  }

  cancelEdit() {
    this.isEditing = false;
    this.initForm();
  }

  saveHouse() {
    if (this.houseForm.invalid) return;

    const payload = {
      HouseID: this.houseId,
      ...this.houseForm.value
    };

    this.http.put(`${this.dashBase}/editHouse`, payload, {
      withCredentials: true
    }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'House Updated',
          detail: 'House updated successfully.'
        });

        this.houseData = {
          ...this.houseData,
          ...payload,
          Country: payload.Country.name,
          CountryCode: payload.Country.code
        };

        this.isEditing = false;
      },
      error: (err) => {
        const detail = err?.error?.msg || 'Something went wrong.';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      }
    });
  }

  deleteHouse() {
    this.showDeleteConfirm = true;
  }

  acceptDelete() {
    this.http
      .request('delete', `${this.dashBase}/removeHouse`, {
        body: { HouseID: this.houseId },
        withCredentials: true
      })
      .subscribe({
        next: () => {
          this.messageService.add({
            severity: 'success',
            summary: 'Deleted',
            detail: 'House has been deleted.'
          });
          this.router.navigate(['/dashboard']);
        },
        error: err => {
          const detail = err?.error?.msg || 'Failed to delete house';
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail
          });
        }
      });
  }

  goToManageUsers(houseId: number) {
    this.router.navigate(['/house/manageUsers'], {
      state: {
        houseId,
        houseName: this.houseData?.HouseName,
        from: 'info'
      }
    });
  }

  isInvalid(fieldName: string): boolean {
    const control = this.houseForm.get(fieldName);
    return !!control && control.invalid && control.touched;
  }

  goBackToHouseDashboard() {
    this.router.navigate(['/house/dashboard'], {
      state: { houseId: this.houseId }
    });
  }
}
