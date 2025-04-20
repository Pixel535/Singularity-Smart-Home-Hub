import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HouseInfoComponent } from './house-info.component';

describe('HouseInfoComponent', () => {
  let component: HouseInfoComponent;
  let fixture: ComponentFixture<HouseInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HouseInfoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HouseInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
