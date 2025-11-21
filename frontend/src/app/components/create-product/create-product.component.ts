import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { Product } from '../../models/products.model';
import { ProductsService } from '../../services/products.service';

@Component({
  selector: 'app-create-product',
  templateUrl: './create-product.component.html',
})
export class CreateProductComponent {
  constructor(
    private productService: ProductsService,
    private router: Router
  ) {}

  onCreate(productData: Product) {
    this.productService.createProduct(productData).subscribe({
      next: (createdProduct: Product) => {
        console.log('Product created:', createdProduct);
        this.router.navigate(['/products']);
      },
      error: (err: Error) => {
        console.error('Failed to create product', err);
      },
    });
  }
}