import { Component } from '@angular/core';

@Component({
  selector: 'app-img-decrypt',
  templateUrl: './img-decrypt.component.html',
  styleUrls: ['./img-decrypt.component.scss']
})
export class ImgDecryptComponent {
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
  }

}
