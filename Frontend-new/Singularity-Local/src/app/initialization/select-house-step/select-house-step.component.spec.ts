import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectHouseStepComponent } from './select-house-step.component';

describe('SelectHouseStepComponent', () => {
  let component: SelectHouseStepComponent;
  let fixture: ComponentFixture<SelectHouseStepComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SelectHouseStepComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SelectHouseStepComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
