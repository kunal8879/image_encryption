import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { ImgEncryptComponent } from './img-encrypt/img-encrypt.component';
import { ImgDecryptComponent } from './img-decrypt/img-decrypt.component';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

@NgModule({
  declarations: [
    AppComponent,
    ImgEncryptComponent,
    ImgDecryptComponent,
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot([
      { path: '', component: ImgEncryptComponent },
      { path: 'image-upload', component: ImgEncryptComponent },
      { path: 'image-download', component: ImgDecryptComponent },
    ]),
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
