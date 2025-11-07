import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
// Angular Material modules
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

import { ActivatedRoute, Router } from '@angular/router';
import { ProductsService } from '../../services/products.service';
import { Product } from '../../models/products.model';

@Component({
  selector: 'app-product-form',
  imports: [ReactiveFormsModule, MatFormFieldModule, MatInputModule, MatButtonModule],
  templateUrl: './product-form.component.html',
  styleUrls: ['./product-form.component.scss']
})
export class ProductFormComponent implements OnInit {
  productForm!: FormGroup;
  mode: 'create' | 'edit' = 'create';
  productId?: number;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private productsService: ProductsService
  ) {}

  ngOnInit() {
    this.productForm = this.fb.group({
      name: ['', Validators.required],
      description: [''],
      price: [0, [Validators.required, Validators.min(0)]],
      stock: [0, [Validators.required, Validators.min(0)]],
      category: [''],
      image_url: ['']
    });

    // Determine if we're in edit mode
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.mode = 'edit';
      this.productId = +id;
      this.loadProduct(this.productId);
    }
  }

  loadProduct(id: number) {
    this.productsService.getProduct(id).subscribe({
      next: (product: Product) => this.productForm.patchValue(product),
      error: (err) => console.error('Failed to load product', err)
    });
  }

  onSubmit() {
    if (this.productForm.invalid) return;

    const payload = this.productForm.value as Product;

    if (this.mode === 'create') {
      this.productsService.createProduct(payload).subscribe({
        next: () => this.router.navigate(['/products']),
        error: (err) => console.error('Create failed', err)
      });
    } else {
      this.productsService.updateProduct(this.productId!, payload).subscribe({
        next: () => this.router.navigate(['/products']),
        error: (err) => console.error('Update failed', err)
      });
    }
  }

  cancel() {
    this.router.navigate(['/products']);
  }
}