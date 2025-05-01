import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../auth/auth.service';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from 'primeng/avatar';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { ButtonModule } from 'primeng/button';
import { ChipModule } from 'primeng/chip';
import { HeaderComponent } from '../shared/header/header.component';
import { InputTextModule } from 'primeng/inputtext';
import { TooltipModule } from 'primeng/tooltip';
import { DropdownModule } from 'primeng/dropdown';
import { COUNTRIES } from '../shared/countries';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { ConfirmDialogComponent } from '../shared/confirm-dialog/confirm-dialog.component';
import { environment } from '../../environments/environment';
import { InvitationService } from '../shared/invitation/invitation.service'

@Component({
  standalone: true,
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  imports: [
    CommonModule,
    RouterModule,
    MenubarModule,
    AvatarModule,
    TieredMenuModule,
    ButtonModule,
    ChipModule,
    HeaderComponent,
    InputTextModule,
    ReactiveFormsModule,
    TooltipModule,
    DropdownModule,
    ToastModule,
    ConfirmDialogComponent
  ],
  providers: [MessageService]
})
export class DashboardComponent implements OnInit {
  private baseUrl = `${environment.apiBaseUrl}/dashboard`;
  private homeUrl = `${environment.apiBaseUrl}/home`;
  private auth = inject(AuthService);
  private router = inject(Router);
  private http = inject(HttpClient);
  private fb = inject(FormBuilder);
  private messageService = inject(MessageService);
  private invitationService = inject(InvitationService);

  userLogin: string | null = null;
  houses: any[] = [];
  loading = true;
  showAddForm = false;
  countries = COUNTRIES;
  isEditing = false;
  editingHouseId: number | null = null;
  showDeleteConfirm = false;
  selectedHouseToDelete: any = null;
  showPin = false;

  addHouseForm!: FormGroup;

  ngOnInit(): void {
    this.auth.startIdleWatch();
    this.auth.getUser().subscribe({
      next: (res) => {
        this.userLogin = res.session === 'user' ? res.userLogin ?? null : null;
      },
      error: () => {
        this.userLogin = null;
      }
    });
    this.fetchHouses();

    this.addHouseForm = this.fb.group({
      HouseName: ['', Validators.required],
      Country: ['', Validators.required],
      City: ['', Validators.required],
      StreetAddress: ['', Validators.required],
      PostalCode: ['', Validators.required],
      PIN: ['', [
        Validators.required,
        Validators.pattern(/^\d{6}$/)
      ]]
    });
    this.invitationService.onInvitationChanged().subscribe(() => {
      this.fetchHouses();
    });
  }

  fetchHouses() {
    this.http.get<{ houses: any[] }>(`${this.baseUrl}/houses`).subscribe({
      next: (res) => {
        this.houses = res.houses;
        this.loading = false;
      },
      error: err => {
        const detail = err?.error?.msg || 'Failed to load houses.';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
        this.auth.logout();
      }
    });
  }

  isOwner(house: any): boolean {
    return house.Role === 'Owner';
  }

  toggleAddForm(house: any = null) {
    this.showAddForm = !this.showAddForm;
  
    if (this.showAddForm && house) {
      this.isEditing = true;
      this.editingHouseId = house.HouseID;
  
      const selectedCountry = this.countries.find(c => c.code === house.CountryCode);
      this.addHouseForm.patchValue({
        HouseName: house.HouseName,
        Country: selectedCountry || null,
        City: house.City,
        StreetAddress: house.StreetAddress,
        PostalCode: house.PostalCode,
        PIN: '******'
      });
  
      this.addHouseForm.get('PIN')?.clearValidators();
      this.addHouseForm.get('PIN')?.updateValueAndValidity();
  
    } else {
      this.isEditing = false;
      this.editingHouseId = null;
      this.addHouseForm.reset();
  
      this.addHouseForm.get('PIN')?.setValidators([
        Validators.required,
        Validators.pattern(/^\d{6}$/)
      ]);
      this.addHouseForm.get('PIN')?.updateValueAndValidity();
    }
  }
  

  closeForm(event: MouseEvent) {
    if ((event.target as HTMLElement).classList.contains('overlay')) {
      this.toggleAddForm();
    }
  }

  submitAddHouse() {
    if (this.addHouseForm.invalid) return;
  
    const payload = this.addHouseForm.value;

    if (this.isEditing) {
      delete payload.PIN;
    }
  
    const endpoint = this.isEditing
      ? `${this.baseUrl}/editHouse`
      : `${this.baseUrl}/addHouse`;
  
    const request = this.isEditing
      ? this.http.put(endpoint, { HouseID: this.editingHouseId, ...payload })
      : this.http.post(endpoint, payload);
  
    request.subscribe({
      next: () => {
        this.toggleAddForm();
        this.fetchHouses();
        this.messageService.add({
          severity: 'success',
          summary: this.isEditing ? 'House Updated' : 'House Added',
          detail: this.isEditing
            ? 'House updated successfully.'
            : 'House added successfully.'
        });
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

  isInvalid(fieldName: string): boolean {
    const control = this.addHouseForm.get(fieldName);
    return !!control && control.invalid && control.touched;
  }

  confirmDelete(house: any) {
    this.selectedHouseToDelete = house;
    this.showDeleteConfirm = true;
  }
  
  acceptDelete() {
    if (!this.selectedHouseToDelete) return;
    this.deleteHouse(this.selectedHouseToDelete.HouseID);
  }
  
  closeDeleteDialog() {
    this.showDeleteConfirm = false;
    this.selectedHouseToDelete = null;
  }

  deleteHouse(houseId: number) {
    this.http.request('delete', `${this.baseUrl}/removeHouse`, {
      body: { HouseID: houseId },
      withCredentials: true
    }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Deleted',
          detail: `House ${houseId} has been removed.`
        });
        this.fetchHouses();
      },
      error: err => {
        const detail = err?.error?.msg || 'Failed to delete the house.';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      }
    });
  }

  goToManageUsers(houseId: number, houseName: string) {
    this.router.navigate(['/house/manageUsers'], {
      state: {
        houseId,
        houseName,
        from: 'dashboard'
      }
    });
  }

  goToHouseDashboard(houseId: number) {
    this.router.navigate(['/house/dashboard'], {
      state: { houseId }
    });
  }
  
  goToChangePin() {
    if (this.editingHouseId) {
      this.router.navigate(['/house/changePin'], {
        state: {
          houseId: this.editingHouseId,
          from: 'dashboard'
        }
      });
    }
  }

}
