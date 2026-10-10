import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class Token {
  private readonly tokenKey = 'access_token';

  saveToken(token: string): void {
    localStorage.setItem(this.tokenKey, token);
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  isLoggedIn(): boolean {
    return this.getToken() !== null;
  }

  clearToken(): void {
    localStorage.removeItem(this.tokenKey);
  }
}