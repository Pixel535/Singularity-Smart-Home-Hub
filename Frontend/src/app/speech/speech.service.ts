import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class SpeechService {
  private apiUrl = 'http://localhost:5000/speech/greet';

  constructor(private http: HttpClient) {}

  playGreeting(houseId: number) {
    this.http.post(this.apiUrl, { HouseID: houseId }, {
      responseType: 'blob',
      withCredentials: true
    }).subscribe({
      next: (blob) => {
        const url = URL.createObjectURL(blob);
        const audio = new Audio(url);
        audio.play();
      },
      error: (err) => {
        console.warn('[TTS] Speech error:', err?.error?.msg || err.message);
      }
    });
  }
}
