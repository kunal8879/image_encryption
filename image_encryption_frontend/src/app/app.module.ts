import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { ImageUploadComponent } from './image-upload/image-upload.component';
import { ImageDownloadComponent } from './image-download/image-download.component';
import { RouterModule } from '@angular/router';

@NgModule({
  declarations: [
    AppComponent,
    ImageUploadComponent,
    ImageDownloadComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot([
      { path: 'image-upload', component: ImageUploadComponent },
      { path: 'image-download', component: ImageDownloadComponent },
    ])
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
