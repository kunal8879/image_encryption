import { Block } from '@angular/compiler';
import { Component } from '@angular/core';

@Component({
  selector: 'app-img-encrypt',
  templateUrl: './img-encrypt.component.html',
  styleUrls: ['./img-encrypt.component.scss']
})
export class ImgEncryptComponent {
  fileName: string = "" ;
  url: any;
  enckey:number = 8745982;


  getImgUrl(event: any) {
    const fileData = event.target.files[0];
    this.fileName = fileData.name;
    console.log(fileData);

    let reader = new FileReader();
    reader.readAsDataURL(fileData);
    reader.onload = () => {
      this.url = reader.result;
    }

    const text = document.getElementById('text');
    text!.style.display = "none";

    const browseBtn = document.getElementById('browse-btn');
    browseBtn!.style.display = "none";
    
    const file = document.getElementById('file');
    file!.style.display = "none";

    const imgSize = document.getElementById('img-display');
    imgSize!.style.maxHeight = "200px";
    imgSize!.style.maxWidth = "400px";

    const submitBtn = document.getElementById('submit-btn');
    submitBtn!.style.display = "block";
  }

  submitImg(){
    const encKey = document.getElementById('enc-key');
    encKey!.style.display = "block";

    const submitBtn = document.getElementById('submit-btn');
    submitBtn!.style.display = "none";

    const fileUpload = document.getElementById('upload');
    fileUpload!.style.display = "none";

    const fileDownload = document.getElementById('download');
    fileDownload!.style.display = "block";    
  }

  copyText(){
    navigator.clipboard.writeText(this.enckey.toString());
  }
}
