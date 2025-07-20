import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetPinStepComponent } from './set-pin-step.component';

describe('SetPinStepComponent', () => {
  let component: SetPinStepComponent;
  let fixture: ComponentFixture<SetPinStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SetPinStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SetPinStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
