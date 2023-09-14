import { Component } from '@angular/core';
import { ClipboardService } from 'ngx-clipboard';

@Component({
  selector: 'app-image-upload',
  templateUrl: './image-upload.component.html',
  styleUrls: ['./image-upload.component.css']
})
export class ImageUploadComponent {
  isDragging = false;
  selectedFile: File | null = null;
  progress: number = 0;
  allowDrop(event: any) {
    event.preventDefault();
  }
  
  handleDrop(event: any) {
    event.preventDefault();
    this.isDragging = false;
  }
  
  dragStart(event: any) {
    this.isDragging = true;
  }
  
  dragEnd(event: any) {
    this.isDragging = false;
 }

 textToCopy : string = '';

  constructor(private clipboardService: ClipboardService) {}

  copyText() {
    this.clipboardService.copyFromContent(this.textToCopy);
  }

//  constructor(private uploadService: UploadService) {}

//   onFileSelected(event: any) {
//     this.selectedFile = event.target.files[0];
//   }

//   onUpload() {
//     if (this.selectedFile) {
//       this.uploadService.uploadFile(this.selectedFile).subscribe((event) => {
//         if (event.type === HttpEventType.UploadProgress) {
//           this.progress = Math.round((100 * event.loaded) / event.total);
//         } else if (event.type === HttpEventType.Response) {
//           // Handle the successful upload response here
//           console.log(event.body);
//         }
//       });
//     }
//   }

}
