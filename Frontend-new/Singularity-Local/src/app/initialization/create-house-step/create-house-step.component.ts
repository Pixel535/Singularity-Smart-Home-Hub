import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators, FormGroup } from '@angular/forms';
import { DropdownModule } from 'primeng/dropdown';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { COUNTRIES } from '../../../shared/countries';

@Component({
  selector: 'app-create-house-step',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    DropdownModule,
    InputTextModule,
    ButtonModule,
  ],
  templateUrl: './create-house-step.component.html',
  styleUrls: ['./create-house-step.component.scss']
})
export class CreateHouseStepComponent implements OnInit {
  @Output() completed = new EventEmitter<any>();
  @Output() back = new EventEmitter<void>();
  showBack = true;

  countries = COUNTRIES;
  form!: FormGroup;

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.form = this.fb.group({
      HouseName: ['', Validators.required],
      Country: [null, Validators.required],
      City: ['', Validators.required],
      StreetAddress: ['', Validators.required],
      PostalCode: ['', Validators.required]
    });
  }

  isInvalid(control: string): boolean {
    const c = this.form.get(control);
    return !!c && c.invalid && (c.dirty || c.touched);
  }

  continue() {
    const raw = this.form.value;
    const data = {
      HouseName: raw.HouseName,
      City: raw.City,
      StreetAddress: raw.StreetAddress,
      PostalCode: raw.PostalCode,
      Country: raw.Country?.name,
      CountryCode: raw.Country?.code
    };
    this.completed.emit(data);
  }

  goBack() {
    this.back.emit();
  }
}
