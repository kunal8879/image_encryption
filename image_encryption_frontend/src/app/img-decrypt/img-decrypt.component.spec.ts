import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImgDecryptComponent } from './img-decrypt.component';

describe('ImgDecryptComponent', () => {
  let component: ImgDecryptComponent;
  let fixture: ComponentFixture<ImgDecryptComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ImgDecryptComponent]
    });
    fixture = TestBed.createComponent(ImgDecryptComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
