import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateHouseStepComponent } from './create-house-step.component';

describe('CreateHouseStepComponent', () => {
  let component: CreateHouseStepComponent;
  let fixture: ComponentFixture<CreateHouseStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateHouseStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreateHouseStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
