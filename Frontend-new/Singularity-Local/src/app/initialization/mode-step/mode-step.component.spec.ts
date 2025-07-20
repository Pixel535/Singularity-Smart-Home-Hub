import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModeStepComponent } from './mode-step.component';

describe('ModeStepComponent', () => {
  let component: ModeStepComponent;
  let fixture: ComponentFixture<ModeStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModeStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModeStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
