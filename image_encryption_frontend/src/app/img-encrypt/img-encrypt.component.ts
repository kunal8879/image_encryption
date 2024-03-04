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

    document.getElementById('text')!.innerHTML = "<style display: none></style>";
    // document.getElementById('browse-button')!.innerHTML = "<style display: none></style>";
    document.getElementById('file')!.innerHTML = "<style display: none></style>";
    const imgSize = document.getElementById('img-display');
    imgSize!.style.maxHeight = "200px";
    imgSize!.style.maxWidth = "400px";

    // submit button code
    // const submitBtn = document.getElementById('submit-btn');
    // submitBtn!.style.display = "";


  }

  


}
