import { Component, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Dialog, DialogModule } from 'primeng/dialog';
import { ButtonModule } from 'primeng/button';
import { DropdownModule } from 'primeng/dropdown';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-edit-role-dialog',
  standalone: true,
  imports: [CommonModule, DialogModule, ButtonModule, DropdownModule, FormsModule],
  templateUrl: './edit-role-dialog.component.html',
  styleUrls: ['./edit-role-dialog.component.scss']
})
export class EditRoleDialogComponent {
  @Input() visible = false;
  @Input() currentRole: string | null = null;
  @Input() userLogin: string | null = null;

  @Output() confirm = new EventEmitter<string>();
  @Output() cancel = new EventEmitter<void>();
  @Output() closed = new EventEmitter<void>();

  @ViewChild('customDialog') customDialogRef!: Dialog;

  availableRoles = [
    { label: 'Owner', value: 'Owner' },
    { label: 'User', value: 'User' }
  ];

  handleClickOutside(event: MouseEvent) {
    const dialogEl = this.customDialogRef?.el?.nativeElement?.querySelector('.p-dialog');
    if (dialogEl && !dialogEl.contains(event.target as HTMLElement)) {
      this.closed.emit();
    }
  }

  onConfirm() {
    if (this.currentRole) {
      this.confirm.emit(this.currentRole);
      this.closed.emit();
    }
  }

  onCancel() {
    this.cancel.emit();
    this.closed.emit();
  }
}
