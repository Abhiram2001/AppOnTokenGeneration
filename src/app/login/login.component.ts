import { Component, OnInit } from '@angular/core';
import { LoginserviceService } from '../service/loginservice.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private ls:LoginserviceService,private route:Router) { }

  ngOnInit(): void {
  }
  offButton1 = false;
  userN="";
  pass="";
  email="";
  FN="";
  LN="";
  DOB="";
  match:any;
  check=true;
  userFound:"";
  sendDetails(){
    this.ls.Signupcheck(this.userN,this.pass,this.email,this.FN,this.LN,this.DOB).subscribe(
      response=>{
        this.match=response['message'];
        console.log(this.match)
      }
    )
  }
  getDetails(){
    this.ls.Logincheck(this.userN,this.pass).subscribe(
      response=>{
        this.match=response['message'];
        console.log(this.match)
        console.log(response['token'])
        if(this.match=="True"){
          this.route.navigate(['/home'])
        }
        else{
          this.check=false;

        }
      }
    )
  }

  FindUser(){
    console.log(this.userN,"temp")
    this.ls.checkUser(this.userN,"temp").subscribe(
      response=>{
        this.userFound=response['message'];
        console.log(this.match)
      }
    )
  }

  genpass(){
    this.ls.NewPass(this.userN,"temp","temp","temp","temp","temp").subscribe(
      response=>{
        this.match=response['message'];
        console.log(this.match)
      }
    )
  }

  retry(){
    this.check = true;
  }

}
