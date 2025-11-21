import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProductsService } from '../../services/products.service';
import { Product } from '../../models/products.model';

@Component({
  selector: 'app-edit-product',
  templateUrl: './edit-product.component.html',
})
export class EditProductComponent implements OnInit {
  product?: Product;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private productService: ProductsService
  ) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.productService.getProduct(id).subscribe((p) => (this.product = p));
  }

  onUpdate(updatedData: Omit<Product, 'id'>) {
    if (!this.product) return;
    this.productService.updateProduct(this.product.id, updatedData).subscribe(() => {
      this.router.navigate(['/products']);
    });
  }
}