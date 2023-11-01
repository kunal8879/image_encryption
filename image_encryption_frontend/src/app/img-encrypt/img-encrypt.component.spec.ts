import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImgEncryptComponent } from './img-encrypt.component';

describe('ImgEncryptComponent', () => {
  let component: ImgEncryptComponent;
  let fixture: ComponentFixture<ImgEncryptComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ImgEncryptComponent]
    });
    fixture = TestBed.createComponent(ImgEncryptComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
