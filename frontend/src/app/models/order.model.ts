import { CartItem } from "./cart_item.model";

export interface Order {
  id: number;            // order ID
  user_id: number;       // ID of the user who placed the order
  total_price: number;   // total cost of the order
  status: 'PENDING' | 'PAID' | 'SHIPPED'; // status of the order
  cart_items: CartItem[]; // snapshot of items in the order
  created_at: string;     // timestamps from backend (ISO string)
  updated_at: string;
}