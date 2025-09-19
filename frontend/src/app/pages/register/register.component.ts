import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';

// Angular Material imports
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  standalone: true,
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  imports: [
    ReactiveFormsModule,
    CommonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule
  ]
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;

  constructor(private fb: FormBuilder, private authService: AuthService, private readonly router: Router) {}

  ngOnInit() {
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]]
    }, { validators: this.passwordsMatch });
  }

  // Custom validator to ensure password and confirmPassword match
  passwordsMatch(group: FormGroup) {
    const pass = group.get('password')?.value;
    const confirm = group.get('confirmPassword')?.value;
    return pass === confirm ? null : { passwordsMismatch: true };
  }

  onSubmit() {
    if (this.registerForm.invalid) return;

    const { email, password } = this.registerForm.value;
    this.authService.register(email, password).subscribe({
      next: (res) => {
        console.log('Registration successful:', res);
        this.router.navigate(['/products']);
      },
      error: (err) => console.error('Registration error:', err)
    });
  }
}