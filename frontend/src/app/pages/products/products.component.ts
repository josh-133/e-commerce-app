import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ProductsService } from '../../services/products.service';
import { Product } from '../../models/products.model';
import { CartService } from '../../services/cart.service';
import { CartItem } from '../../models/cart_item.model';
import { Cart } from '../../models/cart.model';

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule],
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.scss']
})
export class ProductsComponent implements OnInit {
  products: Product[] = [];
  cart!: Cart;

  constructor(
    private readonly productsService: ProductsService,
    private readonly cartService: CartService,
  ) {}

  ngOnInit() {
    this.productsService.getProducts().subscribe({
      next: (res: Product[]) => {
        this.products = res;
        console.log(this.products);
      },
      error: (err) => console.error('Error fetching products:', err)
    });

    this.cartService.getCart().subscribe(cart => this.cart = cart)
    console.log(this.cart);
    
  }

  addToCart(product: Product) {
    if (!this.cart) {
      console.error("No cart found for user.");
      return;
    }

    const item: CartItem = {
      id: 0,
      cart_id: this.cart.id,
      product_id: product.id,
      quantity: 1,
      price_at_time: product.price,
    }

    this.cartService.addToCart(this.cart.id, item).subscribe(item => {
      this.cart.cart_items.push(item);
    });
  }
}