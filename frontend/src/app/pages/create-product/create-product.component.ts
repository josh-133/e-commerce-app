import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ProductsService } from '../../services/products.service';
import { Product } from '../../models/products.model';
import { Cart } from '../../models/cart.model';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-create-product',
  standalone: true,
  imports: [
    CommonModule, 
    MatCardModule, 
    MatButtonModule, 
    ReactiveFormsModule, 
    CommonModule,
    MatCardModule,
    MatButtonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule],
  templateUrl: './create-product.component.html',
  styleUrls: ['./create-product.component.scss']
})
export class CreateProductComponent {
  productForm: FormGroup;
  successMessage = '';
  errorMessage = '';
  cart: Cart | null = null;

  constructor(
    private readonly productsService: ProductsService,
    private fb: FormBuilder,
  ) {
    this.productForm = this.fb.group({
      name: [''],
      description: [''],
      price: [0],
      category: [''],
      image_url: [''],
      stock: [0]
    });
  }

  onSubmit() {
    if (this.productForm.invalid) return;

    const product: Product = this.productForm.value;

    this.productsService.createProduct(product).subscribe({
      next: (res) => {
        this.successMessage = `Product "${res.name} created successfully!"`
        this.productForm.reset();
      },
      error: (err) => {
        this.errorMessage = "Failed to create product."
        console.error(err);
      }
    });
  }
}