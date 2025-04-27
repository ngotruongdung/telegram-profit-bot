from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging

# Cấu hình logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Hàm tính toán lợi nhuận
def calculate_profit(revenue, ad_cost_usd, exchange_rate=26160):
    # Quy đổi USD sang VNĐ
    ad_cost_vnd = ad_cost_usd * exchange_rate
    
    # Tính toán doanh thu sau hoàn (10%)
    refund = revenue * 0.1
    actual_revenue = revenue - refund
    
    # Tính chi phí (vốn 90k/sp, ship 12k/đơn, ship hoàn 6k/đơn)
    avg_order_value = 165000  # Giá trị trung bình 1 đơn
    num_orders = revenue / avg_order_value
    num_refund_orders = num_orders * 0.1
    
    # Chi phí vốn
    successful_orders = num_orders - num_refund_orders
    product_cost = successful_orders * 90000
    
    # Chi phí vận chuyển
    shipping_cost = num_orders * 12000
    refund_shipping_cost = num_refund_orders * 6000
    total_shipping = shipping_cost + refund_shipping_cost
    
    # Tổng chi phí
    total_cost = product_cost + total_shipping + ad_cost_vnd
    
    # Lợi nhuận
    profit = actual_revenue - total_cost
    
    # Trả về kết quả định dạng
    return f"""
📊 **Kết quả tính toán**:
- Doanh thu gốc: {revenue:,.0f} VNĐ
- Doanh thu thực (sau hoàn 10%): {actual_revenue:,.0f} VNĐ
- Chi phí vốn: {product_cost:,.0f} VNĐ
- Chi phí vận chuyển: {total_shipping:,.0f} VNĐ
- Chi phí quảng cáo: {ad_cost_vnd:,.0f} VNĐ
- **Lợi nhuận**: {profit:,.0f} VNĐ
    """

# Hàm xử lý lệnh /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "🤖 **Bot Tính Lợi Nhuận**\n\n"
        "Gửi doanh thu (VNĐ) và chi phí quảng cáo (USD) theo định dạng:\n"
        "`<doanh thu> <quảng cáo USD>`\n\n"
        "Ví dụ: `4775000 48.34`"
    )

# Hàm xử lý tin nhắn người dùng
def handle_message(update: Update, context: CallbackContext) -> None:
    try:
        text = update.message.text
        revenue, ad_cost_usd = map(float, text.split())
        result = calculate_profit(revenue, ad_cost_usd)
        update.message.reply_markdown(result)
    except Exception as e:
        update.message.reply_text("⚠️ Sai định dạng! Vui lòng nhập `<doanh thu> <quảng cáo USD>`")

def main() -> None:
    # Thay YOUR_TOKEN bằng token bot của bạn
    updater = Updater("7750073984:AAHzrIlmC-ZzFF1S2efn6yXyFdzkn-ICQIM", use_context=True)
    dispatcher = updater.dispatcher

    # Đăng ký command và message handler
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Khởi động bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
