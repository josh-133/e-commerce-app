export interface CartItem {
    id?: number;
    name: string;
    cart_id: number;
    product_id: number;
    quantity: number;
    price_at_time: number;
}