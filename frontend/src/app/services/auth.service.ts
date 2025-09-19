import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private loggedIn = new BehaviorSubject<boolean>(false);
  private userEmail = new BehaviorSubject<string>('');

  isLoggedIn$ = this.loggedIn.asObservable();
  userEmail$ = this.userEmail.asObservable(); // <-- add this

  constructor(private http: HttpClient) {
    const token = localStorage.getItem('jwtToken');
    const email = localStorage.getItem('userEmail');
    if (token && email) {
      this.loggedIn.next(true);
      this.userEmail.next(email);
    }
  }

  login(email: string, password: string): Observable<any> {
    return this.http.post('http://localhost:8000/auth/login', { email, password });
  }

  register(email: string, password: string): Observable<any> {
    return this.http.post('http://localhost:8000/auth/register', { email, password });
  }

  isLoggedIn(): boolean {
    return this.loggedIn.value;
  }

  getToken(): string | null {
    return localStorage.getItem('jwtToken');
  }

  saveUser(email: string, token: string): void {
    localStorage.setItem('jwtToken', token);
    localStorage.setItem('userEmail', email);
    this.loggedIn.next(true);
    this.userEmail.next(email);
  }

  logout(): void {
    localStorage.removeItem('jwtToken');
    localStorage.removeItem('userEmail');
    this.loggedIn.next(false);
    this.userEmail.next('');
  }
}