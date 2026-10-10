import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Auth } from '../../services/auth';
import { Token } from '../../services/token';
import { HostListener } from '@angular/core';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login implements OnInit {
  email: string = '';
  password: string = '';
  message: string = '';
  isLoading: boolean = false;

  constructor(
    private auth: Auth,
    private tokenService: Token,
    private cdr: ChangeDetectorRef,
  ) {}

  ngOnInit(): void {
    this.message = '';
    this.password = '';
    this.isLoading = false;
  }

  onLogin(): void {
    if (!this.email.trim() || !this.password) {
      this.message = 'Please enter email and password.';
      return;
    }

    this.isLoading = true;
    this.message = 'Signing in...';

    this.auth.login(this.email.trim(), this.password).subscribe({
      next: (response) => {
        console.log('SUCCESS RESPONSE:', response);

        this.tokenService.saveToken(response.access_token);
        this.message = `Welcome, ${response.name}!`;
        this.isLoading = false;

        this.cdr.detectChanges();
      },
      error: (error) => {
        console.error('ERROR RESPONSE:', error);

        this.message = error.error?.detail || 'Login failed. Please try again.';
        this.isLoading = false;

        this.cdr.detectChanges();
      },
    });
  }
  resetLoginForm(): void {
    this.email = '';
    this.password = '';
    this.message = '';
    this.isLoading = false;
  }

  @HostListener('reset-login')
  onResetLogin(): void {
    this.resetLoginForm();
  }
}
