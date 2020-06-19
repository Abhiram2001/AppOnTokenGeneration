import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LoginserviceService {

  constructor(private http: HttpClient) { }
  Signupcheck(userN:any,pass:any,email:any,FN:any,LN:any,DOB:any){
    return this.http.post('http://127.0.0.1:8000/Signupcheck',{
      "username" : userN,"password" : pass,"Email":email,"FirstName":FN,"LastName":LN,"DateOfBirth":DOB})
  }
  Logincheck(userN:any,pass:any){
    return this.http.post('http://127.0.0.1:8000/Logincheck',{
      "username" : userN,"password" : pass})
  }
  sendImage(imgUrl){
    return this.http.post('http://127.0.0.1:8000/Photocheck',{
      "image":imgUrl})
  }
  checkUser(userN:any,pass:any){
    console.log(userN)
    return this.http.post('http://127.0.0.1:8000/Usercheck',{
      "username":userN,"password":pass})
  }
  NewPass(userN:any,pass:any,email:any,FN:any,LN:any,DOB:any){
    return this.http.post('http://127.0.0.1:8000/genpassword',{
      "username" : userN,"password" : pass,"Email":email,"FirstName":FN,"LastName":LN,"DateOfBirth":DOB
    })
  }
}
