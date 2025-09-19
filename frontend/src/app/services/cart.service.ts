import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Cart } from '../models/cart.model';
import { Observable } from 'rxjs';
import { CartItem } from '../models/cart_item.model';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class CartService {

  private apiUrl = 'http://localhost:8000/cart';

  constructor(private http: HttpClient, private authService: AuthService) {}

  getCarts(): Observable<Cart[]> {
    return this.http.get<Cart[]>(this.apiUrl);
  }

  getCart(): Observable<Cart> {
    let jwtToken = this.authService.getToken();

    return this.http.get<Cart>(`${this.apiUrl}/current`, 
      {
        headers: { Authorization: `Bearer ${jwtToken}` }
      }
    );
  }

  addToCart(cartId: number, item: CartItem): Observable<CartItem> {
    return this.http.post<CartItem>(`${this.apiUrl}/${cartId}/items`, item);
  }
}
