import { Component, OnInit, AfterViewInit, ViewChildren, ElementRef, QueryList, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HeaderComponent } from '../shared/header/header.component';
import { ConfirmDialogComponent } from '../shared/confirm-dialog/confirm-dialog.component';
import { AuthService } from '../auth/auth.service';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';
import { AvatarModule } from 'primeng/avatar';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { MenubarModule } from 'primeng/menubar';
import { ChipModule } from 'primeng/chip';
import { TooltipModule } from 'primeng/tooltip';
import { SpeechService } from '../speech/speech.service';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-house-dashboard',
  standalone: true,
  templateUrl: './house-dashboard.component.html',
  styleUrls: ['./house-dashboard.component.scss'],
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    ButtonModule,
    InputTextModule,
    ToastModule,
    HeaderComponent,
    ConfirmDialogComponent,
    MenubarModule,
    AvatarModule,
    TieredMenuModule,
    ChipModule,
    TooltipModule
  ],
  providers: [MessageService]
})
export class HouseDashboardComponent implements OnInit, AfterViewInit {
  private router = inject(Router);
  private route = inject(Router);
  private http = inject(HttpClient);
  private cdr = inject(ChangeDetectorRef);
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private messageService = inject(MessageService);
  private speech = inject(SpeechService);

  houseId!: number;
  houseName = '';
  userRole: string = '';
  loading = true;
  isEditing = false;
  editingRoomId: number | null = null;
  
  rooms: any[] = [];
  devices: any[] = [];

  showAddForm = false;
  addRoomForm!: FormGroup;

  activeTab: 'rooms' | 'devices' | 'functions' = 'rooms';
  showDeleteConfirm = false;
  selectedRoomToDelete: any = null;

  baseUrl = `${environment.apiBaseUrl}/house`;

  @ViewChildren('tabItem') tabItems!: QueryList<ElementRef>;
  tabIndicatorStyle = {
    left: '0px',
    width: '0px'
  };

  ngOnInit(): void {
    this.auth.startIdleWatch();
  
    const state = history.state;
    if (state && state.houseId) {
      this.houseId = state.houseId;
  
      const greetedKey = `houseGreeted:${this.houseId}`;
      if (!sessionStorage.getItem(greetedKey)) {
        this.speech.playGreeting(this.houseId);
        sessionStorage.setItem(greetedKey, 'true');
      }
  
      this.loadHouseData();
    } else {
      this.messageService.add({
        severity: 'error',
        summary: 'Missing Data',
        detail: 'No house ID was provided. Redirecting to dashboard...'
      });
      this.router.navigate(['/dashboard']);
    }
  
    this.addRoomForm = this.fb.group({
      RoomName: ['', Validators.required]
    });
  }
  
  
  
  isOwner(): boolean {
    return this.auth.isHouseSession() || this.userRole === 'Owner';
  }
  

  toggleEditForm(room: any) {
    this.showAddForm = true;
    this.isEditing = true;
    this.editingRoomId = room.RoomID;
    this.addRoomForm.patchValue({ RoomName: room.RoomName });
  }
  
  closeForm(event: MouseEvent) {
    if ((event.target as HTMLElement).classList.contains('overlay')) {
      this.toggleAddForm();
    }
  }

  ngAfterViewInit(): void {
    this.tabItems.changes.subscribe(() => this.safeUpdateIndicator());
    setTimeout(() => this.safeUpdateIndicator());
  }

  private safeUpdateIndicator(): void {
    setTimeout(() => {
      this.updateIndicator();
      this.cdr.detectChanges();
    });
  }

  setTab(tab: 'rooms' | 'devices' | 'functions') {
    this.activeTab = tab;
    this.updateIndicator();
  }

  updateIndicator() {
    if (!this.tabItems || !this.tabItems.length) return;

    const indexMap = {
      'rooms': 0,
      'devices': 1,
      'functions': 2
    };

    const index = indexMap[this.activeTab];
    const tabEl = this.tabItems.get(index)?.nativeElement;
    if (tabEl) {
      const left = tabEl.offsetLeft;
      const width = tabEl.getBoundingClientRect().width;
      this.tabIndicatorStyle = {
        left: `${left}px`,
        width: `${width}px`
      };
    }
  }

  toggleAddForm() {
    this.showAddForm = !this.showAddForm;
  
    if (!this.showAddForm) {
      this.addRoomForm.reset();
      this.isEditing = false;
      this.editingRoomId = null;
    }
  }

  isInvalid(fieldName: string): boolean {
    const control = this.addRoomForm.get(fieldName);
    return !!control && control.invalid && control.touched;
  }

  submitAddRoom() {
    if (this.addRoomForm.invalid) return;
  
    const payload = {
      HouseID: this.houseId,
      RoomName: this.addRoomForm.value.RoomName
    };
  
    const endpoint = this.isEditing
      ? `${this.baseUrl}/editRoom`
      : `${this.baseUrl}/addRoom`;
  
    const body = this.isEditing
      ? { ...payload, RoomID: this.editingRoomId }
      : payload;
  
    const request = this.isEditing
      ? this.http.put(endpoint, body, { withCredentials: true })
      : this.http.post(endpoint, body, { withCredentials: true });
  
    request.subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: this.isEditing ? 'Room Updated' : 'Room Added',
          detail: this.isEditing
            ? 'Room updated successfully.'
            : 'Room added successfully.'
        });
        this.toggleAddForm();
        this.loadRooms();
      },
      error: (err) => {
        const detail = err?.error?.msg || (
          this.isEditing
            ? 'Failed to update room.'
            : 'Failed to add room.'
        );
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      }
    });
  }

  confirmDeleteRoom(room: any) {
    this.selectedRoomToDelete = room;
    this.showDeleteConfirm = true;
  }

  acceptDeleteRoom() {
    if (!this.selectedRoomToDelete) return;
  
    this.http.request('delete', `${this.baseUrl}/removeRoom`, {
      body: {
        RoomID: this.selectedRoomToDelete.RoomID,
        HouseID: this.houseId
      },
      withCredentials: true
    }).subscribe({
      next: () => {
        this.messageService.add({
          severity: 'success',
          summary: 'Deleted',
          detail: 'Room has been removed.'
        });
        this.loadRooms();
      },
      error: err => {
        const detail = err?.error?.msg || 'Failed to delete room';
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail
        });
      },
      complete: () => {
        this.showDeleteConfirm = false;
        this.selectedRoomToDelete = null;
      }
    });
  }

  cancelDeleteRoom() {
    this.showDeleteConfirm = false;
    this.selectedRoomToDelete = null;
  }

  loadHouseData() {
    this.http.post<any>(`${this.baseUrl}/getHouse`, { HouseID: this.houseId }, { withCredentials: true })
      .subscribe({
        next: (res) => {
          this.houseName = res.HouseName;
          this.userRole = res.Role;
          this.loadRooms();
        },
        error: err => {
          const detail = err?.error?.msg || 'Failed to load house data';
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail
          });
        }
      });
  }

  loadRooms() {
    this.http.post<{ rooms: any[] }>(`${this.baseUrl}/getRooms`, { HouseID: this.houseId }, { withCredentials: true })
      .subscribe({
        next: (res) => {
          this.rooms = res.rooms;
        },
        error: err => {
          const detail = err?.error?.msg || 'Failed to load rooms';
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail
          });
        },
        complete: () => {
          this.loading = false;
        }
      });
  }

  goToRoom(roomId: number) {
    this.router.navigate(['/house/room/dashboard'], {
      state: {
        roomId,
        houseId: this.houseId
      }
    });
  }

}
