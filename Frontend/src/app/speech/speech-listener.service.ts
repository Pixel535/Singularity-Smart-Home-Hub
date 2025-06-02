import { Injectable, NgZone } from '@angular/core';
import { SpeechService } from './speech.service';

declare global {
  interface Window {
    webkitSpeechRecognition: any;
    SpeechRecognition: any;
  }
}


@Injectable({ providedIn: 'root' })
export class SpeechListenerService {
  private recognition: any;

  constructor(private zone: NgZone, private speech: SpeechService) {
    const SpeechRecognition = window.SpeechRecognition || (window as any).webkitSpeechRecognition;
    this.recognition = new SpeechRecognition();
    this.recognition.lang = 'en-US';
    this.recognition.continuous = true;
    this.recognition.interimResults = false;

    this.recognition.onresult = (event: any) => {
      const result = event.results[event.results.length - 1][0].transcript;
      console.log(result);
      this.zone.run(() => {
        this.speech.emitCommand(result);
      });
    };


    this.recognition.onerror = (event: any) => {
      console.error('[SpeechRecognition] error:', event.error);
    };
  }

  startListening(): void {
    this.recognition.start();
    console.log('[SpeechRecognition] started');
  }

  stopListening(): void {
    this.recognition.stop();
    console.log('[SpeechRecognition] stopped');
  }
}
