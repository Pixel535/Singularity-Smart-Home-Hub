import { Component, EventEmitter, Output, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-set-pin-step',
  standalone: true,
  imports: [CommonModule, ButtonModule, CardModule, ToastModule],
  providers: [MessageService],
  templateUrl: './set-pin-step.component.html',
  styleUrls: ['./set-pin-step.component.scss']
})
export class SetPinStepComponent {
  @Output() completed = new EventEmitter<{ pin: string }>();

  stage: 'pin' | 'confirm' = 'pin';
  pin = '';
  confirmPin = '';
  error: string | null = null;

  private toast = inject(MessageService);

  handleDigitClick(digit: string) {
    if (this.stage === 'pin' && this.pin.length < 6) {
      this.pin += digit;
    } else if (this.stage === 'confirm' && this.confirmPin.length < 6) {
      this.confirmPin += digit;
    }
  }

  handleBackspace() {
    if (this.stage === 'pin' && this.pin.length > 0) {
      this.pin = this.pin.slice(0, -1);
    } else if (this.stage === 'confirm' && this.confirmPin.length > 0) {
      this.confirmPin = this.confirmPin.slice(0, -1);
    }
  }

  goToConfirm() {
    if (this.pin.length === 6) {
      this.stage = 'confirm';
      this.error = null;
    } else {
      this.showError('PIN must be 6 digits');
    }
  }

  submit() {
    if (this.confirmPin.length !== 6) {
      this.showError('Confirmation PIN must be 6 digits.');
      return;
    }

    if (this.pin !== this.confirmPin) {
      this.showError('PINs do not match.');
      return;
    }

    this.error = null;
    this.completed.emit({ pin: this.pin });

    this.pin = '';
    this.confirmPin = '';
    this.stage = 'pin';
  }

  private showError(message: string) {
    this.error = message;
    this.toast.add({
      severity: 'error',
      summary: 'PIN Error',
      detail: message,
      life: 4000
    });
  }
}
