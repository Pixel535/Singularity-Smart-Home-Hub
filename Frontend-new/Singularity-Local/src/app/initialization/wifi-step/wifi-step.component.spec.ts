import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WifiStepComponent } from './wifi-step.component';

describe('WifiStepComponent', () => {
  let component: WifiStepComponent;
  let fixture: ComponentFixture<WifiStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WifiStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WifiStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
