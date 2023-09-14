import { Component } from '@angular/core';

@Component({
  selector: 'app-image-download',
  templateUrl: './image-download.component.html',
  styleUrls: ['./image-download.component.css']
})
export class ImageDownloadComponent {
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

}
