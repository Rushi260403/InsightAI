import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { Token } from '../services/token';

export const authGuard: CanActivateFn = () => {
  const tokenService = inject(Token);
  const router = inject(Router);

  const token = tokenService.getToken();

  console.log('Auth guard running');
  console.log('Token found:', !!token);

  if (token) {
    console.log('Access allowed');
    return true;
  }

  console.log('No token: redirecting to login');
  return router.createUrlTree(['/login']);
};