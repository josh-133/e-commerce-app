import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from '../models/products.model';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root',
})
export class ProductsService {
  constructor(private http: HttpClient, private authService: AuthService) {}

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(`api/products`);
  }

  getProduct(id: number) {
    return this.http.get<Product>(`/api/products/${id}`);
  }

  createProduct(product: Product): Observable<Product> {
    const token = this.authService.getToken();
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.post<Product>(`api/products`, product, { headers });
  }

  updateProduct(id: number, product: Partial<Product>) {
    const token = this.authService.getToken();
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.put(`/api/products/${id}`, product, { headers });
  }

  deleteProduct(id: number) {
    const token = this.authService.getToken();
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`
    });
    return this.http.delete(`/api/products/${id}`, { headers });
  }
}