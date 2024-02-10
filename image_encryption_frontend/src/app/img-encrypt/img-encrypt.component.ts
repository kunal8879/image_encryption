import { Component } from '@angular/core';

@Component({
  selector: 'app-img-encrypt',
  templateUrl: './img-encrypt.component.html',
  styleUrls: ['./img-encrypt.component.scss']
})
export class ImgEncryptComponent {
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

 url="./assets/icon.jpg";

 changeImg(event:any){
  if(event.target.files.length > 0){
    var reader = new FileReader();
    const imgSize = document.getElementById('img');
    const keyVisibility = document.getElementById('key');
    const uploadBtn = document.getElementById('upload');
    reader.readAsDataURL(event.target.files[0]);
    reader.onload = (event:any) => {
      this.url = event.target?.result;
    }
    imgSize!.style.maxHeight = "200px";
    imgSize!.style.maxWidth = "400px";  
    imgSize!.style.gridColumn = "100%";
    keyVisibility!.style.visibility = "visible";
    uploadBtn!.style.visibility = "hidden";
  }  
 }
}
