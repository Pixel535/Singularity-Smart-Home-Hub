import { Component, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Dialog, DialogModule } from 'primeng/dialog';
import { ButtonModule } from 'primeng/button';

@Component({
  selector: 'app-confirm-dialog',
  standalone: true,
  imports: [CommonModule, DialogModule, ButtonModule],
  templateUrl: './confirm-dialog.component.html',
  styleUrls: ['./confirm-dialog.component.scss']
})
export class ConfirmDialogComponent {
  @Input() visible = false;
  @Input() header = 'Confirmation';
  @Input() message = 'Are you sure?';
  @Input() identifier: string | number | null = null;

  @Output() accept = new EventEmitter<void>();
  @Output() reject = new EventEmitter<void>();
  @Output() closed = new EventEmitter<void>();

  @ViewChild('customDialog') customDialogRef!: Dialog;

  handleClickOutside(event: MouseEvent) {
    const dialogEl = this.customDialogRef?.el?.nativeElement?.querySelector('.p-dialog');
    if (dialogEl && !dialogEl.contains(event.target as HTMLElement)) {
      this.closed.emit();
    }
  }

  onAccept() {
    this.accept.emit();
    this.closed.emit();
  }

  onReject() {
    this.reject.emit();
    this.closed.emit();
  }
}
