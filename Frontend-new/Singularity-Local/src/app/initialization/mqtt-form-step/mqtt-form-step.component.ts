import { Component, EventEmitter, Output } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { ToastModule } from 'primeng/toast';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-mqtt-step',
  standalone: true,
  templateUrl: './mqtt-form-step.component.html',
  styleUrls: ['./mqtt-form-step.component.scss'],
  providers: [MessageService],
  imports: [
    ReactiveFormsModule,
    CommonModule,
    InputTextModule,
    ButtonModule,
    ToastModule
  ],
})
export class MqttStepComponent {
  @Output() completed = new EventEmitter<{ username: string; password: string }>();
  @Output() back = new EventEmitter<void>();
  showBack = true;

  form!: FormGroup;
  submitted = false;
  loading = false;
  showPassword = false;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      repeatPassword: ['', Validators.required],
    });
  }

  submit() {
    this.submitted = true;

    if (this.form.invalid) return;

    const { password, repeatPassword } = this.form.value;
    if (password !== repeatPassword) {
      this.form.get('repeatPassword')?.setErrors({ mismatch: true });
      return;
    }

    this.loading = true;

    this.completed.emit({
      username: this.form.value.username!,
      password: this.form.value.password!
    });

    this.loading = false;
  }

  goBack() {
    this.back.emit();
  }
}
