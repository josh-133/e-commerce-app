import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { RegisterComponent } from './pages/register/register.component';
import { ProductsComponent } from './pages/products/products.component';
import { CartComponent } from './pages/cart/cart.component';
import { ProductFormComponent } from './pages/product-form/product-form.component';

export const routes: Routes = [
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    { path: 'products', component: ProductsComponent },
    { path: 'admin/products/new', component: ProductFormComponent },
    { path: 'products/edit/:id', component: ProductFormComponent },
    { path: 'cart', component: CartComponent },
    { path: '', redirectTo: '/products', pathMatch: 'full' }
  ];
