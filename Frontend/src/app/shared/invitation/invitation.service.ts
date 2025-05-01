import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export type InvitationEvent = 'created' | 'accepted' | 'rejected';

@Injectable({ providedIn: 'root' })
export class InvitationService {
  private invitationChanged$ = new Subject<InvitationEvent>();

  onInvitationChanged() {
    return this.invitationChanged$.asObservable();
  }

  notifyInvitationCreated() {
    this.invitationChanged$.next('created');
  }

  notifyInvitationAccepted() {
    this.invitationChanged$.next('accepted');
  }

  notifyInvitationRejected() {
    this.invitationChanged$.next('rejected');
  }
}
