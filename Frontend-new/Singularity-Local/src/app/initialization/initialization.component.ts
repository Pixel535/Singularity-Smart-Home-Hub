import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WifiStepComponent } from '../initialization/wifi-step/wifi-step.component';
import { ModeStepComponent } from '../initialization/mode-step/mode-step.component';
import { LoginStepComponent } from './login-step/login-step.component';
import { SelectHouseStepComponent } from './select-house-step/select-house-step.component';
import { CreateHouseStepComponent } from './create-house-step/create-house-step.component';
import { SetPinStepComponent } from './set-pin-step/set-pin-step.component';
import { MqttStepComponent } from './mqtt-form-step/mqtt-form-step.component'; 
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-initialize',
  standalone: true,
  imports: [
    CommonModule,
    WifiStepComponent,
    ModeStepComponent,
    LoginStepComponent,
    SelectHouseStepComponent,
    CreateHouseStepComponent,
    SetPinStepComponent,
    MqttStepComponent
  ],
  templateUrl: './initialization.component.html',
  styleUrls: ['./initialization.component.scss']
})
export class InitializationComponent implements OnInit {
  step: 'wifi' | 'mode' | 'login' | 'selectHouse' | 'createHouse' | 'setPin' | 'mqtt' = 'wifi';
  stepHistory: typeof this.step[] = [];

  isChecking = false;
  createdHouseData: any;
  isHouseCreationOffline = false;
  modeAfterLogin: 'join' | 'new' | null = null;

  private baseInitUrl = `${environment.apiBaseUrl}/initialization`;

  constructor(private router: Router, private http: HttpClient) {}

  ngOnInit(): void {
    this.isChecking = true;

    this.http.get<{ config_exists: boolean, online: boolean }>(`${this.baseInitUrl}/status`)
      .subscribe({
        next: ({ config_exists, online }) => {
          if (online && config_exists) {
            this.router.navigate(['/loginHouse']);
          } else if (online && !config_exists) {
            this.step = 'mode';
          } else {
            this.step = 'wifi';
          }
          this.isChecking = false;
        },
        error: () => {
          this.step = 'wifi';
          this.isChecking = false;
        }
      });
  }

  goToNextStep() {
    const order: typeof this.step[] = [
      'wifi', 'mode', 'login', 'selectHouse', 'createHouse', 'setPin', 'mqtt'
    ];

    const currentIndex = order.indexOf(this.step);
    if (currentIndex !== -1 && currentIndex < order.length - 1) {
      this.stepHistory.push(this.step);
      this.step = order[currentIndex + 1];
    }
  }

  goToStep(step: typeof this.step) {
    if (this.step) {
      this.stepHistory.push(this.step);
    }
    this.step = step;
  }

  handleBack() {
    if (this.stepHistory.length > 0) {
      this.step = this.stepHistory.pop()!;
    }
  }

  setChecking(value: boolean) {
    this.isChecking = value;
  }

  handleOfflineCheck(event: { configExists: boolean }) {
    if (event.configExists) {
      this.router.navigate(['/loginHouse']);
    } else {
      this.goToNextStep();
    }
  }

  onModeSelected(mode: 'local' | 'new' | 'join') {
    if (mode === 'local') {
      this.isHouseCreationOffline = true;
      this.goToStep('createHouse');
    } else {
      this.isHouseCreationOffline = false;
      this.modeAfterLogin = mode;
      this.goToStep('login');
    }
  }

  onUserLoggedIn() {
    if (this.modeAfterLogin === 'join') {
      this.goToStep('selectHouse');
    } else if (this.modeAfterLogin === 'new') {
      this.goToStep('createHouse');
    } else {
      console.warn('Unknown mode after login');
      this.goToStep('mode');
    }
  }

  onHouseCreated(houseData: any) {
    this.createdHouseData = houseData;
    this.goToStep('setPin');
  }

  redirectToLoginHouse() {
    this.router.navigate(['/loginHouse']);
  }

  onPinSet(event: { pin: string }) {
    this.createdHouseData = {
      ...this.createdHouseData,
      PIN: event.pin
    };
    this.goToStep('mqtt');
  }

  onMqttContinue(event: { username: string; password: string }) {
    const fullData = {
      ...this.createdHouseData,
      mqtt: {
        username: event.username,
        password: event.password
      }
    };

    const endpoint = this.isHouseCreationOffline
      ? `${this.baseInitUrl}/create-house-offline`
      : `${this.baseInitUrl}/create-house-online`;

    this.setChecking(true);

    this.http.post(endpoint, fullData).subscribe({
      next: () => {
        this.setChecking(false);
        this.router.navigate(['/loginHouse']);
      },
      error: (err) => {
        this.setChecking(false);
        console.error('Error creating house:', err);
      }
    });
  }
}
