import { Component, OnInit } from '@angular/core';
import { CartService } from '../../services/cart.service';
import { Cart } from '../../models/cart.model';
import { CartItem } from '../../models/cart_item.model';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule, MatTableModule, MatButtonModule, MatInputModule],
  templateUrl: './cart.component.html',
  styleUrls: ['./cart.component.scss']
})
export class CartComponent implements OnInit {

  cart!: Cart;

  constructor(private readonly cartService: CartService) {}

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

  // removeItem(itemId: number): void {
  //   if (!this.cart) return;

  //   this.cartService.removeItem(itemId).subscribe({
  //     next: (updatedCart: Cart) => this.cart = updatedCart,
  //     error: (err) => console.error('Error removing item:', err)
  //   });
  // }

  // updateQuantity(item: CartItem, newQuantity: number): void {
  //   if (!this.cart) return;

  //   this.cartService.updateItem(item.id, { quantity: newQuantity }).subscribe({
  //     next: (updatedCart: Cart) => this.cart = updatedCart,
  //     error: (err) => console.error('Error updating quantity:', err)
  //   });
  // }
}