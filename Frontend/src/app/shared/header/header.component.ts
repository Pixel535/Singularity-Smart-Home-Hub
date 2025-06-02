import { Component, Input, OnChanges, OnInit, OnDestroy, SimpleChanges, HostListener } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AuthService } from '../../auth/auth.service';
import { InvitationService } from '../../shared/invitation/invitation.service';
import { SpeechListenerService } from '../../speech/speech-listener.service';
import { io, Socket } from 'socket.io-client';
import { CommonModule } from '@angular/common';
import { MenubarModule } from 'primeng/menubar';
import { AvatarModule } from 'primeng/avatar';
import { TieredMenuModule } from 'primeng/tieredmenu';
import { ButtonModule } from 'primeng/button';
import { ChipModule } from 'primeng/chip';
import { SpeechService } from '../../speech/speech.service';

@Component({
  selector: 'app-header',
  standalone: true,
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  imports: [
    CommonModule,
    MenubarModule,
    AvatarModule,
    TieredMenuModule,
    ButtonModule,
    ChipModule
  ]
})
export class HeaderComponent implements OnInit, OnChanges, OnDestroy {
  @Input() houseName: string | null = null;
  @Input() isInsideHouse = false;
  @Input() houseId: number | null = null;
  @Input() userLogin: string | null = null;

  constructor(
  private auth: AuthService,
  private router: Router,
  private http: HttpClient,
  private invitationService: InvitationService,
  private speech: SpeechService,
  private listener: SpeechListenerService
) {}

  menuItems: any[] = [];
  houseMenuItems: any[] = [];
  notifications: any[] = [];
  showNotificationList = false;
  socket!: Socket;

  ngOnInit(): void {
    if (this.auth.isUserSession()) {
      this.connectSocket();
      this.loadNotifications();
      this.invitationService.onInvitationChanged().subscribe(() => {
        this.loadNotifications();
      });
    }
    this.listener.startListening();

    this.speech.onCommand().subscribe((command: string) => {
      if (command === 'logout' || command === 'log out') {
        this.logout();
      }
    });
  }

  ngOnDestroy(): void {
    this.socket?.disconnect();
  }

  checkIsUserSession(): boolean {
    return this.auth.isUserSession();
  }

  ngOnChanges(changes: SimpleChanges): void {
    const sessionType = this.auth.getSessionType();

    this.menuItems =
      sessionType === 'user'
        ? [
            {
              label: 'Profile',
              icon: 'pi pi-user',
              command: () => this.router.navigate(['/profile'])
            },
            {
              label: 'Log out',
              icon: 'pi pi-sign-out',
              command: () => this.logout()
            }
          ]
        : [
            {
              label: 'Log out',
              icon: 'pi pi-sign-out',
              command: () => this.logout()
            }
          ];

    this.houseMenuItems =
      this.isInsideHouse && this.houseId != null
        ? [
            {
              label: 'House Info',
              icon: 'pi pi-info-circle',
              command: () =>
                this.router.navigate(['/house/info'], {
                  state: { houseId: this.houseId }
                })
            }
          ]
        : [];
  }

  connectSocket(): void {
    this.auth.fetchAccessToken().subscribe({
      next: (token) => {
        this.socket = io(environment.socketUrl, {
          auth: { token },
          transports: ['websocket']
        });
  
        this.socket.on('connect', () => {
          console.log('[Socket] connected');
        });
  
        this.socket.on('invitation_created', (data) => {
          console.log('[Socket] invitation_created received');
          this.loadNotifications();
        });
  
        this.socket.on('disconnect', () => {
          console.log('[Socket] disconnected');
        });
  
        this.socket.on('connect_error', (err) => {
          console.error('[Socket] connection error:', err);
        });
      },
      error: () => {
        console.warn('[Socket] Could not fetch JWT token');
      }
    });
  }

  logout() {
    this.listener.stopListening();
    this.auth.logout();
  }

  goHome() {
    const sessionType = this.auth.getSessionType();
    if (sessionType === 'house' && this.houseId != null) {
      this.router.navigate(['/house/dashboard'], {
        state: { houseId: this.houseId }
      });
    } else {
      this.router.navigate(['/dashboard']);
    }
  }

  toggleNotifications(): void {
    this.showNotificationList = !this.showNotificationList;
  }

  @HostListener('document:click', ['$event'])
  onDocumentClick(event: MouseEvent): void {
    const target = event.target as HTMLElement;
    const clickedInside = target.closest('.notification-wrapper');
    if (!clickedInside) {
      this.showNotificationList = false;
    }
  }

  loadNotifications(): void {
    this.http
      .get<{ invitations: any[] }>(
        `${environment.apiBaseUrl}/house/getInvitations`,
        {
          withCredentials: true
        }
      )
      .subscribe({
        next: (res) => {
          this.notifications = res.invitations;
        },
        error: () => {
          this.notifications = [];
        }
      });
  }

  acceptInvitation(invitationId: string): void {
    this.http
      .post(
        `${environment.apiBaseUrl}/house/acceptInvitation`,
        { InvitationID: invitationId },
        { withCredentials: true }
      )
      .subscribe(() => {
        this.loadNotifications();
        this.invitationService.notifyInvitationAccepted();
      });
  }

  rejectInvitation(invitationId: string): void {
    this.http
      .post(
        `${environment.apiBaseUrl}/house/rejectInvitation`,
        { InvitationID: invitationId },
        { withCredentials: true }
      )
      .subscribe(() => {
        this.loadNotifications();
        this.invitationService.notifyInvitationRejected();
      });
  }
}
