import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MqttFormStepComponent } from './mqtt-form-step.component';

describe('MqttFormStepComponent', () => {
  let component: MqttFormStepComponent;
  let fixture: ComponentFixture<MqttFormStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MqttFormStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MqttFormStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
