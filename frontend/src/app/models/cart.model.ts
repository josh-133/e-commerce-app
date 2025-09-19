import { CartItem } from "./cart_item.model";
import { Status } from "../utils/enums";

export interface Cart {
    id: number;
    user_id: number;
    cart_items: CartItem[];
    created_at: Date;
    updated_at: Date;
    status: Status;
}