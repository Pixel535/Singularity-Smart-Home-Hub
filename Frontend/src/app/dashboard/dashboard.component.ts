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
import { SpeechService } from '../speech/speech.service';

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
  private speech = inject(SpeechService);

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
  voiceWizardActive = false;
  voiceWizardStepIndex = 0;
  voiceWizardSteps = ['HouseName', 'Country', 'City', 'StreetAddress', 'PostalCode', 'PIN'];
  waitingForSubmissionConfirm = false;
pendingDeleteHouseName: string | null = null;

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

    this.speech.onCommand().subscribe(command => {
      if (this.voiceWizardActive) {
        this.handleWizardResponse(command);
      } else {
        this.handleSpeechCommand(command);
      }
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

    if (!this.showAddForm) {
      this.voiceWizardActive = false;
      this.waitingForSubmissionConfirm = false;
      return;
    }
  
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
    console.log("TAL KSEJTM");
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

handleSpeechCommand(command: string): void {
  const lower = command.toLowerCase().trim();

  if (this.pendingDeleteHouseName && (lower === 'yes' || lower === 'no')) {
    if (lower === 'yes' && this.selectedHouseToDelete) {
      this.acceptDelete();
      this.closeDeleteDialog();
    } else {
      this.playTTS('Okay, cancelled.');
      this.closeDeleteDialog();
    }
    this.pendingDeleteHouseName = null;
    return;
  }

  if (lower === 'new house' || lower === 'add house') {
    this.toggleAddForm();
    setTimeout(() => this.startVoiceWizard(), 500);
    return;
  }

  if (lower === 'close form' || lower === 'cancel') {
    if (this.showAddForm) {
      this.playTTS('Closing the form');
      this.toggleAddForm();
    } else {
      this.playTTS('The form is already closed');
    }
    return;
  }

  if (lower.startsWith('go to house')) {
    let spokenName = lower.replace('go to house', '').trim();
    spokenName = this.normalizeNumberWords(spokenName).toLowerCase();

    const matched = this.houses.find(h => 
      this.normalizeNumberWords(h.HouseName.toLowerCase()) === spokenName
    );
  
    if (matched) {
      this.goToHouseDashboard(matched.HouseID);
    } else {
      this.playTTS(`Sorry, I couldn't find house named ${spokenName}`);
    }
    return;
  }

  if (lower.startsWith('delete house')) {
    let spokenName = lower.replace('delete house', '').trim();
    spokenName = this.normalizeNumberWords(spokenName).toLowerCase();

    const matched = this.houses.find(h => 
      this.normalizeNumberWords(h.HouseName.toLowerCase()) === spokenName
    );

    if (matched) {
      this.confirmDelete(matched);
      this.playTTS(`Are you sure you want to delete house ${matched.HouseName}? Say yes or no.`);
      this.pendingDeleteHouseName = matched.HouseName;
    } else {
      this.playTTS(`Sorry, I couldn't find house named ${spokenName}`);
    }
    return;
  }
}


  playTTS(text: string): void {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  }

  normalizeNumberWords(text: string): string {
    const numbersMap: { [key: string]: string } = {
      'zero': '0',
      'one': '1',
      'two': '2',
      'three': '3',
      'four': '4',
      'five': '5',
      'six': '6',
      'seven': '7',
      'eight': '8',
      'nine': '9'
    };

    const parts = text.split(' ');
    const result: string[] = [];

    let numberBuffer = '';

    for (const word of parts) {
      if (word in numbersMap) {
        numberBuffer += numbersMap[word];
      } else {
        if (numberBuffer.length) {
          result.push(numberBuffer);
          numberBuffer = '';
        }
        result.push(word);
      }
    }

    if (numberBuffer.length) {
      result.push(numberBuffer);
    }

    return result.join(' ');
  }

  startVoiceWizard(): void {
    this.voiceWizardActive = true;
    this.voiceWizardStepIndex = 0;
    this.askCurrentQuestion();
  }

  askCurrentQuestion(): void {
    const step = this.voiceWizardSteps[this.voiceWizardStepIndex];
    let question = '';

    switch (step) {
      case 'HouseName':
        question = 'What is your house name?';
        break;
      case 'Country':
        question = 'What is your country?';
        break;
      case 'City':
        question = 'What city is it in?';
        break;
      case 'StreetAddress':
        question = 'What is the street address?';
        break;
      case 'PostalCode':
        question = 'What is the postal code?';
        break;
      case 'PIN':
        question = 'What is the six digit PIN?';
        break;
    }

    this.playTTS(question);
  }

handleWizardResponse(response: string): void {
  const lowerResponse = response.toLowerCase().trim();
  if (lowerResponse === 'close form' || lowerResponse === 'cancel') {
    if (this.showAddForm) {
      this.voiceWizardActive = false;
      this.waitingForSubmissionConfirm = false;
      this.playTTS('Closing the form');
      this.toggleAddForm();
    } else {
      this.playTTS('The form is already closed');
    }
    return;
  }

  if (this.waitingForSubmissionConfirm) {
    if (lowerResponse === 'yes') {
      this.waitingForSubmissionConfirm = false;
      this.voiceWizardActive = false;
      this.submitAddHouse();
    } else if (lowerResponse === 'no') {
      this.waitingForSubmissionConfirm = false;
      this.voiceWizardActive = false;
      this.playTTS('Okay, the form is ready to submit manually.');
    } else {
      this.playTTS('Please say yes or no.');
    }
    return;
  }

  const currentStep = this.voiceWizardSteps[this.voiceWizardStepIndex];

  if (lowerResponse === 'yes') {
    this.voiceWizardStepIndex++;
    if (this.voiceWizardStepIndex < this.voiceWizardSteps.length) {
      this.askCurrentQuestion();
    } else {
      this.waitingForSubmissionConfirm = true;
      this.playTTS('Thank you. Form is ready to submit. Do you want to submit it?');
    }
    return;
  }

  if (lowerResponse === 'no') {
    this.askCurrentQuestion();
    return;
  }

  if (currentStep === 'Country') {
    const matchedCountry = this.countries.find(
      c => c.name.toLowerCase() === lowerResponse
    );
    if (matchedCountry) {
      this.addHouseForm.get('Country')?.setValue(matchedCountry);
      this.playTTS('Can we move to next one?');
    } else {
      this.playTTS(`Sorry, I didn't recognize country ${response}`);
      this.askCurrentQuestion();
    }
    return;
  }

  let processedValue = response;
  if (['PIN', 'PostalCode'].includes(currentStep)) {
    processedValue = this.normalizeNumberWords(response).replace(/\s+/g, '');
  }

  const control = this.addHouseForm.get(currentStep);
  if (control) {
    control.setValue(processedValue);
    this.playTTS('Can we move to next one?');
  }
}

}
