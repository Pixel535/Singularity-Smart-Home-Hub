import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChangePINComponent } from './change-pin.component';

describe('ChangePINComponent', () => {
  let component: ChangePINComponent;
  let fixture: ComponentFixture<ChangePINComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ChangePINComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ChangePINComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
