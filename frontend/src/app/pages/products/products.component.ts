import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ProductsService } from '../../services/products.service';
import { Product } from '../../models/products.model';

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatButtonModule],
  templateUrl: './products.component.html',
  styleUrls: ['./products.component.scss']
})
export class ProductsComponent implements OnInit {
  products: Product[] = [];

  constructor(private productsService: ProductsService) {}

  ngOnInit() {
    this.productsService.getProducts().subscribe({
      next: (res: Product[]) => {
        this.products = res;
        console.log(this.products);
      },
      error: (err) => console.error('Error fetching products:', err)
    });
  }
}