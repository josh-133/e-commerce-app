import { Component } from '@angular/core';
import { ProductsService } from '../../services/products.service';

@Component({
  selector: 'app-products',
  imports: [],
  templateUrl: './products.component.html',
  styleUrl: './products.component.scss'
})
export class ProductsComponent {
  products: any[] = [];

  constructor(private productsService: ProductsService) {}

  // ngOnInit() {
  //   this.productsService.getProducts().subscribe((res: any) {
  //     this.products = res;
  //   })
  // }

}
