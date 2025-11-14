import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';
import { Order } from '../models/order.model';
import { CartItem } from '../models/cart_item.model';

@Injectable({ providedIn: 'root' })
export class OrderService {
  constructor(private authService: AuthService, private http: HttpClient) {}

  private getAuthHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    return new HttpHeaders({ Authorization: `Bearer ${token}`});
  }

  createOrder(cartId: number, cartItems: CartItem[]): Observable<Order> {
    return this.http.post<Order>(`api/orders`, 
      {
        cart_id: cartId,
        cart_items: cartItems
      }, { headers: this.getAuthHeaders() });
  }

  getOrders(): Observable<any> {
    return this.http.get(`api/orders`);
  }

  getOrder(id: number): Observable<any> {
    return this.http.get(`api/orders/${id}`);
  }
}