import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { AppComponent } from './app/app.component';

bootstrapApplication(AppComponent, appConfig)
  .catch((err) => console.error(err)).finally(() => {
    const loader = document.getElementById('global-loader');
    if (loader) {
      loader.style.display = 'none';
    }
  });
