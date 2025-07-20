import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginToHouseComponent } from './login-to-house.component';

describe('LoginToHouseComponent', () => {
  let component: LoginToHouseComponent;
  let fixture: ComponentFixture<LoginToHouseComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LoginToHouseComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LoginToHouseComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
