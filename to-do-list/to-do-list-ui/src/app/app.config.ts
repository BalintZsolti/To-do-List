// app.config.ts vagy app.module.ts

import { ApplicationConfig, importProvidersFrom, NgModule } from '@angular/core';
import { provideZoneChangeDetection } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms'; // FormsModule importálása
import { CommonModule } from '@angular/common';
import { routes } from './app.routes';

export const appConfig: ApplicationConfig = {
  providers: [
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes),
    provideHttpClient(),
    importProvidersFrom(CommonModule),
    importProvidersFrom(FormsModule)
  ]
};
