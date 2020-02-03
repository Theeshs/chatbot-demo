import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class ChatServiceService {

  constructor(private http: HttpClient) { }

  Chat(data): Observable<any> {
    return this.http.post('https://7a62fe1b.ngrok.io/send_message', data)
  }
}
