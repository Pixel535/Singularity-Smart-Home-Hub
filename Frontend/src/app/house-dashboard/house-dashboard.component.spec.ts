import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HouseDashboardComponent } from './house-dashboard.component';

describe('HouseDashboardComponent', () => {
  let component: HouseDashboardComponent;
  let fixture: ComponentFixture<HouseDashboardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HouseDashboardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HouseDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
