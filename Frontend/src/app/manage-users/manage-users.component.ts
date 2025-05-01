import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HeaderComponent } from '../shared/header/header.component';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { DropdownModule } from 'primeng/dropdown';
import { DialogModule } from 'primeng/dialog';
import { EditRoleDialogComponent } from '../shared/edit-role-dialog/edit-role-dialog.component';
import { ConfirmDialogComponent } from '../shared/confirm-dialog/confirm-dialog.component';
import { environment } from '../../environments/environment';
import { InvitationService } from '../shared/invitation/invitation.service';

@Component({
  selector: 'app-manage-users',
  standalone: true,
  templateUrl: './manage-users.component.html',
  styleUrls: ['./manage-users.component.scss'],
  imports: [
    CommonModule,
    RouterModule,
    HeaderComponent,
    ReactiveFormsModule,
    ToastModule,
    ButtonModule,
    InputTextModule,
    DropdownModule,
    DialogModule,
    EditRoleDialogComponent,
    ConfirmDialogComponent
  ],
  providers: [MessageService]
})
export class ManageUsersComponent implements OnInit {
  private router = inject(Router);
  private http = inject(HttpClient);
  private fb = inject(FormBuilder);
  private messageService = inject(MessageService);
  private invitationService = inject(InvitationService);

  houseId!: number;
  houseName: string | null = null;
  from: 'dashboard' | 'info' = 'dashboard';
  baseUrl = `${environment.apiBaseUrl}/house`;

  loading = true;

  removeDialogVisible = false;
  userToRemove: any = null;

  users: any[] = [];
  roles = [
    { label: 'Owner', value: 'Owner' },
    { label: 'User', value: 'User' }
  ];

  searchResults: any[] = [];
  isSearching = false;
  hasSearched = false;
  selectedUser: any = null;


  addUserForm!: FormGroup;

  showEditDialog = false;
  editedUser: any = null;
  editedUserRole: string | null = null;

  ngOnInit(): void {
    const state = history.state;
    this.houseId = state.houseId;
    this.from = state.from || 'dashboard';
    this.houseName = state.houseName || null;

    this.initForm();
    this.loadUsers();
  }

  initForm() {
    this.addUserForm = this.fb.group({
      search: ['', Validators.required],
      role: [null, Validators.required]
    });
  }

  isInvalid(field: string): boolean {
    const control = this.addUserForm.get(field);
    return !!control && control.invalid && control.touched;
  }

  goBack() {
    const route = this.from === 'dashboard' ? '/dashboard' : '/house/info';
    this.router.navigate([route], {
      state: { houseId: this.houseId }
    });
  }

  loadUsers() {
    this.http
      .post<{ users: any[] }>(
        `${this.baseUrl}/getHouseUsers`,
        { HouseID: this.houseId },
        { withCredentials: true }
      )
      .subscribe({
        next: (res) => {
          this.users = res.users;
          this.loading = false;
        },
        error: err => {
          const detail = err?.error?.msg || 'Failed to load users.';
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail
          });
          this.users = [];
          this.loading = false;
        }
      });
  }

  searchUsers() {
    const query = this.addUserForm.get('search')?.value;
  
    if (!query || query.trim().length < 2) {
      this.searchResults = [];
      this.hasSearched = false;
      return;
    }
  
    this.isSearching = true;
    this.hasSearched = false;
  
    this.http.post<{ results: any[] }>(`${this.baseUrl}/searchUsersForHouse`, {
      query,
      HouseID: this.houseId
    }, { withCredentials: true }).subscribe({
      next: (res) => {
        this.searchResults = res.results || [];
        this.isSearching = false;
        this.hasSearched = true;
      },
      error: err => {
        const detail = err?.error?.msg || 'User search failed';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
        this.searchResults = [];
        this.isSearching = false;
        this.hasSearched = true;
      }
    });
  }
  
  
  
  addUser() {
    if (this.addUserForm.invalid) {
      this.addUserForm.markAllAsTouched();
      return;
    }
  
    const { search, role } = this.addUserForm.value;
  
    this.http.post(`${this.baseUrl}/addUserToHouse`, {
      HouseID: this.houseId,
      UserLogin: search,
      Role: role
    }, { withCredentials: true }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Invitation Sent',
          detail: `User "${search}" has been invited to join this house as "${role.value}".`
        });
        this.addUserForm.reset();
        this.searchResults = [];
        this.selectedUser = null;
        this.invitationService.notifyInvitationCreated();
      },
      error: (err) => {
        const detail = err?.error?.msg || 'Failed to send invitation.';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      }
    });
  }
  

  selectUser(user: any) {
    this.selectedUser = user;
    this.addUserForm.patchValue({ search: user.UserLogin });
    this.searchResults = [];
    this.hasSearched = false;
  }

  hideSearchDropdown() {
    setTimeout(() => {
      this.hasSearched = false;
    }, 150);
  }

  openEditRole(user: any) {
    this.editedUser = user;
    this.editedUserRole = user.Role;
    this.showEditDialog = true;
  }
  
  onDialogClosed() {
    this.showEditDialog = false;
    this.editedUser = null;
    this.editedUserRole = null;
  }
  
  onRoleChange(newRole: string) {
    if (!this.editedUser) return;
  
    const editedLogin = this.editedUser.UserLogin;
  
    this.http.put(`${this.baseUrl}/changeUserRole`, {
      HouseID: this.houseId,
      UserLogin: editedLogin,
      NewRole: newRole
    }, { withCredentials: true }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Role Updated',
          detail: `Role for "${editedLogin}" changed to "${newRole}".`
        });
        this.onDialogClosed();
        this.loadUsers();
      },
      error: (err) => {
        const detail = err?.error?.msg || 'Failed to update role.';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      }
    });
  }
  
  

  confirmRemove(user: any) {
    this.userToRemove = user;
    this.removeDialogVisible = true;
  }
  
  acceptRemove() {
    if (!this.userToRemove) return;
  
    const login = this.userToRemove.UserLogin;
  
    this.http.request('delete', `${this.baseUrl}/removeUserFromHouse`, {
      body: {
        HouseID: this.houseId,
        UserLogin: login
      },
      withCredentials: true
    }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'User Removed',
          detail: `User "${login}" removed from the house.`
        });
  
        this.loadUsers();
  
        this.removeDialogVisible = false;
        this.userToRemove = null;
      },
      error: (err) => {
        const detail = err?.error?.msg || 'Failed to remove user.';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      }
    });
  }
  
  

  cancelRemove() {
    this.removeDialogVisible = false;
    this.userToRemove = null;
  }
}
