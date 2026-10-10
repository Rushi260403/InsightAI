import { Component } from '@angular/core';
import { Router, RouterLink, RouterOutlet } from '@angular/router';
import { Token } from './services/token';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  constructor(
    private tokenService: Token,
    private router: Router
  ) {}

  logout(): void {
    this.tokenService.clearToken();

    // Reset the login form if the Login component is currently active.
    const loginComponent = document.querySelector('app-login');

    if (loginComponent) {
      loginComponent.dispatchEvent(new CustomEvent('reset-login'));
    }

    window.location.href = '/login';
  }
}