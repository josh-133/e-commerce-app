import { Component, OnInit } from '@angular/core';
import { CartService } from '../../services/cart.service';
import { Cart } from '../../models/cart.model';
import { CartItem } from '../../models/cart_item.model';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { OrderService } from '../../services/orders.service';
import { Router } from '@angular/router';
import { switchMap } from 'rxjs';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatButtonModule, MatInputModule],
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss']
})
export class CartComponent implements OnInit {

  cart!: Cart;

  constructor(
    private readonly orderService: OrderService, 
    private readonly cartService: CartService,
    private readonly router: Router
  ) {}

  ngOnInit(): void {
    this.loadCart();
  }

  loadCart(): void {
    this.cartService.getCart().subscribe({
      next: (cart: Cart) => this.cart = cart,
      error: (err) => console.error('Error loading cart:', err)
    });
  }

  getTotal(item: CartItem): number {
    return item.price_at_time * item.quantity;
  }

  removeItem(itemId: number): void {
    if (!this.cart) return;

    this.cartService.removeItem(this.cart.id, itemId).subscribe({
      next: () => {
        this.cart!.cart_items = this.cart!.cart_items.filter(item => item.id != itemId);
      },
      error: (err) => console.error('Error removing item:', err)
    });
  }

  orderNow() {
    if (!this.cart || !this.cart.cart_items?.length) {
      alert('Your cart is empty!');
      return;
    }
  
    this.orderService.createOrder(this.cart.id, this.cart.cart_items).pipe(
      switchMap(() => this.cartService.clearCart(this.cart.id))
    ).subscribe({
      next: (clearedCart) => {
        // Push empty cart to BehaviorSubject
        this.cartService.cart.next(clearedCart);
        alert('Order placed successfully!');
        this.router.navigate(['/products']);
      },
      error: (err) => {
        console.error(err);
        alert('Failed to place order or clear cart.');
      }
    });
    this.cart.cart_items = []
    console.warn(this.cart.cart_items);
  }
}