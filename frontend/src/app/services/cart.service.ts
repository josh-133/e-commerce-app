import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Cart } from '../models/cart.model';
import { BehaviorSubject, Observable, tap } from 'rxjs';
import { CartItem } from '../models/cart_item.model';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  cart = new BehaviorSubject<Cart | null>(null);
  cart$ = this.cart.asObservable();

  constructor(private http: HttpClient, private authService: AuthService) {}

  private getAuthHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    return new HttpHeaders({ Authorization: `Bearer ${token}`});
  }

  getCarts(): Observable<Cart[]> {
    return this.http.get<Cart[]>(`api/cart`);
  }

  getCart(): Observable<Cart> {

    return this.http.get<Cart>(`api/cart/current`,  { headers: this.getAuthHeaders() })
    .pipe(tap(cart => this.cart.next(cart)));
  }

  addToCart(cartId: number, item: CartItem): Observable<CartItem> {
    return this.http.post<CartItem>(`api/cart/current/items`, item, { headers: this.getAuthHeaders() })
    .pipe(
      tap(() => {
        this.getCart().subscribe();
      })
    );
  }

  updateCartItem(itemId: number, quantity: number) {
    return this.http.put(`/api/cart/current/items/${itemId}`, { quantity });
  }

  removeItem(cartId: number, itemId: number): Observable<any> {
    return this.http.delete(`api/cart/current/items/${itemId}`, { headers: this.getAuthHeaders() })
    .pipe(
      tap(() => {
          this.getCart().subscribe();
        }
      )
    );
  }

  clearCart(cartId: number): Observable<any> {
    return this.http.delete(`/api/cart/current/${cartId}/clear`, { headers: this.getAuthHeaders() });
  }

  getCartValue(): Cart | null {
    return this.cart.value;
  }


}